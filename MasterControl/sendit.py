import socket
import time
import random
import sys
import yaml

from math import ceil

IPADDR = 'localhost'
PORTNUM = 8080
FPS = 32

HIGH = 255
LOW = 0

N_FLOWERS = 16
N_LIGHTS = 4

BRIGHTNESS_CACHING = False

MAX_FRAMES = FPS
MAX_FRAMES = -1

FLOWERS_CONF = "flowers.conf"

flowers = []
effects = []

frameCount = 0

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
s.connect((IPADDR, PORTNUM))

################################################################################

def log(msg):
  print msg

################################################################################

class Effect(object):
  def next(self):
    pass

################################################################################

def scale(OldMin, OldMax, NewMin, NewMax, OldValue):
  return (((OldValue - OldMin) * (NewMax - NewMin)) / (OldMax - OldMin)) + NewMin

def clamp(x, lo, hi):
  if x < lo:
    return lo
  elif x > hi:
    return hi
  else:
    return x

################################################################################

class Circle(Effect):
  def __init__(self, flowers, frames=FPS, direction=1, trail=2, brightness=HIGH, postFade=0.25, preFade=0.2):
    self.flowers = flowers # on which flowers
    self.frames = frames # frames to complete a circuit
    self.direction = 1 if direction > 0 else -1
    self.trail = trail
    self.brightness = brightness
    self.postFade = clamp(postFade, 0, 1)
    self.preFade = clamp(preFade, 0, 1)

    self.curFrame = 0

    for flower in flowers:
      for light in flower.lights:
        light.register(self)

  def remove(self):
    for flower in flowers:
      for light in lights:
        light.deregister(self)

  # TODO you can make this much more efficient...
  def next(self):
    self.curFrame = (self.curFrame + self.direction) % self.frames
    lightIdx = self.curFrame / float(self.frames) * N_LIGHTS

    for flower in self.flowers:
      if self.direction == 1:
        dist = lightIdx - int(lightIdx)
      else:
        dist = int(ceil(lightIdx)) - lightIdx

      try:
        multiplier = clamp(scale(0, self.preFade, 0.0, 1.0, dist), 0.0, 1.0)
      except:
        multiplier = 1.0

      light = flower.get(int(lightIdx)).set(self, int(self.brightness * multiplier))
#      print "    j %d multiplier %.3f" % (int(lightIdx), multiplier)

      for i in range(1, N_LIGHTS):
        if self.direction == 1:
          j = int(lightIdx) - i
          diff = lightIdx - j
          if j < 0:
            j = j + N_LIGHTS
        else:
          j = int(lightIdx) + i
          diff = j - lightIdx + 1
          if j >= N_LIGHTS:
            j = j - N_LIGHTS

        light = flower.get(j)

        if diff > self.trail+1:
#          print "i %d j %d 0%%" % (i, j)
          light.set(self, 0)
          continue

        rescaled = scale(1-self.postFade, self.trail+1-self.postFade, 1.0, 0.0, diff)
        multiplier = clamp(rescaled, 0.0, 1.0)
        value = int(self.brightness * multiplier)
#        print "i %d j %d multiplier %.3f value %3d lightIdx %.3f diff %.3f rescaled %.3f" % (i, j, multiplier, value, lightIdx, diff, rescaled)
        light = flower.get(j)
        light.set(self, value)

#    print ""

################################################################################

class Full(Effect):
  def __init__(self, objs, value=HIGH):
    self.objs = objs
    self.value = value
    self.first = True

    for obj in objs:
      obj.register(self)
      obj.set(self, value)

  def remove(self):
    for obj in objs:
      obj.deregister(self)

################################################################################

class Erratic(Effect):
  pass

def erratic(repeat):
  for q in range(repeat):
    full(255 if q % 2 else 0, random.expovariate(10.0))

################################################################################

class Fade(Effect):
  pass

################################################################################

class Lightable(object):
  def __init__(self):
    self._mod = {}
    self._effects = []
    self._lastFrame = -1
    self._lastBrightness = 0
    self._valid = True

  def register(self, effect):
    self._effects.append(effect)
    self.set(effect, 0)
    self._valid = False

  def deregister(self, effect):
    self._effects.remove(effect)
    self._valid = False

  def adjust(self, effect, value):
    self._mod[effect] = self._mod[effect] + value
    self._valid = False

  def set(self, effect, value):
    self._mod[effect] = value
    self._valid = False

################################################################################

class Light(Lightable):
  def __init__(self, flower):
    super(Light, self).__init__()
    self._flower = flower

  def getBrightness(self, frame=None):
    if BRIGHTNESS_CACHING and self._valid and self._lastFrame == frame:
      return self._lastBrightness

    self._lastBrightness = self._flower.getBrightness(frame)

    for effect in self._effects:
      self._lastBrightness = self._lastBrightness + self._mod[effect]

    self._lastFrame = frame
    self._valid = True
    return self._lastBrightness

################################################################################

class Flower(Lightable):
  def __init__(self, x=0, y=0, h=0):
    super(Flower, self).__init__()
    self.lights = [Light(self), Light(self), Light(self), Light(self)] # TRDL
    self.lightsIdx = range(len(self.lights))

    self.x = x
    self.y = y
    self.h = h

  def get(self, idx):
    return self.lights[self.lightsIdx[idx]]

  def getBrightness(self, frame=None):
    if BRIGHTNESS_CACHING and self._lastFrame == frame:
      return self._lastBrightness

    self._lastBrightness = 0

    for effect in self._effects:
      self._lastBrightness = self._lastBrightness + self._mod[effect]

    self._lastFrame = frame
    return self._lastBrightness

  def rotateLightIdx(self, value):
    pass

  def reorderLightIdx(self, value):
    pass

################################################################################

def loadFlowers(fileName):
  try:
    f = open(fileName, "r")
    conf = yaml.load(f)
    f.close()
    for flower in conf["flowers"]:
      x = flower.get("x", 0)
      y = flower.get("y", 0)
      h = flower.get("h", 0)
      flowers.append(Flower(x, y, h))
  except:
    log("error loading flowers configuration file")
    for i in range(N_FLOWERS):
      flowers.append(Flower())

################################################################################

def constructPayload(flowers):
  res = "%3d " % (len(flowers)*N_LIGHTS)

  for flower in flowers:
    for idx in range(len(flower.lights)):
      res += "%3d " % (min(max(flower.lights[idx].getBrightness(frameCount), 0), 255))

  return res

################################################################################

def setup():
  loadFlowers(FLOWERS_CONF)

  effects.append(Circle(flowers[0:8], frames=FPS*.75, trail=1, direction=-1, postFade=0.2, preFade=0))
  effects.append(Circle(flowers[9:16], frames=FPS*2, trail=1.5, direction=1, postFade=0.2, preFade=0))
  effects.append(Full(flowers, HIGH/2))

################################################################################

def loop():
  for effect in effects:
    effect.next()

#  sys.stdout.write("hey: ")
#  for flower in flowers:
#    for i in range(N_LIGHTS):
#      sys.stdout.write("%3d " % flower.get(i).getBrightness())
#  print ""

  payload = constructPayload(flowers)
#  print payload
  s.send(payload)

################################################################################

if __name__ == "__main__":
  setup()

  loopDelta = 1./FPS
  currentTime = targetTime = time.time()

  while MAX_FRAMES < 0 or frameCount < MAX_FRAMES:
    previousTime, currentTime = currentTime, time.time()
    timeDelta = currentTime - previousTime

    time.sleep(random.uniform(0, loopDelta / 2.))

    loop()

    targetTime += loopDelta
    sleepTime = targetTime - time.time()
    if sleepTime > 0:
#      print "%.5f delta %.5f" % (sleepTime, loopDelta)
      time.sleep(sleepTime)
    else:
      print 'took too long'

    frameCount = frameCount + 1

  s.close()

