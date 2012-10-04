import socket
import time
import random
import sys
import yaml
import argparse

from math import ceil

N_FLOWERS = 16
N_LIGHTS = 4

def constructPayload(xx):
  res = "%3d " % (N_FLOWERS * N_LIGHTS)

  for i in range(N_FLOWERS):
    for j in range(N_LIGHTS):
      x = 255 if i == xx else 0
      res += "%3d " % (x)

  return res


channel = 0
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
sock.connect(("192.168.2.103", 9930))

for i in range(16):
  payload = constructPayload(channel)
  print "payload %s" % (payload)
  sock.send(payload)
  raw_input("Channel %d: Press Enter to continue..." % (channel))
  channel = channel + 1

sock.close()

