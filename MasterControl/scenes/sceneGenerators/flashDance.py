import random
import yaml
import sys

FILE="../../flowers/final.conf"

DELAY=2000
REPEATS=3

def dance(time, direction):
  circle1Params = { "time": 500, "trail": 2, "direction": direction, "flowerIdx": range(0,16,2), "preFade": 1, "postFade": 1 }
  circle1 = { "type": "Circle", "params": circle1Params }

  circle2Params = { "time": 500, "trail": 2, "direction": -direction, "flowerIdx": range(1,16,2) }
  circle2 = { "type": "Circle", "params": circle2Params }

  return { "time": time, "duration": 2000, "effects": [circle1, circle2] }

def flash(time, individual):
  if individual:
    glistenParams = { "time": 500, "expOn": 0.5, "expOff": 5, "lightIdx": range(64), "fadeOut": 0.5 }
  else:
    glistenParams = { "time": 500, "expOn": 0.5, "expOff": 5, "flowerIdx": range(16), "fadeOut": 0.5 }
  glisten = { "type": "Glisten", "params": glistenParams }

  return { "time": time, "duration": 2000, "effects": [glisten] }


sequences = []

startTime = 0

for i in range(REPEATS):
  sequences.append(dance(startTime, 1))
  startTime = startTime + 2000
  sequences.append(flash(startTime, False))
  startTime = startTime + 2000
  sequences.append(dance(startTime, -1))
  startTime = startTime + 2000
  sequences.append(flash(startTime, True))
  startTime = startTime + 2000
  
scene = { "name": "flashDance", "sequence": sequences }
doc = { "scenes": [scene] }

print yaml.dump(doc)
