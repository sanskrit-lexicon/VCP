""" check_ea.py (generic) For vac_input.txt
"""

import re,sys
as_max = 10
import vac_headword
reHeadword = vac_headword.reHeadword

class As(object):
 def __init__(self,key,m):
  self.key = key
  self.m = m
  self.n = 0
  self.instances = [] # only m of these
 def update(self,instance):
  if (self.n < self.m):
   self.instances.append(instance)
  self.n = self.n + 1
def convert(s):
 """ convert a string, changing extended ascii characters
 """
 out=[]
 for c in s:
  ic = ord(c)
  if (ic > 127):
   #h = "0x%0.2X" % ic
   h = "<x%0.2X/>" % ic
  else:
   h = c
  out.append(h)
 ans = ''.join(out)
 return ans
def check_as(filein,fileout):
# set up regex callback 'repl' with access to dictionary asdict
 asdict = {}
 as_instance = ''
 def repl(m):
  x = m.group(0)
  if (x in asdict):
   asobj = asdict[x]
  else:
   asobj = As(x,as_max)
   asdict[x] = asobj
  asobj.update(as_instance)
  
 # read the lines of the file
 f = open(filein,'r')
 n = 0
 last_page = 'Page0-0'
 last_hw = 'NO HW'
 for line in f:
  line = line.rstrip()
  n = n + 1
  m = re.search(r'\[(Page.*?)\]',line)
  if m:
   last_page = m.group(1)
  m = re.search(reHeadword,line)  
  if m:
   last_hw = m.group(1)
  #line = re.sub(r'\[Page.*?\]','',line)  # to avoid the e1,etc of Page
  nstr = "%s" % n
  #line_utf8 = line.decode("iso-8859-1").encode("utf-8")
  #as_instance = (last_page,last_hw,nstr,line_utf8)
  as_instance = (last_page,last_hw,nstr,line)
  line = re.sub(r'[^\x00-\x7F]',repl,line)
 f.close()
 #write asdict to fileout
 fout = open(fileout,'w')
 #import codecs
 #fout = codecs.open(fileout,'w','utf-8')
 keys = asdict.keys()
 #keys = sorted(keys,cmp=lambda x,y: cmp(x.lower(),y.lower()))
 keys = sorted(keys)
 # generate outs_uncommon and outs_common arrays of lines to output
 m = as_max
 nkey = 0
 outlines_common = []
 outlines_uncommon = []
 # put everything in 'common'
 for key in keys:
  nkey = nkey + 1
  asobj = asdict[key]
  outlines = []  # the lines for this key
  key1=convert(key)
  outlines.append("%s (%s) %s  STATUS: " %(key,key1,asobj.n))
  for as_instance in asobj.instances:
   outlines.append(' :: '.join(as_instance))
  if (asobj.n < m):
   outlines_common.append(outlines)
  else:
   outlines_common.append(outlines)
 # write header 
 fout.write("input file = %s\n" % filein)
 fout.write("*******************************\n")
 fout.write("%s  'AS' codes follow, with instances\n" % len(outlines_common))
 fout.write("Each instances shows: page,headword,line number in %s\n" % filein)
 fout.write("*******************************\n")
 k = 0
 for outlines in outlines_common:
  k = k + 1
  fout.write("# %s --------------------------------------------------\n" % k);
  j = 0
  for out in outlines:
   j = j + 1
   #out=convert(out)
   #out = out.decode("iso-8859-1").encode("utf-8")
   #out = out.encode("utf-8")
   fout.write("%s\n" % out)
   #if (j > 1):
    #fout.write("ejf: \n")
    #fout.write("tm: \n")
    #fout.write(".....\n")
 # write common cases  
 fout.write("*******************************\n")
 """ commented out
 fout.write("PART 2 of 2\n")
 fout.write("%s common 'AS' codes follow, with instances\n" % len(outlines_common))
 fout.write("Each instances shows: page,headword,line number in %s\n" % filein)
 fout.write("*******************************\n")
 k = 0
 for outlines in outlines_common:
  k = k + 1
  fout.write("# %s --------------------------------------------------\n" % k);
  j = 0
  for out in outlines:
   out = convert(out)
   j = j + 1
   #if (j == 1):
    #fout.write("ejf: \n")
    #fout.write("tm: \n")
   fout.write("%s\n" % out)
 """
 fout.close()
#-----------------------------------------------------
if __name__=="__main__":
 filein = sys.argv[1]
 fileout = sys.argv[2]
 check_as(filein,fileout)
