# coding=utf-8
import sys,re,codecs
#from levenshtein import *

class Vac(object):
 def __init__(self,line):
  line = line.rstrip('\r\n')
  m = re.search(r'^(.*?):(.):(  te:) (.*)$',line)
  self.lnum = m.group(1)
  self.numdiff = m.group(2)
  self.ident = m.group(3)
  self.text = m.group(4)
  self.line = line
  
def init_vac2(filein):
 recs = []
 with codecs.open(filein,"r","utf-8") as f:
  for line in f:
   recs.append(Vac(line))
 print(len(recs),"records from",filein)
 return recs

class VCP2(object):
 def __init__(self,line):
  self.line = line.rstrip('\r\n')
  m = re.search(r'^(.*?):(.):( vcp:) (.*)$',self.line)
  self.lnum = m.group(1)
  self.numdiff = m.group(2)
  self.ident = m.group(3)
  self.text = m.group(4)
  #m = re.search(r'^(.*?):(.):(  te: )(.*)$',line)
 def vcp2_vcp(self):
  # convert text to form appearing in vcp.txt
  # This undoes make_vcp1a.py
  line = self.text
  line = re.sub(r' \[Page.*$','',line)
  line = re.sub(r'<HI>{@(.*?)@}',r'\1',line)
  return line
 
def init_vcp2a(filein):
 recs = []
 with codecs.open(filein,"r","utf-8") as f:
  for line in f:
   recs.append(VCP2(line))
 print(len(recs),"records from",filein)
 return recs

def init_map(filein):
 recs = []
 with codecs.open(filein,"r","utf-8") as f:
  for iline,line in enumerate(f):
   line = line.rstrip('\r\n')
   n1str,n2str = line.split(' ')
   n1 = int(n1str)
   n2 = int(n2str)
   assert n1 == (iline + 1)
   recs.append(n2)
 print(len(recs),"records from",filein)
 return recs
 
def unused_te_reduce(x):
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

def unused_vcp_reduce(x):
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


def write(fileout,filter_data,vcprecs,terecs,vcp2a_vcp_map):
 dbg=False
 with codecs.open(fileout,"w","utf-8") as f:
  n1mult = 0
  n2mult = 0
  n0 = 0
  for _idx,_temp in enumerate(filter_data):
   idx,probs = _temp
   if dbg and (_idx == 10):  
    print('write exit at _idx=',_idx)
    break
   vcprec = vcprecs[idx]
   line = vcprec.vcp2_vcp()
   lnum = vcp2a_vcp_map[idx]
   outarr = []
   outarr.append(';')
   # E -> ai and O -> au
   n1 = len(re.findall(r'[E]',line))
   n2 = len(re.findall(r'[O]',line))
   n = n1 + n2
   if n == 0:
    outarr.append('; Problem: no E or O in line')
    n0 = n0 + 1
   if (n1 > 1) and ('ai' in probs):
    outarr.append('; Problem: multiple changes of E to ai')
    n1mult = n1mult + 1
   if (n2 > 1) and ('au' in probs):
    outarr.append('; multiple changes of O to au')
    n2mult = n2mult + 1
   probstr = ','.join(probs)
   outarr.append('; (%s) %s' % (probstr,terecs[idx].line))
   newline = line
   if 'ai' in probs:
    newline = newline.replace('E','ai')
   if 'au' in probs:
    newline = newline.replace('O','au')
   outarr.append('%s old %s' %(lnum,line))
   outarr.append('%s new %s' %(lnum,newline))
   for out in outarr:
    f.write(out+'\n')
 print(len(filter_data),'change records written to',fileout)
 print(n1mult,'cases with multiple E->ai')
 print(n2mult,'cases with multiple O->au')
 print(n0,'cases with no E or O')
 
def filter_hiatus(terecs):
 ans = []
 for idx,te in enumerate(terecs):
  a = []
  if ('ai' in te.text):
   a.append('ai')
  if ('au' in te.text):
   a.append('au')
  if len(a) != 0:
   ans.append((idx,a))
 print("filter_hiatus found",len(ans),"cases")
 return ans

if __name__ == "__main__":
 filein1 = sys.argv[1]  # vac2.txt
 filein2 = sys.argv[2]  # vcp1a.txt
 filein3 = sys.argv[3]  # temp_vcp2a_map.txt
 fileout = sys.argv[4]  # vcp2a.txt
 terecs = init_vac2(filein1)
 vcprecs = init_vcp2a(filein2)
 vcp2a_vcp_map = init_map(filein3)
 
 filter = filter_hiatus(terecs)
 write(fileout,filter,vcprecs,terecs,vcp2a_vcp_map)
 
