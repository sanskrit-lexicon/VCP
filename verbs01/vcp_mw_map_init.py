#-*- coding:utf-8 -*-
"""vcp_mw_map_init.py
"""
from __future__ import print_function
import sys, re,codecs

class Preverb1(object):
 def __init__(self,line):
  line = line.rstrip()
  self.line = line
  m = re.search(r'L=([^,]*), k1=([^,]*),.* mw=([^ ]*)',line)
  self.L,self.k1,self.mw = m.group(1),m.group(2),m.group(3)

 
def init_preverb1(filein):
 with codecs.open(filein,"r","utf-8") as f:
  recs = [Preverb1(x) for x in f if x.startswith(';; Case')]
 print(len(recs),"records read from",filein)
 return recs

def write(fileout,recs):
 n = 0
 # remove duplicates
 d = {}
 newrecs=[]
 for rec in recs:
  if rec.k1 in d:
   recold = d[rec.k1]
   assert rec.mw == recold.mw
  else:
   d[rec.k1] = rec
   newrecs.append(rec)

 with codecs.open(fileout,"w","utf-8") as f:
  for rec in newrecs:
   n = n + 1
   out = "%s:%s" %(rec.k1,rec.mw)
   f.write(out + '\n')
 print(n,"records written to",fileout)

if __name__=="__main__": 
 filein = sys.argv[1] #  preverb1.txt
 fileout = sys.argv[2] # vcp_mw_map_init.txt

 recs = init_preverb1(filein)
 write(fileout,recs)
