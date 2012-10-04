import socket
import time
import random
import sys
import yaml
import argparse

from math import ceil

IP = "127.0.0.1"
PORT = 9930

N_FLOWERS = 16
N_LIGHTS = 4

def constructPayload(xx):
  res = "%3d " % (N_FLOWERS * N_LIGHTS)

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
      channel = int(inx)
    else:
      channel = channel + 1

################################################################################

if __name__ == "__main__":
  loop()
  sock.close()

