# coding=utf-8
import sys,re,codecs
from levenshtein import *

class Vac(object):
 def __init__(self,line):
  line = line.rstrip('\r\n')
  m = re.search(r'^(.*?):(.):(  te:) (.*)$',line)
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

def te_reduce(x):
 x = re.sub(r'<page>[^<]*</page>',' ',x)
 x = re.sub(r'<column>[^<]*</column>',' ',x)
 x = re.sub(r'<[^>]*>',' ',x)
 x = re.sub(r'%','',x)
 x = re.sub(r'\([0-9]+\)',' ',x)
 x = re.sub(r' +',' ',x)
 x = x.replace(' ','')
 x = re.sub(r'[,.!+()-]','',x)
 x = x.strip()
 return x

def vcp_reduce(x):
 x = re.sub(r'<[^>]*>',' ',x)
 x = re.sub(r'{@','',x)
 x = re.sub(r'@}','',x)
 x = re.sub(r'[“”¦+]','',x)
 x = re.sub(r' *\[Page.*$','',x)
 x = re.sub(r'\([0-9]+\)',' ',x)
 x = re.sub(r' +',' ',x)
 x = re.sub(r'[,.!()-]','',x)
 x = x.strip()
 x = x.replace(' ','')
 return x

def diff(terec,vcprec):
 x = te_reduce(terec.text)
 y = vcp_reduce(vcprec.text) 
 if x == 'NA':
  d = '?'
 else:
  d = levenshtein1(x,y,9)
  if d > 9: d = 9
 if False: # debug
  print('tetext:',terec.text)
  print('vcptxt:',vcprec.text)
  print('tered :',x)
  print('vcpred:',y)
  print('d=',d)
 return d
 x1 = x.replace(' ','')
 y1 = y.replace(' ','')
 if x1 == y1:
  return 1
 nx = len(x1)
 ny = len(y1)
 if nx < ny:
  return min((ny-nx),9)
 if ny < nx:
  return min((nx-ny),9)
 if nx == ny:
  return 8


def write(fileout,terecs,vcprecs):
 assert len(terecs) == len(vcprecs)
 dbg=False
 with codecs.open(fileout,"w","utf-8") as f:
  n0 = 0
  for idx,terec in enumerate(terecs):
   if dbg and (idx == 10):  
    print('write exit at idx=',idx)
    exit(1)
   vcprec = vcprecs[idx]
   numdiff = diff(terec,vcprec)
   if numdiff == 0:
    n0  = n0 + 1
   ident = ' vcp'
   lnum = terec.lnum
   out = '%s:%s:%s: %s' %(lnum,numdiff,ident,vcprec.text)
   f.write(out+'\n')
 print(len(terecs),"records written to",fileout)
 print(n0,"records are nearly the same")
if __name__ == "__main__":
 filein1 = sys.argv[1]  # vac2.txt
 filein2 = sys.argv[2]  # vcp1a.txt
 fileout = sys.argv[3]  # vcp2a.txt
 terecs = init_vac2(filein1)
 vcprecs = init_vcp2a(filein2)
 write(fileout,terecs,vcprecs)
 
