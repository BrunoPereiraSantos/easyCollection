#! /usr/bin/python
from TOSSIM import *
from random import *
import time
import sys

fileName = "topo-9-default.txt"

logName = "./LOG/log-"+fileName

numNodes = int(fileName.split('-')[1])


t = Tossim([])
r = t.radio()
f = open(fileName, "r")
outFile = open(logName, "w")

for line in f:
  s = line.split()
  if len(s) > 0:
    if "gain" in s:
      print " ", s[0], " ", s[1], " ", s[2], " ", s[3]
      r.add(int(s[1]), int(s[2]), float(s[3]))
    elif "noise" in s:
      print " ", s[0], " ", s[1], " ", s[2], " ", s[3]
      #t.getNode(int(s[1])).addNoiseTraceReading(int(float(s[2])))
    #if "topo-9-default.txt" is fileName:
    else:
      print " ", s[0], " ", s[1], " ", s[2]
      r.add(int(s[0]), int(s[1]), float(s[2]))

f.close()


t.addChannel("TreeRoutingCtl", sys.stdout)
t.addChannel("TreeRouting", sys.stdout)
t.addChannel("RoutingTimer", sys.stdout)
t.addChannel("LITest", sys.stdout)
t.addChannel("EasyCollection", sys.stdout)
t.addChannel("Forwarder", sys.stdout)

t.addChannel("TreeRoutingCtl", outFile)
t.addChannel("TreeRouting", outFile)
t.addChannel("RoutingTimer", outFile)
t.addChannel("LITest", outFile)
t.addChannel("EasyCollection", outFile)
t.addChannel("StopAndWait", outFile)
t.addChannel("beacons", outFile)


noise = open("meyer-light.txt", "r")

for line in noise:
  str1 = line.strip()
  if str1:
    val = int(float(str1))
    for i in range(0, numNodes+1):
      t.getNode(i).addNoiseTraceReading(val)

for i in range(0, numNodes+1):
  print "Creating noise model for ",i;
  t.getNode(i).createNoiseModel()

noise.close()
# else:
#   for i in range(numNodes):
#     print "Creating noise model for ",i;
    #t.getNode(i).createNoiseModel()

# t.getNode(1).bootAtTime(1);
# t.getNode(2).bootAtTime(2);
# t.getNode(3).bootAtTime(3);
# t.getNode(4).bootAtTime(1050);
# t.getNode(5).bootAtTime(3050);
# t.getNode(6).bootAtTime(5050);
# t.getNode(7).bootAtTime(7050);
# t.getNode(8).bootAtTime(3550);
# t.getNode(9).bootAtTime(4450);


# t.getNode(1).bootAtTime(5);
# t.getNode(2).bootAtTime(6);
# t.getNode(3).bootAtTime(8);
# t.getNode(4).bootAtTime(7);
# t.getNode(5).bootAtTime(4);
# t.getNode(6).bootAtTime(3);
# t.getNode(7).bootAtTime(10);
# t.getNode(8).bootAtTime(3);
# t.getNode(9).bootAtTime(11);

for i in range(1, numNodes + 1):
  t.getNode(i).bootAtTime(100000 * i + randrange(10000))
#for i in range(0, numNodes):
#  t.getNode(i).bootAtTime(randrange(10))

#t.runNextEvent();

def getMinute(time, who):
  split = time.split(':')
  if who is 'h':
    return int(split[0])
  elif who is 'm':
    return int(split[1])
  elif who is 's':
    return float(split[2])
  else:
    return split


while getMinute(t.timeStr(), 's') < 50:
  t.runNextEvent()

outFile.write(t.timeStr())
outFile.write("\n")

print t.timeStr() 

sys.stderr.write("Finished!\n")
outFile.close()
 
