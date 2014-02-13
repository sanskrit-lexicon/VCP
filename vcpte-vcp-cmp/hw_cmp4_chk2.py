"""hw_cmp4_chk2.py  Feb 8, 2014
 Checks hw_cmp4.txt for completeness of coverage of vcp

"""

import re
import sys
import codecs
import string
from levenshtein import levenshtein1,levenshtein
tranfrom="aAiIuUfFxXeEoOMHkKgGNcCjJYwWqQRtTdDnpPbBmyrlvSzsh"
tranto = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvw"
trantable = string.maketrans(tranfrom,tranto)

def extract_recs(filein):
 f = codecs.open(filein,encoding='utf-8',mode='r')
 recs=[]
 n = 0
 nok = 0
 nskip = 0
 nprob = 0
 lmin = 99999999
 lmax = -1
 for line in f:
  n = n + 1
  line = line.rstrip()
  (rec1,mtype,rec2) = re.split(r' +',line)
  if mtype == "onlyfile#1":
   nskip = nskip + 1
   continue
  rec2arr = re.split(r'[;]',rec2)
  for r2 in rec2arr:
   (key,l1str,l2str) = re.split(r'[:,]',r2)
   l1 = int(l1str)
   l2 = int(l2str)
   if l1 < lmin:
    lmin = l1
   if l2 > lmax:
    lmax = l2
   recs.append([l1,l2])
 f.close()
 print "%s lines read from %s" % (n,filein)
 print "%s lines skipped" % nskip
 print "%s line-pairs in recs" % len(recs)
 print "min l = %s, max l = %s" %(lmin,lmax)
 # discover gaps from lmin to lmax
 xlines = [False]*(lmax+1)
 for [l1,l2] in recs:
  for i in xrange(l1,l2+1):
   xlines[i]=True
 nmiss = 0
 misslines = [] 
 for i in xrange(1,len(xlines)):
  if not xlines[i]:
   misslines.append(i)
   nmiss = nmiss + 1
 print "%s lines from %s to %s of vcpte1 not covered" %(nmiss,lmin,lmax)
 misspairs = []
 curpair = None
 for i in misslines:
  if not curpair:
   curpair = [i,i]
   misspairs.append(curpair)
  elif i == (curpair[1] + 1):
   curpair[1] = (curpair[1] + 1)
  else:
   curpair = [i,i]
   misspairs.append(curpair)
 for (i1,i2) in misspairs:
  print "%s-%s missing (%s lines)" %(i1,i2,(i2-i1+1))
 return recs

def hw_cmp4_chk2(filein):
 recs = extract_recs(filein)

 return

#-----------------------------------------------------
if __name__=="__main__":
 filein=sys.argv[1] 
 #fileout =sys.argv[3]
 hw_cmp4_chk2(filein)
