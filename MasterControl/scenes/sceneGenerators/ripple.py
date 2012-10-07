import random
import yaml
import sys

FILE="../../flowers/final.conf"

DELAY=2000
REPEATS=20

flowers = yaml.load(file(FILE, "r"))["flowers"]

minX = 10000
maxX = -10000

for flower in flowers:
  minX = min(minX, flower["x"])
  maxX = max(maxX, flower["x"])

sequences = []

startTime = 0

for j in range(REPEATS):
  for i in range(16):
    percent = (float(flowers[i]["x"]) - minX) / (maxX - minX)
  
    if percent > 0.5:
      percent = 1 - percent

    percent = 1 - percent
  
    creep = int(float(j) / REPEATS * DELAY / 2)
    creep = min(creep, DELAY/2)
    time = int((DELAY * percent) + (j * (DELAY-creep)))
    
    sys.stderr.write("j %d time %d creep %d\n" % (j, time, creep))

    fadeParams = { "time": DELAY/2, "flowerIdx": i }
    fade = { "type": "Fade", "params": fadeParams }

    effects = [fade]
    duration = DELAY/2
    sequence = { "time": time, "duration": DELAY/2, "effects": effects }

    sequences.append(sequence)

for j in range(REPEATS):
  for i in range(16):
    percent = (float(flowers[i]["x"]) - minX) / (maxX - minX)
  
    if percent > 0.5:
      percent = 1 - percent

    percent = 1 - percent
  
#    creep = int(float(j) / REPEATS * DELAY / 4)
    time = int((DELAY * percent) + (j * DELAY))
    
    sys.stderr.write("j %d time %d creep %d\n" % (j, time, creep))

    fadeParams = { "time": DELAY/2, "flowerIdx": i }
    fade = { "type": "Fade", "params": fadeParams }

    effects = [fade]
    duration = DELAY/2
    sequence = { "time": time, "duration": DELAY/2, "effects": effects }

    sequences.append(sequence)
    
scene = { "name": "ripple", "sequence": sequences }
doc = { "scenes": [scene] }

print yaml.dump(doc)
