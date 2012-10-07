import random
import yaml
import sys

FILE="../../flowers/final.conf"

flowers = yaml.load(file(FILE, "r"))["flowers"]

minX = 10000
maxX = -10000

for flower in flowers:
  minX = min(minX, flower["x"])
  maxX = max(maxX, flower["x"])

BPM=80
DELAY=int(1000/(BPM/60.0))

def full(time, duration, value, flowerIdx=range(16)):
  fullParams = { "flowerIdx": flowerIdx, "value": value }
  full = { "type": "Full", "params": fullParams }
  return { "time": time, "duration": duration, "effects": [full] }

def fade(time, duration, flowerIdx=range(16), delay=DELAY*2, brightness=255):
  fadeParams = { "time": delay, "flowerIdx": flowerIdx, "brightness": brightness, "delayBetweenTime": delay }
  fade = { "type": "Fade", "params": fadeParams }
  return { "time": time, "duration": duration, "effects": [fade] }

def dance(time, direction, duration):
  circle1Params = { "time": DELAY, "trail": 2, "direction": direction, "flowerIdx": range(0,16,2), "preFade": 1, "postFade": 1 }
  circle1 = { "type": "Circle", "params": circle1Params }

  circle2Params = { "time": DELAY, "trail": 2, "direction": -direction, "flowerIdx": range(1,16,2) }
  circle2 = { "type": "Circle", "params": circle2Params }

  return { "time": time, "duration": duration, "effects": [circle1, circle2] }

def circles(time, duration, flowerIdx=range(16), speed=DELAY, trail=2, direction=1):
  circle1Params = { "time": speed, "trail": trail, "direction": direction, "flowerIdx": flowerIdx }
  circle1 = { "type": "Circle", "params": circle1Params }

  return { "time": time, "duration": duration, "effects": [circle1] }

def flash(time, individual, duration):
  if individual:
    glistenParams = { "time": DELAY, "expOn": 0.2, "expOff": 10, "lightIdx": range(64), "fadeOut": 0.5, "brightness": 255 }
  else:
    glistenParams = { "time": DELAY, "expOn": 0.2, "expOff": 10, "flowerIdx": range(16), "fadeOut": 0.5, "brightness": 255 }
  glisten = { "type": "Glisten", "params": glistenParams }

  return { "time": time, "duration": duration, "effects": [glisten] }

def ripple(sequences, repeats, startTime):
  res = 0

  for j in range(repeats):
    for i in range(16):
      percent = (float(flowers[i]["x"]) - minX) / (maxX - minX)
    
      if percent > 0.5:
        percent = (1 - percent) * 2
      else:
        percent = percent * 2
  
      percent = 1 - percent
    
      time = startTime + int((DELAY * percent) + (j * DELAY))
      res = max(time+DELAY/2, res)
      
#      sys.stderr.write("j %d time %d\n" % (j, time))
  
      fadeParams = { "time": DELAY/2, "flowerIdx": i }
      fade = { "type": "Fade", "params": fadeParams }
  
      effects = [fade]
      duration = DELAY/2
      sequence = { "time": time, "duration": DELAY/2, "effects": effects }
  
      sequences.append(sequence)

  return res

def sweep(sequences, duration, direction=1):
  res = 0

  for i in range(16):
    percent = (float(flowers[i]["x"]) - minX) / (maxX - minX)
    if direction == -1:
      percent = 1.0 - percent

    time = startTime + int(duration * percent)
    res = max(res, time+duration/4)
  
    fadeParams = { "time": int(duration/4), "flowerIdx": i }
    fade = { "type": "Fade", "params": fadeParams }

    sequence = { "time": time, "duration": duration/4, "effects": [fade] }
  
    sequences.append(sequence)

  return res

sequences = []

startTime = 0

# start sequence

for i in range(8):
  sequences.append(full(startTime, DELAY/4, 255))
  startTime = startTime + DELAY/4
  sequences.append(full(startTime, DELAY/4, 0))
  startTime = startTime + DELAY/4

full(startTime, DELAY*2, 0)
startTime = startTime + DELAY*2

# just fades

duration = DELAY*8
sequences.append(fade(startTime, duration))
startTime = startTime + duration
 
# magic

START = startTime
duration = DELAY*8
sequences.append(dance(startTime, 1, duration))
startTime = startTime + duration
sequences.append(flash(startTime, False, duration))
startTime = startTime + duration

sequences.append(fade(START, startTime-START, brightness=255))

# ripple

START = startTime
startTime = ripple(sequences, 40, startTime)

sequences.append(fade(START, startTime-START, range(8)))
sequences.append(fade(START+DELAY+DELAY, startTime-START, range(8, 16)))

# magic

START = startTime
duration = DELAY*8
sequences.append(dance(startTime, 1, duration))
startTime = startTime + duration
sequences.append(flash(startTime, False, duration))
startTime = startTime + duration

sequences.append(fade(START, startTime-START, brightness=255))

# boom

boomRanges = [range(16), range(0, 16, 2), range(1, 16, 2), range(16)]
fadeRanges = [[], range(1, 16, 2), range(0, 16, 2), range(16)]

for i in range(4):
  boomRange = boomRanges[i]
  fadeRange = fadeRanges[i]
  sys.stderr.write(str(boomRange) + "\n")
  START = startTime
  sequences.append(full(startTime, DELAY/2, 255, boomRange))
  startTime = startTime + DELAY/2
  sequences.append(full(startTime, DELAY/2, 0, boomRange))
  startTime = startTime + DELAY/2
  sequences.append(full(startTime, DELAY/4, 255, boomRange))
  startTime = startTime + DELAY/4
  sequences.append(full(startTime, DELAY/4, 0, boomRange))
  startTime = startTime + DELAY/4
  sequences.append(full(startTime, DELAY/8, 255, boomRange))
  startTime = startTime + DELAY/8
  sequences.append(full(startTime, DELAY/4, 0, boomRange))
  startTime = startTime + DELAY/4
  sequences.append(full(startTime, DELAY/8, 255, boomRange))
  startTime = startTime + DELAY/8
  sequences.append(full(startTime, DELAY/4, 0, boomRange))
  startTime = startTime + DELAY/4
  sequences.append(full(startTime, DELAY/2, 255, boomRange))
  startTime = startTime + DELAY/2
  sequences.append(full(startTime, DELAY, 0, boomRange))
  startTime = startTime + DELAY
  if len(fadeRange):
    sequences.append(fade(START, startTime-START, fadeRange))

# sweeps

START = startTime
startTime = sweep(sequences, DELAY*4, 1)
startTime = sweep(sequences, DELAY*4, -1)
startTime = sweep(sequences, DELAY*2, 1)
startTime = sweep(sequences, DELAY*4, -1)
startTime = sweep(sequences, DELAY*2, 1)
startTime = sweep(sequences, DELAY*2, -1)
startTime = sweep(sequences, DELAY*4, 1)
startTime = sweep(sequences, DELAY*2, -1)
startTime = sweep(sequences, DELAY*2, 1)
startTime = sweep(sequences, DELAY*1, -1)
startTime = sweep(sequences, DELAY*1, 1)
startTime = sweep(sequences, DELAY*2, -1)
startTime = sweep(sequences, DELAY*2, 1)
startTime = sweep(sequences, DELAY*1, -1)
startTime = sweep(sequences, DELAY*1, 1)
startTime = sweep(sequences, DELAY*1, -1)
startTime = sweep(sequences, DELAY*1, 1)
startTime = sweep(sequences, DELAY*2, -1)
startTime = sweep(sequences, DELAY*2, 1)
startTime = sweep(sequences, DELAY*1, -1)
startTime = sweep(sequences, DELAY*1, 1)

sequences.append(fade(START, startTime-START, brightness=255, delay=DELAY*4))

# circles man

START = startTime

duration = DELAY*4
sequences.append(circles(startTime, duration, range(0,16,2), direction=1, speed=DELAY*2))
sequences.append(full(startTime, duration, 255, range(1,16,2)))
startTime = startTime + duration

duration = DELAY*4
sequences.append(circles(startTime, duration, range(1,16,2), direction=-1, speed=DELAY))
sequences.append(full(startTime, duration, 255, range(0,16,2)))
startTime = startTime + duration

duration = DELAY*4
sequences.append(circles(startTime, duration, range(0,16,2), direction=1, speed=DELAY*2, trail=3))
sequences.append(full(startTime, duration, 255, range(1,16,2)))
startTime = startTime + duration

duration = DELAY*4
sequences.append(circles(startTime, duration, range(1,16,2), direction=-1, speed=DELAY, trail=3))
sequences.append(full(startTime, duration, 255, range(0,16,2)))
startTime = startTime + duration

duration = DELAY*4
sequences.append(circles(startTime, duration, range(0,16,2), direction=-1, speed=DELAY, trail=0.5))
sequences.append(full(startTime, duration, 255, range(1,16,2)))
startTime = startTime + duration

duration = DELAY*4
sequences.append(circles(startTime, duration, range(1,16,2), direction=1, speed=DELAY*2, trail=0.5))
sequences.append(full(startTime, duration, 255, range(0,16,2)))
startTime = startTime + duration

duration = DELAY*4
sequences.append(circles(startTime, duration, range(0,16,2), direction=-1, speed=DELAY, trail=2))
sequences.append(full(startTime, duration, 255, range(1,16,2)))
startTime = startTime + duration

duration = DELAY*4
sequences.append(circles(startTime, duration, range(1,16,2), direction=1, speed=DELAY*0.75, trail=2))
sequences.append(full(startTime, duration, 255, range(0,16,2)))
startTime = startTime + duration

duration = DELAY*4
sequences.append(circles(startTime, duration, range(0,16,2), direction=-1, speed=DELAY * 0.7, trail=2))
sequences.append(full(startTime, duration, 255, range(1,16,2)))
startTime = startTime + duration

duration = DELAY*4
sequences.append(circles(startTime, duration, range(1,16,2), direction=1, speed=DELAY*0.65, trail=2))
sequences.append(full(startTime, duration, 255, range(0,16,2)))
startTime = startTime + duration

duration = DELAY*4
sequences.append(circles(startTime, duration, range(0,16,2), direction=-1, speed=DELAY * 0.6, trail=2))
sequences.append(full(startTime, duration, 255, range(1,16,2)))
startTime = startTime + duration

duration = DELAY*4
sequences.append(circles(startTime, duration, range(1,16,2), direction=1, speed=DELAY*0.55, trail=2))
sequences.append(full(startTime, duration, 255, range(0,16,2)))
startTime = startTime + duration

duration = DELAY*4
sequences.append(circles(startTime, duration, range(0,16,2), direction=-1, speed=DELAY * 0.4, trail=1))
sequences.append(full(startTime, duration, 255, range(1,16,2)))
startTime = startTime + duration

duration = DELAY*4
sequences.append(circles(startTime, duration, range(1,16,2), direction=1, speed=DELAY*0.35, trail=1))
sequences.append(full(startTime, duration, 255, range(0,16,2)))
startTime = startTime + duration

duration = DELAY*8
sequences.append(circles(startTime, duration, range(0,16,2), direction=-1, speed=DELAY * 0.25, trail=1))
sequences.append(full(startTime, duration, 255, range(1,16,2)))
startTime = startTime + duration

duration = DELAY*8
sequences.append(circles(startTime, duration, range(1,16,2), direction=1, speed=DELAY*0.25, trail=1))
sequences.append(full(startTime, duration, 255, range(0,16,2)))
startTime = startTime + duration

# end sequence TODO
 
scene = { "name": "best", "sequence": sequences }
doc = { "scenes": [scene] }

print yaml.dump(doc)
