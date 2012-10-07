import random
import yaml
import sys

FILE="../../flowers/final.conf"

DELAY=2000
REPEATS=5

sequences = []

glisten1Params = { "flowerIdx": range(16), "brightness": 128, "expOn": 20 }
glisten1 = { "type": "Glisten", "params": glisten1Params }
sequences.append({ "time": 0, "duration": 10000, "effects": [glisten1] })

glisten2Params = { "lightIdx": range(64), "brightness": 128, "expOn": 50 }
glisten2 = { "type": "Glisten", "params": glisten2Params }
sequences.append({ "time": 0, "duration": 10000, "effects": [glisten2] })
  
scene = { "name": "glisten", "sequence": sequences }
doc = { "scenes": [scene] }

print yaml.dump(doc)
