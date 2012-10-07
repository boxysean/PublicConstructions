import random
import yaml
import sys

SWEEP_TIME = 3000

FILE="../../flowers/final.conf"

flowers = yaml.load(file(FILE, "r"))["flowers"]

sequences = []

starter = range(16)
random.shuffle(starter)

startTime = 0

for j in range(8):
  time = SWEEP_TIME
  A = starter[j]
  B = starter[j]

  fadeParams = { "time": time, "flowerIdx": A, "fadeIn": time/4, "fadeOut": time/2 }
  fade = { "type": "Fade", "params": fadeParams }
  effects = [fade]
  sequence = { "time": startTime, "duration": time, "effects": effects }
  sequences.append(sequence)

  while A >= 0 or B < 16:
    A = A-1
    B = B+1

    startTime = startTime + time
    time = 2*time/3
    lights = []
    if A >= 0:
      lights.append(A)

    if B < 16:
      lights.append(B)

    fadeParams = { "time": time, "flowerIdx": lights, "fadeIn": time/4, "fadeOut": time/2 }
    fade = { "type": "Fade", "params": fadeParams }
    effects = [fade]
    sequence = { "time": startTime, "duration": time, "effects": effects }
    sequences.append(sequence)

scene = { "name": "sweep", "sequence": sequences }
doc = { "scenes": [scene] }

print yaml.dump(doc)
