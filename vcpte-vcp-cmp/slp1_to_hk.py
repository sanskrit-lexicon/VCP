""" slp1_to_hk.py  Jan 30, 2014
 Inverse transformation to hk_slp1.py.  Use specialized vcp version of
  slp1_hk.xml
"""
import sys, re
import codecs, unicodedata
import transcoder
transcoder.transcoder_set_dir("");

def adjust_slp1(x):
 # modfied to return both 
 outarr = [] # slp1
 parts = re.split(r'(<[^>]+>)|(\[Page.*?\])',x) # xml tags
 for part in parts: 
  if not part: #why needed? 
   pass 
  elif part.startswith('<') and part.endswith('>'):
   outarr.append(part)
  elif part.startswith('[Page') and part.endswith(']'):
   outarr.append(part)
  else: 
   # assume text in slp. Convert to slp1. Use specialized slp1_hk.xml
   y = transcoder.transcoder_processString(part,'slp1','hk')
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
  line = line.strip()
  lineout = adjust_slp1(line)
  fout.write("%s\n" %lineout)
  nout = nout + 1
 f.close()
 fout.close()

if __name__=="__main__":
 filein = sys.argv[1] # vcp_orig0.txt (utf8, hk)
 fileout = sys.argv[2] # vcp_orig1.txt (utf8,slp)
 make_txt(filein,fileout)
