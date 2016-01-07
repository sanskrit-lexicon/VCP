"""hw1.py  ejf Oct 1,2013 for vcp
 Usage - python hw1.py vcphw0.txt vcphw1_dhaval.txt vcphw1_dhaval_note.txt 
 Read  hw0.txt, whose lines were created with:
 out = "%s:%s:%s,%s" %(page,hw,l1,l2)

 'Normalize' all headword spellings, but still leave in HK.
 Then output the same format, using the normalized headword
 Here are the normalizations:
 - Change 'D.' to 'D'
 - Remove parenthetical parts (these represent alternate spellings)
 - Remove {??}  (unreadable text)
 - Remove space
 - Remove ' (avagraha)
 - Remove trailing ',' or '-'
 - Change ira--IrSAyAM to ira
 Jan 30, 2014 read/write utf-8. 
 Nov 20, 2014.  Manually adjust some 'UrdD' headwords
"""
import re
import sys
import codecs
hw_override = {'UrdDa(rdDva)':'UrdDva',
  'UrdDa(rdDva)kaca':'UrdDvakaca',
  'UrdDa(rdDva)kaRWa':'UrdDvakaRWa',
  'UrdDa(rdDva)karmman':'UrdDvakarmman',
  'UrdDa(rdDva)manTin':'UrdDvamanTin',
  'UrdDa(rdDva)mAna':'UrdDvamAna',
  'UrdDa(dDva)ka':'UrdDvaka',
  'kuve(be)ra':'kubera',
  'Karva(rba)':'Karba',
  'navava(ba)DU':'navabaDU' ,
  'purU(ru)ravasa':'puru(rU)ravasa',
  'pUrRakU(ku)wa':'pUrRaku(kU)wa'
  }
def hw_normalize(hw):
 hw0 = hw
 if hw in hw_override:
  print "Note: %s -> %s" %(hw,hw_override[hw])
  hw = hw_override[hw]
 hw = re.sub(r"[*]","",hw) # special nukta coding
 hw = re.sub(r"\(.*?\)","",hw)
 hw = re.sub(r"{[?][?]}","",hw)
 hw = re.sub(r" ","",hw)
 hw = re.sub(r"'","",hw)
 hw = re.sub(r"[,]$","",hw)
 hw = re.sub(r"[-]+$","",hw)
 hw = re.sub(r"ira--IrzAyAM","ira",hw)
 #hw = re.sub(r"M~","M",hw) # candra-bindu changed to M
 #hw = re.sub(r"[^a-z0-9]$","",hw)
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
