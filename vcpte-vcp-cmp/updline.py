"""updline.py  ejf Feb 11, 2014  
 Modify an input file based on a transaction file of line-replacements.
 Replace the lines of the input file according to the transactions, and
 write the output.
 Also, write a 'log' file documenting all replacements.
 All files assumed to be utf-8 format.
 The transaction file is a file of lines, each with the format
 linenum<space>[replacement line], where
 linenum is a digit-string representing the number (starting at 1) of
          a line in the input file
 <space> is a (single) space character
 [replacement line] is the 'new value' to which the given line of input
          is to be changed.

"""
import re
import sys
import codecs

def init_transactions(filetran):
 f = codecs.open(filetran,encoding='utf-8',mode='r')
 d = {} # returned dictionary
 n = 0
 for line in f:
  n = n+1
  line = line.rstrip('\n\r')
  m = re.search(r'^([0-9]+) (.*)$',line)
  if not m:
   out =  "Error in %s at line # %s:\n%s" %(filetran,n,line)
   print out.encode('utf-8')
   exit(1)
  lnum = int(m.group(1))
  newline = m.group(2)
  d[lnum] = newline
 f.close()
 return d

def updline(filein,filetran,fileout,filenote):
 f = codecs.open(filein,encoding='utf-8',mode='r')
 fout = codecs.open(fileout,'w','utf-8')
 fnote = codecs.open(filenote,'w','utf-8')
 transactions = init_transactions(filetran)
 n = 0
 nout = 0
 nnote = 0
 nprob = 0
 for line in f:
  n = n+1
  line = line.rstrip()
  if n in transactions:
   line1 = transactions[n]
  else:
   line1 = line
  fout.write("%s\n" % line1)
  nout = nout + 1
  if (line1 != line):
   out = "line %s\nold=%s\nnew=%s\n" %(n,line,line1)
   fnote.write("%s\n" % out)
   nnote = nnote + 1
 f.close()
 fnote.close()
 fout.close()
 print "file %s has %s lines" % (filein,n)
 print "%s lines to file %s" % (nout,fileout)
 print "wrote %s line adjustment notes to %s" % (nnote,filenote)
#-----------------------------------------------------
if __name__=="__main__":
 filein = sys.argv[1]
 filetran = sys.argv[2]
 fileout = sys.argv[3]
 filenote = sys.argv[4]
 updline(filein,filetran,fileout,filenote)
