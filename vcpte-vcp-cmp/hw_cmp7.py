"""hw_cmp5.py  Feb 8, 2014
 Compare vcphw1.txt and vcptehw1.txt - further attempts to
 optimize
 Slight revision to hw_cmp4
"""


import re
import sys
import codecs
import string
from levenshtein import levenshtein1,levenshtein

class Hwrec(object):
 def __init__(self,line,n):
  line = line.rstrip()
  (pagecol,hw,line12) = re.split(':',line)
  self.hw = hw
  (line1,line2) = re.split(r',',line12)
  lnum1=int(line1)
  lnum2=int(line2)
  self.ids = "%s:%s" %(hw,line12)
  self.used = False
  self.dup = False

def extract2_recs(filein):
 f = codecs.open(filein,encoding='utf-8',mode='r')
 recs=[]
 n = 0
 ndup = 0
 recprev = None
 for line in f:
  rec = Hwrec(line,n)
  if n == 0:
   recprev = rec
   recs.append(rec)
  elif recprev.hw == rec.hw:
   #recprev.ids = "%s;%s" % (recprev.ids,rec.ids)
   recs.append(rec)
   ndup = ndup + 1
  else:
   recprev = rec
   recs.append(rec)
  n = n + 1
 f.close()
 print "%s consecutive duplicate headwords found in %s" % (ndup,filein)
 recmap = {}
 for rec in recs:
  recmap[rec.ids] = rec 
 return (recs,recmap)

def levenshtein1b(s1,s2,dmax):
 """ like levenshtein1, except return dmax if s1 and s2 have different
   first letters
 """
 #if (len(s1)>0) and (len(s2)>0) and (s1[0] != s2[0]):
 #return dmax
 if abs(len(set(s1)) - len(set(s2))) >= dmax: #additional optimization
  return dmax
 return levenshtein1(s1,s2,max)

def init_force(fileforce):
 f = codecs.open(fileforce,encoding='utf-8',mode='r')
 force1map = {}
 force2map = {}
 for line in f:
  line = line.rstrip()
  (force1,forcetype,force2) = re.split(r' ',line)
  forcerec = (force1,forcetype,force2)
  force1keys = re.split(r';',force1)
  force2keys = re.split(r';',force2)
  for force1key in force1keys:
   if not re.search(r'MISSING',force1key):
    force1map[force1key] = forcerec
  for force2key in force2keys:
   if not re.search(r'MISSING',force2key):
    force2map[force2key] = forcerec
 f.close()
 return (force1map,force2map)


def hw_cmp7(filein1,filein2,fileforce,fileout):
 (recs1,rec1map) = extract2_recs(filein1)
 (recs2,rec2map) = extract2_recs(filein2)
 (force1map,force2map) = init_force(fileforce) 
 i1 = 0
 i2 = 0
 recs = [] # matches
 nrecs1 = len(recs1)
 nrecs2 = len(recs2)
 nprob = 0
 dmax = 3
 while (i1<nrecs1) and (i2<nrecs2):
  rec1 = recs1[i1]
  rec2 = recs2[i2]
  if rec1.used:
   i1 = i1 + 1
   continue
  if rec2.used:
   i2 = i2 + 1
   continue
  if rec1.ids in force1map:
   forcerec = force1map[rec1.ids]
   recs.append(forcerec)
   (force1idstr,forcetype,force2idstr)= forcerec
   force1ids = re.split(r';',force1idstr)
   force2ids = re.split(r';',force2idstr)
   for force1id in force1ids:
    if re.search(r'MISSING',force1id ):
     continue
    if not force1id in rec1map:
     print "force1id not in rec1map: %s " % forcerec
     exit(1)
    rec1=rec1map[force1id]
    rec1.used = True
   for force2id in force2ids:
    if re.search(r'MISSING',force2id ):
     continue
    if not force2id in rec2map:
     print "force2id not in rec2map:%s :  %s %s %s" % (force2id,force1idstr,forcetype,force2idstr)
     exit(1)
    rec2=rec2map[force2id]
    rec2.used = True
   continue
  if rec2.ids in force2map:
   forcerec = force2map[rec2.ids]
   recs.append(forcerec)
   rec2.used=True
   i2 = i2 + 1
   continue
  if rec2.hw == recs2[i2-1].hw:
   (rec1ids,eqtype,rec2ids) = recs[-1]
   rec2ids = "%s;%s" % (rec2ids,rec2.ids)
   recs[-1] = (rec1ids,eqtype,rec2ids)
   i2 = i2 + 1
   continue
  if rec1.hw == recs1[i1-1].hw:
   (rec1ids,eqtype,rec2ids) = recs[-1]
   rec1ids = "%s;%s" % (rec1ids,rec1.ids)
   recs[-1] = (rec1ids,eqtype,rec2ids)
   i1 = i1 + 1
   continue
  if rec1.hw == rec2.hw:
   recs.append((rec1.ids,'==',rec2.ids))
   rec1.used=True
   rec2.used=True
   i1 = i1 + 1
   i2 = i2 + 1
   continue
  d = levenshtein1b(rec1.hw,rec2.hw,dmax)
  if (d < dmax):
   recs.append((rec1.ids,'~=',rec2.ids))
   i1 = i1 + 1
   i2 = i2 + 1
   rec1.used=True
   rec2.used=True
   continue
  nprob = nprob + 1
  recs.append((rec1.ids,'??',rec2.ids))
  i1 = i1 + 1
  i2 = i2 + 1
  if nprob >= 5:
   print "Breaking after %s problems" % nprob
   break
 # some further adjustments
 fout = codecs.open(fileout,'w','utf-8')
 # write these 'near matches'
 dtypes = {}
 for (rec1ids,mtype,rec2ids) in recs:
  out = "%s %s %s" % (rec1ids,mtype,rec2ids)
  fout.write("%s\n" % out)
  if mtype in dtypes:
   dtypes[mtype] = dtypes[mtype] + 1
  else:
   dtypes[mtype] = 1
 # print summaries
 print "%s records read from file#1 = %s" %(len(recs1),filein1)
 print "%s records read from file#2 = %s" %(len(recs2),filein2)
 print "%s records written to %s" %(len(recs),fileout)
 for (mtype,ntype) in dtypes.iteritems():
  print "%5d matches of type %s" % (ntype,mtype)
 fout.close()
 if nprob>0:  # print last 15 records
  nrecs = len(recs)
  for i in xrange(nrecs-15,nrecs):
   (rec1ids,mtype,rec2ids) = recs[i]
   out = "%s %s %s" % (rec1ids,mtype,rec2ids)
   print out
 else:
  print "NO OPEN PROBLEMS!"
 return

#-----------------------------------------------------
if __name__=="__main__":
 filein1=sys.argv[1]  #vcpte headwords+linenums
 filein2 =sys.argv[2]  # vcp headwords+linenums
 fileforce = sys.argv[3]  #forced correspondences
 fileout =sys.argv[4]
 hw_cmp7(filein1,filein2,fileforce,fileout)
