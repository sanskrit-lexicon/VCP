""" slp1_to_wx.py
  for vcpte
"""
import sys, re
import codecs, unicodedata
import transcoder
transcoder.transcoder_set_dir("");

def adjust_slp1(x):
 # modfied to return wx
 m = re.search(r'^<(/?)(.*?)>$',x)
 if m:
  x1 = m.group(1)
  x2 = m.group(2)
  y2 =  transcoder.transcoder_processString(x2,'slp1','wx')
  ans = "<%s%s>" %(x1,y2)
  return ans
 outarr = [] # wx
 parts = re.split(r'(<[^>]+>)|(\[Page.*?\])',x) # xml tags
 for part in parts: 
  if not part: #why needed? 
   pass 
  elif part.startswith('<') and part.endswith('>'):
   outarr.append(part)
  elif part.startswith('[Page') and part.endswith(']'):
   outarr.append(part)
  else: 
   # assume text in wx. Convert to slp1. Use specialized wx_slp1.xml
   y = transcoder.transcoder_processString(part,'slp1','wx')
   outarr.append(y)
 ans = ''.join(outarr)
 return ans

def make_txt(filein,fileout):
 f = codecs.open(filein,encoding='utf-8',mode='r')
 fout = codecs.open(fileout,'w','utf-8')
 nout = 0  # count of lines written
 for line in f:
  if nout > 500000:
   print "DEBUG: stopping early"
   break
  line = line.rstrip() # some leading whitespace may have significance
  lineout = adjust_slp1(line)
  fout.write("%s\n" %lineout)
  nout = nout + 1
 f.close()
 fout.close()

if __name__=="__main__":
 filein = sys.argv[1] # vcpte1.txt (utf8, wx)
 fileout = sys.argv[2] # vcpte0_chk.txt (utf8,slp)
 make_txt(filein,fileout)
