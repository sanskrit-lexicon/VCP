""" cp1252_to_utf8.py
 Converts extended ascii into &#xHHHH; form
 Converts x80...x9F from cp1252 to unicode form
  
"""
import sys, re
import codecs

def make_utf8(filein,fileout):
 # slurp txt file into list of lines
 #f = open(filein,"r") # open
 f = codecs.open(filein,encoding='latin1',mode='r')
 # open output file
 fout = codecs.open(fileout,encoding='utf-8',mode='w')
 n = 0
 for line in f:
  n = n+1
  if n > 5000000:
   n = n-1
   print "debug stopping after %s lines" %n
   break
  line = line.rstrip() # remove ending whitespace
  # construct output
  data = line  # all the transformations occur via the codecs!
  out = "%s\n" % data
  fout.write( out)
  # check that out is well-formed xml
 # write closing line
 fout.close()

if __name__=="__main__":
 filein = sys.argv[1] # X.txt
 fileout = sys.argv[2] # Y.txt
 make_utf8(filein,fileout)
