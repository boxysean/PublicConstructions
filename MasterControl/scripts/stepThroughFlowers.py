import socket
import time
import random
import sys
import yaml
import argparse

from math import ceil

N_FLOWERS = 16
N_LIGHTS = 4

#IP = "127.0.0.1"
IP = "192.168.2.103"
PORT = 9930

flowerShift = [ 4, 5, 6, 7, 0, 1, 2, 3, 12, 13, 14, 15, 8, 9, 10, 11 ]
flowerRemapping = True

def getFlower(i):
  if flowerRemapping:
    return flowerShift[i]
  else:
    return i

def constructPayload(xx):
  res = "%3d " % (N_FLOWERS * N_LIGHTS)

  for i in range(N_FLOWERS):
    for j in range(N_LIGHTS):
      x = 255 if i == xx else 0
      res += "%3d " % (x)

  return res


flower = 0
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
sock.connect((IP, PORT))

for i in range(16):
  payload = constructPayload(getFlower(flower))
  print "payload %s" % (payload)
  sock.send(payload)
  inx = raw_input("Channel %d: Press Enter to continue..." % (flower))
  if len(inx):
    try:
      flower = int(inx)
    except:
      flower = flower - 1
  else:
    flower = flower + 1

sock.close()

