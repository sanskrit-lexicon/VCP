""" wx_to_slp1.py
 
"""
import sys, re
import codecs, unicodedata
import transcoder
transcoder.transcoder_set_dir("");

def adjust_wx(x):
 # modfied to return both slp1 
 # headword entries start with a <wx-headword> line and
 # end with a </wx-headword> line.
 # convert these to <slp-headword> 
 # and </slp-headword>
 m = re.search(r'^<(/?)(.*?)>$',x)
 if m:
  x1 = m.group(1)
  x2 = m.group(2)
  y2 =  transcoder.transcoder_processString(x2,'wx','slp1')
  ans = "<%s%s>" %(x1,y2)
  return ans
 # presumably, not a headword. Don't transcode xml tags
 outarr = [] # slp1
 parts = re.split(r'(<[^>]+>)',x) # xml tags
 for part in parts: 
  if not part: #why needed? 
   pass 
  elif part.startswith('<') and part.endswith('>'):
   outarr.append(part)
  elif part.startswith('[Page') and part.endswith(']'):
   outarr.append(part)
  else: 
   # assume text in wx. Convert to slp1. Use specialized wx_slp1.xml
   y = transcoder.transcoder_processString(part,'wx','slp1')
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
  # headword xmls are
  lineout = adjust_wx(line)
  fout.write("%s\n" %lineout)
  nout = nout + 1
 f.close()
 fout.close()

if __name__=="__main__":
 filein = sys.argv[1] # vcpte0.txt (utf8, wx)
 fileout = sys.argv[2] # vcpte1.txt (utf8,slp)
 make_txt(filein,fileout)
