import socket
import time
import random
import sys
import yaml
import argparse

from math import ceil

N_FLOWERS = 16
N_LIGHTS = 4

IP = "127.0.0.1"
PORT = 9930

def constructPayload(xx):
  res = "%3d " % (N_FLOWERS * N_LIGHTS)

  for i in range(N_FLOWERS):
    for j in range(N_LIGHTS):
      x = 255 if i == xx else 0
      res += "%3d " % (x)

  return res


channel = 0
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
sock.connect((IP, PORT))

for i in range(16):
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

sock.close()

