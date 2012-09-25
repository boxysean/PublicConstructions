import socket
import time
import random

def circle(repeat, delay=0.01):
  for j in range(repeat):
    for i in range(255):
     s.send("000 %03d 001 %03d 002 %03d 003 %03d" % (i, (i+64)%255, (i+128)%255, (i+192)%255))
     time.sleep(delay)

def full(level, delay):
  s.send("000 %03d 001 %03d 002 %03d 003 %03d" % (level, level, level, level))
  time.sleep(delay)

def erratic(repeat):
  for q in range(repeat):
    full(255 if q % 2 else 0, random.expovariate(10.0))

if __name__ == "__main__":
  IPADDR = '192.168.2.244'
  PORTNUM = 9930

  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
  s.connect((IPADDR, PORTNUM))

  while True:
    erratic(50)
    circle(5, 0.001)

  s.close()
