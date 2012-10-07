import socket
import time
import random
import sys
import yaml
import argparse

from math import ceil

IP = "192.168.2.103"
PORT = 9930

N_FLOWERS = 16
N_LIGHTS = 4

flowerShift = [ 4, 5, 6, 7, 0, 1, 2, 3, 12, 13, 14, 15, 8, 9, 10, 11 ]
flowerRemapping = True

def getFlower(i):
  if flowerRemapping:
    return flowerShift[i]
  else:
    return i

def constructPayload(xx):
  res = "%3d " % (N_FLOWERS * N_LIGHTS)

  print xx

  lightIdx = xx % N_LIGHTS
  flowerIdx = getFlower(xx / N_LIGHTS)

  xx = flowerIdx * N_LIGHTS + lightIdx

  print flowerIdx, xx

  for i in range(N_FLOWERS * N_LIGHTS):
    x = 255 if i == xx else 0
    res += "%3d " % (x)

  return res

def loop():
  sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
  sock.connect((IP, PORT))

  channel = 0
  while channel < 64:
    payload = constructPayload(channel)
    print "payload %s" % (payload)
    sock.send(payload)
    inx = raw_input("Channel %d: Press Enter to continue..." % (channel))
    if len(inx):
      try:
        channel = int(inx)
      except:
        channel = channel - 1
    else:
      channel = channel + 1

################################################################################

if __name__ == "__main__":
  loop()
  sock.close()

