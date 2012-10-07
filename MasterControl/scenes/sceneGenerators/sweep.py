import random
import yaml
import sys

FILE="../../flowers/final.conf"
ADD=200

flowers = yaml.load(file(FILE, "r"))["flowers"]

minX = 10000
maxX = -10000

for flower in flowers:
  minX = min(minX, flower["x"])
  maxX = max(maxX, flower["x"])

minX = minX - ADD
maxX = maxX + ADD

sequences = []

startTime = 0

for j in range(16):
  SWEEP_TIME = random.expovariate(2.0) * 4000
  sys.stderr.write("%d\n" % SWEEP_TIME)
  for i in range(16):
    percent = (float(flowers[i]["x"]) - minX) / (maxX - minX)
    if (j & 1) == 0:
      percent = 1.0 - percent

    time = startTime + int(SWEEP_TIME * percent)
  
    fadeParams = { "time": int(SWEEP_TIME/5), "flowerIdx": i }
    fade = { "type": "Fade", "params": fadeParams }
  
    effects = [fade]
    sequence = { "time": time, "duration": int(SWEEP_TIME/5), "effects": effects }
  
    sequences.append(sequence)

  startTime = startTime + SWEEP_TIME
  
scene = { "name": "sweep", "sequence": sequences }
doc = { "scenes": [scene] }

print yaml.dump(doc)
