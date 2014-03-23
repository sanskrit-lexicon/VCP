# coding=utf-8
""" len1.py  Feb 21, 2014
    Compare the 'squashed' length of corresponding sections of
    vcpte and vac.
"""
import re
import sys
import codecs
class Token(object):
 def __init__(self,i1,i2,markup,s):
  self.i1 = i1
  self.i2 = i2
  self.type = markup
  self.string = s

class Vcpte(object):
 #baseregex = r'([ `#.+!_,"\t%-]+)|(<.*?>)|(\([0-9]+\))'
 baseregex = r'([0-9 ~`#.+!_,"\t%-]+)|(<.*?>)|(\([0-9]+\))'
 regex = re.compile(baseregex)
 regex1 = re.compile("^%s$" % baseregex)

class Vcp(object):
 #baseregex = u'([ .+!_,“”¦*{@@}-]+)|(\[Page.*?\])|(<.*?>)|({[?][?]})|(\([0-9]+\))'
 baseregex = u'(\[Page.*?\])|([0-9 ~.+!_,“”¦*{@@}-]+)|(<.*?>)|({[?][?]})|(\([0-9]+\))'
 regex = re.compile(baseregex)
 regex1 = re.compile("^%s$" % baseregex)

class Vac(object):
 baseregex = r'(^.*?\t[0-9]+\t)|([0-9 .+!_,*%-]+)|(<page>.*?</page>)|(<column>.*?</column>)|(<.*?>)|(\([0-9]+\))'
 baseregex = r'(^.*?\t[0-9]+\t)|([0-9 .+!_,*%-]+)|(<page>.*?</page>)|(<column>.*?</column>)|(<.*?>)|(\([0-9]+\))'
 regex = re.compile(baseregex)
 regex1 = re.compile("^%s$" % baseregex)

def squash(regex,regex1,line):
 splits = re.split(regex,line)
 tokens = []
 i2 = -1
 squashlist = []
 for split in splits:
  if not split: # Sometimes, None is one of the splits
   continue
  i1 = i2 + 1
  i2 = i1 + len(split)
  if re.match(regex1,split):
   markup = True
  else:
   markup = False
   squashlist.append(split)
  token = Token(i1,i2,markup,split)
  tokens.append(token)
 line1 = ''.join(squashlist)
 return (tokens,line1)

class Hw_chunk(object):
 def __init__(self,data):
  # data = x:l1,l2
  (x,l1str,l2str) = re.split(r'[:,]',data)
  self.hw = x
  self.l1 = int(l1str)
  self.l2 = int(l2str)
  self.missing = False
  if self.l1 == -1:
   self.missing = True
  self.len = -1
  self.squashlen = -1
  self.squashline=''

class Hw_cmp(object):
 def __init__(self,line):
  line = line.rstrip()
  (cmp1,cmptype,cmp2) = re.split(r' ',line)
  self.line = line
  cmprec = (cmp1,cmptype,cmp2)
  cmp1keys = re.split(r';',cmp1)
  cmp2keys = re.split(r';',cmp2)
  self.chunks1 = [Hw_chunk(x) for x in cmp1keys]
  self.chunks2 = [Hw_chunk(x) for x in cmp2keys]
  self.len1 = 0
  self.squashlen1 = 0
  self.len2 = 0
  self.squashlen2 = 0
  self.pctdiff = 0
  self.missing = False
  for chunk in self.chunks1:
   if chunk.missing:
     self.missing = True
  for chunk in self.chunks2:
   if chunk.missing:
     self.missing = True

def init_cmp(filecmp):
 f = codecs.open(filecmp,encoding='utf-8',mode='r')
# recs = [Hw_cmp(line) for line in f]
 recs=[]
 n = 0
 for line in f:
  n = n + 1
  try:
   rec = Hw_cmp(line)
  except:
   print "ERROR(init_cmp) at line#",n
   print line.encode('utf-8')
   exit(1)
  recs.append(rec)
 f.close()
 return recs

def init_digitization(filein):
 f = codecs.open(filein,encoding='utf-8',mode='r')
 recs = [line.rstrip() for line in f]
 f.close()
 return recs

def update_chunks(chunks,recs,regex,regex1):
 for chunk in chunks:
  if chunk.missing:
   continue
  try:
   lines = recs[chunk.l1-1:chunk.l2]
  except:
   print "ERROR: update_chunks: l1,l2 = ",chunk.l1,chunk.l2
   exit(1)
  lentot = 0
  squashlentot = 0
  squashlines=[]
  for line in lines:
   lentot = lentot + len(line)
   (tokens,line1) = squash(regex,regex1,line)
   squashlines.append(line1)
   squashlentot = squashlentot + len(line1)
  chunk.len = lentot
  chunk.squashlen = squashlentot
  chunk.squashline = ''.join(squashlines)

def calc_ipctdiff(i,j):
 """ i,j integers """
 if (i==-1) or (j==-1):
  return -1
 if (i == 0) or (j == 0):
  return 0
 x = float(i)
 y = float(j)
 a = (x+y)/2.0
 d = 100.0*(abs(x-y)/a)
 return int(d)
def calc_ipctdiff_simplediff(i,j):
 """ i,j integers """
 if (i==-1) or (j==-1):
  return 0
 if (i == 0) or (j == 0):
  return 0
 d = (i-j)
 #x = float(i)
 #y = float(j)
 #a = (x+y)/2.0
 #d = 100.0*(abs(x-y)/a)
 return int(d)

def len1(filein1,filein2,filecmp,fileout):
 cmprecs = init_cmp(filecmp)
 recs1 = init_digitization(filein1)
 recs2 = init_digitization(filein2)
 mcmp = 1000 # for debug
 mcmp = 1000000 # for production
 ncmp = 0
 for cmprec in cmprecs:
  update_chunks(cmprec.chunks1,recs1,Vcpte.regex,Vcpte.regex1)
  cmprec.len1 = sum([chunk.len for chunk in cmprec.chunks1])
  cmprec.squashlen1 = sum([chunk.squashlen for chunk in cmprec.chunks1])
  cmprec.squashline1 = ''.join([chunk.squashline for chunk in cmprec.chunks1])

  update_chunks(cmprec.chunks2,recs2,Vac.regex,Vac.regex1)
  cmprec.len2 = sum([chunk.len for chunk in cmprec.chunks2])
  cmprec.squashlen2 = sum([chunk.squashlen for chunk in cmprec.chunks2])
  cmprec.squashline2 = ''.join([chunk.squashline for chunk in cmprec.chunks2])
  #print "vac squashline for record",(ncmp+1)
  #print cmprec.squashline2,"\n"
  cmprec.pctdiff = calc_ipctdiff_simplediff(cmprec.squashlen1,cmprec.squashlen2)
   
  ncmp = ncmp + 1
  if ncmp >= mcmp:
   break
 fout = codecs.open(fileout,'w','utf-8')
 ncmp = 0
 nsame = 0
 nmiss = 0
 for cmprec in cmprecs:
  if cmprec.missing:
   diff = "   NA"
   nmiss = nmiss + 1
  elif cmprec.squashline1 == cmprec.squashline2:
   diff = "   EQ"
   nsame = nsame + 1
  else:
   diff = "%5d" % cmprec.pctdiff
  out = "%5d %5d %5d %5d %s %s" %(cmprec.len1,cmprec.len2,cmprec.squashlen1,
         cmprec.squashlen2,diff,cmprec.line)
  fout.write("%s\n" % out)
  ncmp = ncmp + 1
  if ncmp >= mcmp:
   break
 print "# of hw matches = ",ncmp
 print "# of these missing vcpte or vac data = ",nmiss
 print "# of these with identical squashlines = ",nsame
 fout.close()
 
#-----------------------------------------------------
if __name__=="__main__":
 filein1 =sys.argv[1]  # vcpte
 filein2 =sys.argv[2]  # vac
 filecmp = sys.argv[3]  #hwcmp
 fileout =sys.argv[4]
 len1(filein1,filein2,filecmp,fileout)
