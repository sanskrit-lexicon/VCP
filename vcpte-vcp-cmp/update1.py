"""update1.py
 This is a special purpose program for vcp.
 It removes some lines. Jan 30, 2014. Modified to work with utf8 files.
"""

import re,sys
import codecs, unicodedata
def update(filein,fileout,filesout1):
 # open outputs
 fout = codecs.open(fileout,'w','utf-8')
 fouts1=[]
 nout1 = []
 nouts1 = len(filesout1)
 for i in range(0,nouts1):
  fout1 = codecs.open(filesout1[i],'w','utf-8')   
  fouts1.append(fout1)
  nout1.append(0)
 # open input
 f = codecs.open(filein,encoding='utf-8',mode='r')
 # set parameters for line numbers to go to fileout1: a sequence of tuples
 # (l1,l2).  If l1 <= nin <= l2, then line goes to fileout1, otherwise it
 # goes to fileout2
 parms = [(1,2864),(412911,412950)]
 nin = 0 # number of lines read
 n = 0 # number of lines written to fileout
 for linein in f:
  nin = nin+1
  line = linein.rstrip()
  found1=False # when nin is in the parms
  for j in range(0,nouts1):
   parm = parms[j]
   (l1,l2) = parm
   if (l1 <= nin <= l2):
    i = j
    found1 = True
    break
  if found1:
   fouts1[i].write("%s\n" % line)
   nout1[i] = nout1[i] + 1
  else:
   if nin == 2865:
    lineold = line
    line = "%s%s" %(lineold, "[Page0035-a+ 30]")
    out = "change line # %s. \nold=%s\nnew=%s\n" %(nin,lineold,line)
    print out.encode('utf-8')
   fout.write("%s\n" % line)
   n = n + 1
 # close
 f.close()
 fout.close()
 for i in range(0,nouts1):
  fouts1[i].close()
 # write message
 print "%s lines read from %s" % (nin,filein)
 print "%s lines written to %s" % (n,fileout)
 for i in range(0,nouts1):
  print "%s lines written to %s" % (nout1[i],filesout1[i])
 
if __name__=="__main__":
 filein = sys.argv[1]
 fileout = sys.argv[2]
 filesout1 = [sys.argv[3],sys.argv[4]]
 update(filein,fileout,filesout1)
