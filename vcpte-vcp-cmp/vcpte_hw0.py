"""hw0.py  ejf Feb 2, 2014  Modified Feb 11, 2014
 Read digitization vcpte.txt.
 Output all major headwords, along with the page on which the headword appear.
 Also, output the line numbers in inm.txt that pertain to the headword.
 - Page numbers are absent. W

"""
import re
import sys
import codecs
import vcpte_headword

def hw0(filein,fileout,filenote):
 f = codecs.open(filein,encoding='utf-8',mode='r')
 fout = codecs.open(fileout,'w','utf-8')
 fnote = codecs.open(filenote,'w','utf-8')
 n = 0
 page='0001-a'
 col='1'
 nb = 0 # number of left brackets
 nout = 0 # number of headword lines written to output
 rePage = re.compile(r"\[Page(.*?)]")
 reHeadword0 = vcpte_headword.reHeadword
 reHeadword = re.compile(reHeadword0)
 # for vcpte, consider end-headword also
 reHeadwordEnd0 = vcpte_headword.reHeadwordEnd
 reHeadwordEnd = re.compile(reHeadwordEnd0)
 l0=0 # first line number for a headword
 nhw=0 # same as n, but stops when the 'end' string is found
 #first line of file, not processed 
 firststring=r'<'
 firstfound=False
 endstring=r'XXXXXXXXXX'  #not really needed. file is read to end
 endfound=False
 isFirst = True
 outlines = []
 page0=0
 col0=0
 hw0=None
 hwend0 = None
 hwendFlag = False
 nnote = 0
 nprob = 0
 for line in f:
  n = n+1
  nhw = nhw + 1
  line = line.rstrip()
  m = reHeadword.search(line)
  if not m:
   if not hw0:
    continue
   m = reHeadwordEnd.search(line)
   if m:
    hwend0 = m.group(1)
    if hwend0 != hw0:
     print "At line %s, got hwend=%s, expected hw=%s" %(n,hwend0,hw0)
     print "CORRECTION:  %s:\"</%s>\"," %(n,hw0)
     nprob = nprob + 1
     if (nprob >= 5):
      print "Breaking after %s problems" % nprob
      break
    else:
     hwendFlag = True
   continue
  if m and isFirst:
   l0=nhw
   hw0 = m.group(1)
   isFirst = False
   hwendFlag = False
   continue
  if m and (not isFirst):
   # output the prior word
   l1 = l0
   l2 = nhw - 1
   out = "%s,%s:%s:%s,%s" %(page0,col0,hw0,l1,l2)
   outlines.append(out)
   #fout.write("%s\n" %(out,))
   nout = nout + 1
   # check hw0 properly ended
   if not hwendFlag:
    print "INCOMPLETE HW: %s,%s:%s:%s,%s" %(page0,col0,hw0,l1,l2)
   # the base headword. This program outputs this
   hw0 = m.group(1) 
   hwendFlag = False
   l0=nhw
   # check no ':' character in hw0. Write a message if so
   if re.search(":",hw0):
    out = "Removing from ':' to end at line %s: %s" % (n,hw0)
    fnote.write("%s\n" % out)
    nnote = nnote + 1   
    nb = nb + 1
    hw0 = re.sub(':.*$','',hw0)
 # we must now prepare the last headword
 l1 = l0
 l2 = nhw
 out = "%s,%s:%s:%s,%s" %(page0,col0,hw0,l1,l2)
 #print "%s lines read from %s" % (n,filein)
 outlines.append(out)
 nout = nout + 1
 

 #---------Output adjusted lines
 nout = 0
 for out in outlines:
  fout.write("%s\n" % out)
  nout = nout + 1
 f.close();
 fout.close();
 fnote.close()
 print "file %s has %s lines" % (filein,n)
 print "%s headwords written to file %s" % (nout,fileout)
 print "%s headwords contained a colon" % (nb,)
 if nnote > 0:
  print "wrote %s line adjustment notes to %s" % (nnote,filenote)
#-----------------------------------------------------
if __name__=="__main__":
 filein = sys.argv[1]
 fileout = sys.argv[2]
 filenote = sys.argv[3]
 hw0(filein,fileout,filenote)
