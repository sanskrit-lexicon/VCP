"""hw1.py  ejf Feb 2, 2014 for vcpte
 Read  hw0.txt, whose lines were created with:
 out = "%s:%s:%s,%s" %(page,hw,l1,l2)
 Jan 30, 2014 read/write utf-8. 

 'Normalize' all headword spellings, but still leave in HK.
 Then output the same format, using the normalized headword
 Here are the normalizations:
 - Remove '.'
 - Remove parenthetical parts (these represent alternate spellings)
 - Remove single quote "'" (avagraha)
 - Remove '_'
 - Remove '>' to eol (probable coding errors)
 - Remove '<'  (a typo @ <<pArSvaparivarttana>
 - Remove ~  (one)
 - Remove '(' ')' to end  
 - Remove space
"""
import re
import sys
import codecs
def hw_normalize(hw):
 hw0 = hw 
 hw = re.sub(r"[.]","",hw) 
 hw = re.sub(r"\(.*?\)","",hw) # parenthetical
 hw = re.sub(r"'","",hw)
 hw = re.sub(r" ","",hw)
 hw = re.sub(r"[_~]","",hw)
 hw = re.sub(r"<","",hw)
 hw = re.sub(r"[()].*$","",hw)
 m = re.search(r'([^a-zA-Z])',hw)
 if m:
  c = m.group(1)
  cint = ord(c)
  out = "headword '%s' (%s) has unexpected character '%s' = %s" %(hw,hw0,c,cint)
  print out.encode('utf-8')
 return hw
def hw1(filein,fileout,filenote):
 f = codecs.open(filein,encoding='utf-8',mode='r')
 fout = codecs.open(fileout,'w','utf-8')
 fnote = codecs.open(filenote,'w','utf-8')
 n = 0
 nnote = 0
 nout = 0 # number of headword lines written to output
 for line in f:
  n = n+1
  line = line.strip() # remove starting or ending whitespace
  (pagecol,hw0,line12) = re.split(':',line)
 
  hw = hw_normalize(hw0)
  out = "%s:%s:%s" %(pagecol,hw,line12)
  fout.write("%s\n" % out);
  nout = nout + 1
  if ((hw != hw0) and ((hw+"-")!=hw0)):
   out = "%s:  '%s' => '%s'  :%s" %(pagecol,hw0,hw,line12)
   fnote.write("%s\n" % out);
   nnote = nnote + 1
 f.close()
 fout.close()
 fnote.close()
 print "file %s has %s lines" % (filein,n)
 print "%s headwords written to file %s" % (nout,fileout)
 print "%s headwords with normalization changes written to %s" % (nnote,filenote)
#-----------------------------------------------------
if __name__=="__main__":
 filein=sys.argv[1] 
 fileout =sys.argv[2] 
 filenote =sys.argv[3]
 hw1(filein,fileout,filenote)
