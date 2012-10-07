import random
import yaml

TIME=3000

specialFlower = range(16)
random.shuffle(specialFlower)
flowers = range(16)

sequences = []

for i in range(16):
  idx = specialFlower[i]

  if idx != 0:
    glisten1Params = { "time": TIME, "flowerIdx": i, "brightness": 192 }
    glisten1 = { "type": "Glisten", "params": glisten1Params }
    glisten1Sequence = { "time": 0, "duration": TIME*idx, "effects": [glisten1] }
    sequences.append(glisten1Sequence)

  circleParams = { "time": TIME/3, "flowerIdx": i }
  circle = { "type": "Circle", "params": circleParams }
  circleSequence = { "time": TIME*idx, "duration": TIME, "effects": [circle] }
  sequences.append(circleSequence)

  if idx != 15:
    glisten2Params = { "time": TIME, "flowerIdx": i, "brightness": 192 }
    glisten2 = { "type": "Glisten", "params": glisten2Params }
    glisten2Sequence = { "time": TIME*(idx+1), "duration": TIME*(16-idx), "effects": [glisten2] }
    sequences.append(glisten2Sequence)

scene = { "name": "magic", "sequence": sequences }
doc = { "scenes": [scene] }

print yaml.dump(doc)
