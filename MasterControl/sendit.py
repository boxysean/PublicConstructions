import socket
import time
import random
import sys
import yaml
import argparse
import os

from math import ceil

HIGH = 255
LOW = 0

N_FLOWERS = 16
N_LIGHTS = 4

DEFAULT_IP = "127.0.0.1"
DEFAULT_PORT = 9930
DEFAULT_FPS = 32

DEFAULT_CONFIG_FILE = "settings.conf"
DEFAULT_FLOWERS_FILE = "flowers.conf"
DEFAULT_SCENES_FILE = "scenes.conf"

DEFAULT_SCENE_TIME = 10000
DEFAULT_SCENE_DURATION = 10000

MAX_FRAMES = -1

BRIGHTNESS_CACHING = False

flowerShift = [ 4, 5, 6, 7, 0, 1, 2, 3, 12, 13, 14, 15, 8, 9, 10, 11 ]
flowerRemapping = True

effects = []
_flowers = []
scenes = []
sceneIdx = -1

FPS = DEFAULT_FPS
frameCount = 0
currentTime = 0
startTime = 0

sock = None

################################################################################

def log(*msg):
  print " ".join([str(x) for x in msg])

def rotate(l,n):
  return l[n:] + l[:n]

def getFlower(idx):
  return _flowers[idx]

################################################################################

class Effect(object):
  def add(self):
    for obj in self.objs:
      obj.register(self)

  def remove(self):
    for obj in self.objs:
      obj.deregister(self)

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

  def add(self):
    for flower in self.flowers:
      for light in flower.lights:
        light.register(self)

  def remove(self):
    for flower in self.flowers:
      for light in flower.lights:
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

  def add(self):
    for obj in self.objs:
      obj.register(self)
      obj.set(self, self.value)

################################################################################

class GlistenSingle(Effect):
  def __init__(self, obj, fadeOut=0.25, frames=FPS):
    self.obj = obj
    self.fadeOut = fadeOut
    self.frames = frames

    self.value = 0
    self.maxValue = 0

  def add(self):
    pass

  def remove(self):
    pass

  def next(self):
    self.obj.set(self, self.value)
    if self.fadeOut > 0:
      self.value = self.value - (float(self.maxValue) / (self.frames * self.fadeOut))

  def setBrightness(self, value):
    self.value = value
    self.maxValue = value

class Glisten(Effect):
  # fade, expected time on, expected time off
  def __init__(self, objs, brightness=HIGH, fadeOut=0.25, exp=1.0, expOn=-1, expOff=-1, frames=FPS):
    self.objs = objs
    self.brightness = brightness
    self.fadeOut = fadeOut

    if expOn >= 0:
      self.expOn = expOn
    else:
      self.expOn = exp

    if expOff >= 0:
      self.expOff = expOff
    else:
      self.expOff = exp

    self.frames = frames

    self.curState = {}
    self.singles = {}
    self.ison = {}

    for obj in objs:
      self.curState[obj] = 0
      self.singles[obj] = GlistenSingle(obj, fadeOut=fadeOut, frames=frames)
      self.ison[obj] = random.choice([True, False])

  def add(self):
    for obj in self.objs:
      single = self.singles[obj]
      obj.register(single)

  def remove(self):
    for obj in self.objs:
      single = self.singles[obj]
      obj.deregister(single)

  def randomFrames(self, variable):
    return int(random.expovariate(variable) * self.frames)

  def next(self):
    for obj in self.objs:
      state = self.curState[obj]
      single = self.singles[obj]

      if state == 0:
        ison = self.ison[obj]
        if ison:
          if self.fadeOut == 0:
            single.setBrightness(LOW)
          frames = self.randomFrames(self.expOff)
          self.curState[obj] = frames
        else:
          single.setBrightness(self.brightness)
          frames = self.randomFrames(self.expOn)
          self.curState[obj] = frames

        self.ison[obj] = not ison
      else:
        self.curState[obj] = state-1

      single.next()

################################################################################

class Fade(Effect):
  def __init__(self, objs, frames=FPS, brightness=HIGH):
    self.objs = objs
    self.frames = frames
    self.brightness = brightness

    self.curFrame = 0

  def next(self):
    if self.curFrame < self.frames/2:
      curBrightness = int(float(self.curFrame) / self.frames * self.brightness * 2)
    else:
      curBrightness = int(float(self.frames - self.curFrame) / self.frames * self.brightness * 2)
      
    for obj in self.objs:
      obj.set(self, curBrightness)

    self.curFrame = self.curFrame + 1
    if self.curFrame >= self.frames:
      self.curFrame = self.curFrame - self.frames

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
    self.lights = []

    for i in range(N_LIGHTS):
      self.lights.append(Light(self))

    self.lightsIdx = range(N_LIGHTS)

    self.x = x
    self.y = y
    self.h = h

  def get(self, idx):
    return self.lights[idx]

  def getShift(self, idx):
    return self.lightsIdx[idx]

  def getBrightness(self, frame=None):
    if BRIGHTNESS_CACHING and self._lastFrame == frame:
      return self._lastBrightness

    self._lastBrightness = 0

    for effect in self._effects:
      self._lastBrightness = self._lastBrightness + self._mod[effect]

    self._lastFrame = frame
    return self._lastBrightness

  def rotateLightIdx(self, value):
    self.lightsIdx = rotate(self.lightsIdx, value)

  def reorderLightIdx(self, value):
    self.lightsIdx = value

################################################################################

class Scene(object):
  def __init__(self, name, sequences):
    self.name = name
    self.sequences = sequences

    self.duration = 0

    for sequence in sequences:
      self.duration = max(self.duration, sequence.time + sequence.duration)

################################################################################

class Sequence(object):
  def __init__(self, time, duration, effects):
    self.time = time
    self.duration = duration
    self.effects = effects
    self.invoked = False

  def invoke(self):
    global effects
    self.invoked = True
    for effect in self.effects:
      effect.add()
      effects.append(effect)

  def revoke(self):
    global effects
    self.invoked = False
    for effect in self.effects:
      effect.remove()
      effects.remove(effect)

################################################################################

def load(fileName, flowerFile=None, sceneFile=None):
  global sock
  global flowerRemapping

  f = open(fileName, "r")
  conf = yaml.load(f)
  f.close()

  settings = conf["settings"]

  ip = settings.get("ip", DEFAULT_IP)
  port = settings.get("port", DEFAULT_PORT)

  log("connecting", ip, port)

  sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
  sock.connect((ip, port))

  FPS = settings.get("fps", DEFAULT_FPS)

  MAX_FRAMES = settings.get("maxFrames", -1)
  flowerRemapping = settings.get("flowerRemapping", True)

  if flowerFile:
    loadFlowers(flowerFile)
  else:
    loadFlowers(settings.get("flowerConf", DEFAULT_FLOWERS_FILE))

  if sceneFile:
    loadScenes(sceneFile)
  else:
    loadScenes(settings.get("scenesConf", DEFAULT_SCENES_FILE))

################################################################################

def loadFlowers(fileName):
  f = open(fileName, "r")
  conf = yaml.load(f)
  f.close()

  for flower in conf["flowers"]:
    x = flower.get("x", 0)
    y = flower.get("y", 0)
    h = flower.get("h", 0)
    flowerObj = Flower(x, y, h)

    if "lightsIdx" in flower:
      flowerObj.reorderLightIdx(flower["lightsIdx"])

    if "lightsRot" in flower:
      flowerObj.rotateLightIdx(flower["lightsRot"])

    _flowers.append(flowerObj)

################################################################################

def loadScenes(fileName):
  global scenes

  f = open(fileName, "r")
  conf = yaml.load(f)
  f.close()

  for sceneIdx, scene in enumerate(conf["scenes"], 1):
    name = scene.get("name", "Scene %d" % (sceneIdx))
    sequences = []

    for seqIdx, sequence in enumerate(scene.get("sequence", [])):
      time = sequence.get("time", [DEFAULT_SCENE_TIME, seqIdx])

      if isinstance(time, list):
        time = time[0] * time[1]

      duration = sequence.get("duration", DEFAULT_SCENE_DURATION)
      effects = []

      for effect in sequence.get("effects", []):
        effectObj = makeEffect(effect)
        effects.append(effectObj)

      sequences.append(Sequence(time, duration, effects))
     
    sceneObj = Scene(name, sequences)
    scenes.append(sceneObj)

################################################################################

def getFlowerObjs(flowerIdx):
  if isinstance(flowerIdx, int):
    flowerIdx = [flowerIdx]

  flowerObjs = []
  for idx in flowerIdx:
    flowerObjs.append(getFlower(idx))

  return flowerObjs

################################################################################

def getLightObjs(lightIdx):
  if isinstance(lightIdx, int):
    lightIdx = [lightIdx]

  lightObjs = []
  for idx in lightIdx:
    if isinstance(idx, list):
      lightObjs.append(getFlower(idx[0]).get(idx[1]))
    else:
      lightObjs.append(getFlower(idx/4).get(idx%4))

  return lightObjs

################################################################################

def makeEffect(effect):
  params = effect.get("params", {})
  effectType = effect["type"]

  if effectType == "Full":
    value = params.get("value", HIGH)
    lightObjs = getLightObjs(params.get("lightIdx", []))
    flowerObjs = getFlowerObjs(params.get("flowerIdx", []))
    return Full(lightObjs + flowerObjs, value = value)

  elif effectType == "Fade":
    brightness = params.get("brightness", HIGH)

    if "time" in params:
      frames = int(params["time"] / 1000.0 * FPS)
    else:
      frames = params.get("frames", FPS)

    lightObjs = getLightObjs(params.get("lightIdx", []))
    flowerObjs = getFlowerObjs(params.get("flowerIdx", []))
    return Fade(lightObjs + flowerObjs, brightness=brightness, frames=frames)

  elif effectType == "Circle":
    flowerObjs = getFlowerObjs(params.get("flowerIdx", []))

    if "time" in params:
      frames = int(params["time"]  / 1000.0 * FPS)
    else:
      frames = params.get("frames", FPS)

    direction = params.get("direction", 1)
    trail = params.get("trail", 2)
    brightness = params.get("brightness", HIGH)
    postFade = params.get("postFade", 0.25)
    preFade = params.get("preFade", 0.2)

    return Circle(flowers=flowerObjs, frames=frames, direction=direction, trail=trail, brightness=brightness, postFade=postFade, preFade=preFade)

  elif effectType == "Glisten":
    flowerObjs = getFlowerObjs(params.get("flowerIdx", []))
    lightObjs = getLightObjs(params.get("lightIdx", []))
    brightness = params.get("brightness", HIGH)
    fadeOut = params.get("fadeOut", 0.25)
    exp = params.get("exp", 1.0)
    expOn = params.get("expOn", -1)
    expOff = params.get("expOff", -1)

    if "time" in params:
      frames = int(params["time"]  / 1000.0 * FPS)
    else:
      frames = params.get("frames", FPS)

    return Glisten(flowerObjs + lightObjs, brightness=brightness, fadeOut=fadeOut, exp=exp, expOn=expOn, expOff=expOff, frames=frames)

################################################################################

def constructPayload(withShift=True):
  lights = [0 for i in range(N_FLOWERS * N_LIGHTS)]

  for i in range(len(_flowers)):
    flower = getFlower(i)
    shift = flowerShift[i]
    for idx in range(len(flower.lights)):
      if withShift:
        lights[4*shift + flower.getShift(idx)] = min(max(flower.get(idx).getBrightness(frameCount), 0), 255)
      else:
        lights[4*i + idx] = min(max(flower.get(idx).getBrightness(frameCount), 0), 255)

  res = "%3d " % (N_FLOWERS * N_LIGHTS)

  for x in lights:
    res += "%3d " % (x)

  return res

################################################################################

def setup():
  if len(sys.argv) > 1 and os.path.isfile(sys.argv[1]):
    configFile = sys.argv[1]
  else:
    configFile = DEFAULT_CONFIG_FILE

  if len(sys.argv) > 2 and os.path.isfile(sys.argv[2]):
    flowerFile = sys.argv[2]
  else:
    flowerFile = None

  if len(sys.argv) > 3 and os.path.isfile(sys.argv[3]):
    sceneFile = sys.argv[3]
  else:
    sceneFile = None

  load(configFile, flowerFile, sceneFile)

################################################################################

def loop():
  global sceneIdx, effects

  time = (currentTime - startTime) * 1000

  scene = scenes[sceneIdx] if sceneIdx >= 0 else None

  if not scene:
    sceneIdx = 0
    scene = scenes[sceneIdx]
    scene.startTime = 0

    # add effects
    for sequence in scene.sequences:
      if sequence.time == 0:
        sequence.invoke()
  elif time >= scene.startTime + scene.duration:
    # remove effects
    for sequence in scene.sequences:
      if sequence.invoked:
        sequence.revoke()

    # next scene
    sceneIdx = sceneIdx+1
    if sceneIdx >= len(scenes):
      sceneIdx = sceneIdx - len(scenes)
    scene = scenes[sceneIdx]
    scene.startTime = time

    # add effects
    for sequence in scene.sequences:
      if sequence.time == 0:
        sequence.invoke()
  else:
    sceneTime = time - scene.startTime
    for sequence in scene.sequences:
      if sequence.invoked:
        if sequence.time + sequence.duration < sceneTime:
          sequence.revoke()
      else:
        if sequence.time <= sceneTime < sequence.time + sequence.duration:
          sequence.invoke()

  for effect in effects:
    effect.next()

#  sys.stdout.write("hey: ")
#  for flower in flowers:
#    for i in range(N_LIGHTS):
#      sys.stdout.write("%3d " % flower.get(i).getBrightness())
#  print ""

  payload = constructPayload(flowerRemapping)
  log("payload %s" % (payload))
  sock.send(payload)

################################################################################

if __name__ == "__main__":
  setup()

  loopDelta = 1./FPS
  startTime = currentTime = targetTime = time.time()

  while MAX_FRAMES < 0 or frameCount < MAX_FRAMES:
    previousTime, currentTime = currentTime, time.time()
    timeDelta = currentTime - previousTime

    time.sleep(random.uniform(0, loopDelta / 2.))

    loop()

    targetTime += loopDelta
    sleepTime = targetTime - time.time()
    if sleepTime > 0:
    #  print "%.5f delta %.5f" % (sleepTime, loopDelta)
      time.sleep(sleepTime)
    else:
      print 'took too long'

    frameCount = frameCount + 1

  sock.close()

