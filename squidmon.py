#!/usr/bin/python

import sys

dat = {}

def sort_by_traffic(a,b):
  return cmp(a[1],b[1])

def report():
  c = []
  totalBytes = float(0)
  totalHitBytes = float(0)
  for h in dat:
    cur = dat.get(h)
    hitBytes=cur[0]
    bytes=float(cur[1])
    if bytes>0:
      c.append([h, bytes, hitBytes/bytes*100])
    totalBytes += bytes
    totalHitBytes += hitBytes

  c=sorted(c, sort_by_traffic)
  c.reverse()
  del c[25:]

  print "cache effect: %2.2f%%, save %.2fK of %.2fK" % (totalHitBytes/totalBytes*100, totalHitBytes/1024, totalBytes/1024)
  print "most accessed sites (by traffic)"
  print "%33s %8s  %s" % ("URL", "Kbytes", "Ratio")
  for h in c:
    print "%33s %8d%7.2f" % (h[0], h[1]/1024, h[2])
  #print "\n".join(map(str, c))


def take_split(sl):
  shortURI = sl[6]
  isHit = 0
  hitBytes = 0
  bytes = int(sl[4])

  if shortURI[:7] == "http://":
    shortURI = shortURI[7:]
  elif shortURI[:6] == "ftp://":
    shortURI = shortURI[6:]
  if shortURI.find("/") != -1:
    shortURI = shortURI[:shortURI.find("/")]

  if sl[3].find("HIT") != -1 :
    ##print "hit for ", sl[6],"(",shortURI,")", bytes," bytes"
    hitBytes = bytes

  if dat.has_key(shortURI):
    cur = dat.get(shortURI)
    dat[shortURI]=[cur[0]+hitBytes, cur[1]+bytes ]
  else:
    dat[shortURI]=[hitBytes, bytes]


##                               3       4     5     6
## Timestamp Elapsed Client Action/Code Size Method URI Ident Hierarchy/From Content
def take_line(s):
  sl = s.split(" ")
  sl = [f for f in sl if len(f)>0 ]
  if len(sl) == 10:
    take_split(sl)
  else:
    print "wrong format [",s,"]"

def read_input(f):
	while True:
	  s = f.readline()
	  if not s:
		break
	  take_line(s)

if sys.stdin.isatty():
	read_input(open ("/var/log/squid3/access.log"))
else:
	read_input(sys.stdin)

report()


