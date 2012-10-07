import socket
import time
import random
import sys
import yaml
import argparse

from math import ceil

N_FLOWERS = 16
N_LIGHTS = 4
SLEEP = 250

IP = "192.168.2.103"
PORT = 9930

DEFAULT_FLOWER_FILE = "../flowers.conf"

flowerShift = [ 4, 5, 6, 7, 0, 1, 2, 3, 12, 13, 14, 15, 8, 9, 10, 11 ]
flowerRemapping = True

lightsIdx = {}
lightsRot = {}

def getFlower(i):
  if flowerRemapping:
    return flowerShift[i]
  else:
    return i

def getLight(flower, i):
  idx = lightsIdx[flower]
  rot = lightsRot[flower]

  return idx[(i+rot)%N_LIGHTS]

def constructPayload(flower, light):
  res = "%3d " % (N_FLOWERS * N_LIGHTS)

  for i in range(N_FLOWERS):
    for j in range(N_LIGHTS):
      x = 255 if flower == i and light == j else 0
      res += "%3d " % (x)

  return res

def readConf(fileName):
  f = open(fileName, "r")
  conf = yaml.load(f)
  f.close()

  idx = 0

  for flower in conf["flowers"]:
    lightsIdx[idx] = flower.get("lightsIdx", range(N_LIGHTS))
    lightsRot[idx] = flower.get("lightsRot", 0)
    idx = idx + 1

flower = 0
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
sock.connect((IP, PORT))
readConf(DEFAULT_FLOWER_FILE)

while True:
  readConf(DEFAULT_FLOWER_FILE)
  for light in range(N_LIGHTS):
    payload = constructPayload(getFlower(flower), getLight(flower, light))
    print "payload %s" % (payload)
    sock.send(payload)
    time.sleep(SLEEP/1000.0)
  inx = raw_input("Flower %d..." % (flower))
  readConf(DEFAULT_FLOWER_FILE)
  if len(inx):
    try:
      flower = int(inx)
    except:
      if inx == "n":
        flower = flower + 1
      else:
        flower = flower - 1

sock.close()

