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

def constructPayload(xx):
  res = "%3d " % (N_FLOWERS * N_LIGHTS)

  for i in range(N_FLOWERS * N_LIGHTS):
    res += "%3d " % (xx)

  return res

def loop():
  sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
  sock.connect((IP, PORT))

  payload = constructPayload(255)
  sock.send(payload)
  inx = raw_input("FULL POWER: Press Enter to continue...")
  payload = constructPayload(0)
  sock.send(payload)

################################################################################

if __name__ == "__main__":
  loop()
  sock.close()

