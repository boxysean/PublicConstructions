import random
import yaml
import sys

FILE="../../flowers/final.conf"

DELAY=2000
REPEATS=10

top = range(0, 64, 4) + range(3, 64, 4)
top = sorted(top)

bottom = range(1, 64, 4) + range(2, 64, 4)
bottom = sorted(bottom)

def bullet(time, idx):
  fadeParams = { "time": 200, "lightIdx": idx }
  fade = { "type": "Fade", "params": fadeParams }
  return { "time": time, "duration": 200, "effects": [fade] }

def shoot(time, thetop, direction, speed):
  res = []
  idxs = range(32)
  if direction == -1:
    idxs.reverse()
  for idx, i in enumerate(idxs):
    res.append(bullet(time+(idx*speed), top[i] if thetop else bottom[i]))
  return res

sequences = []

startTime = 0

for i in range(REPEATS):
  for x in shoot(startTime, random.choice([True, False]), 1, random.randint(25, 125)):
    sequences.append(x)

  startTime = startTime + random.randint(250, 1000)

  for x in shoot(startTime, random.choice([False, True]), -1, random.randint(25, 125)):
    sequences.append(x)

  startTime = startTime + random.randint(250, 1000)
 
scene = { "name": "shoot", "sequence": sequences }
doc = { "scenes": [scene] }

print yaml.dump(doc)
