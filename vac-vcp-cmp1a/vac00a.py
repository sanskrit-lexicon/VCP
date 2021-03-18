# coding=utf-8
import sys,re,codecs
from levenshtein import *

class Vac(object):
 def __init__(self,line):
  line = line.rstrip('\r\n')
  self.line = line
  m = re.search(r'^(.*?):(.):(  te): (.*)$',line)
  self.lnum = m.group(1)
  self.numdiff = m.group(2)
  self.ident = m.group(3)
  self.text = m.group(4)

def init_vac2(filein):
 recs = []
 with codecs.open(filein,"r","utf-8") as f:
  for line in f:
   recs.append(Vac(line))
 print(len(recs),"records from",filein)
 return recs

class VCP2(object):
 def __init__(self,line):
  line = line.rstrip('\r\n')
  #m = re.search(r'^(.*?):(.):(  te: )(.*)$',line)
  self.text = line

def init_vcp2a(filein):
 recs = []
 with codecs.open(filein,"r","utf-8") as f:
  for line in f:
   recs.append(VCP2(line))
 print(len(recs),"records from",filein)
 return recs

def write(fileout,filelog,terecs,vcprecs):
 assert len(terecs) == len(vcprecs)
 dbg=False
 flog = codecs.open(filelog,"w","utf-8")
 mt = 0 # max length of te lines
 mv = 0 # max length of vcp lines
 nt300 = 0  # number of te lines of length >= 300
 with codecs.open(fileout,"w","utf-8") as f:
  n0 = 0
  for idx,terec in enumerate(terecs):
   if dbg and (idx == 10):  
    print('write exit at idx=',idx)
    exit(1)
   vcprec = vcprecs[idx]
   ident = terec.ident
   numdiff = terec.numdiff
   lnum = terec.lnum
   lt = len(terec.text)
   if (vcprec.text == '<Picture>') or (lt >= 300):
    n0 = n0 + 1
    flog.write(terec.line+'\n')
    out = '%s:%s:%s: %s' %(lnum,numdiff,' vcp',vcprec.text)
    flog.write(out+'\n')
    flog.write(';' + '\n')
    terec.text = '?'
   out = '%s:%s:%s: %s' %(lnum,numdiff,ident,terec.text)
   f.write(out+'\n')
   if lt > mt:
    mt = lt
   if lt >= 300:
    nt300 = nt300 + 1
   #if l > 1000:
   # print(lnum,l)
   lv = len(vcprec.text)
   if lv > mv:
    mv = lv
 print(len(terecs),"records written to",fileout)
 flog.close()
 print(n0,"records written to",filelog)
 print(mt,"is max length of lines in TE")
 print(mv,"is max length of lines in VCP")
 print(nt300,"TE lines of length 300 or more")
 
if __name__ == "__main__":
 filein1 = sys.argv[1]  # vac2.txt
 filein2 = sys.argv[2]  # vcp1a.txt
 fileout = sys.argv[3]  # vac2a.txt
 filelog = sys.argv[4]  # vac2a_picturedata.txt
 terecs = init_vac2(filein1)
 vcprecs = init_vcp2a(filein2)
 write(fileout,filelog,terecs,vcprecs)
 
