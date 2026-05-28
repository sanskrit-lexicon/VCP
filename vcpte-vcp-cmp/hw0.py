"""hw0.py  ejf Jan 7, 2014  
 Read digitization vcp.txt.
 Output all major headwords, along with the page on which the headword appear.
 Also, output the line numbers in inm.txt that pertain to the headword.
 - Page numbers are 
[Pagepppp-c+ n]
where
  pppp is 4-digit page number (pagination starts anew for each volume)
  c = column. (a or b)
n is a 2-digit number of lines in next column
There are three pages (which start with tables) of form
 [Pagepppp+ n]

 - Headwords are as in headword.py
   X is coded in HK encoding 
   It is checked that 'X' contains no colon character.
 - line numbers l1,l2 are the first line number and last line number of 
   vcp.txt that pertain to the headword.  
  
 The output is written as  (note: 'page' is pppp,c)
   page:headword:line1,line2
 Jan 31, 2014: read/write utf8
"""
import re
import sys
import codecs
def hw0(filein,fileout):
 f = codecs.open(filein,encoding='utf-8',mode='r')
 fout = codecs.open(fileout,'w','utf-8')
 n = 0
 page='0001-a'
 col='1'
 nb = 0 # number of left brackets
 nout = 0 # number of headword lines written to output
 rePage = re.compile(r"\[Page(.*?)]")
 import headword
 reHeadword0 = headword.reHeadword
 reHeadword = re.compile(reHeadword0)
 l0=0 # first line number for a headword
 nhw=0 # same as n, but stops when the 'end' string is found
 #first line of file, not processed 
 firststring=r'[Page0035-a+ 30]'
 firstfound=False
 endstring=r'XXXXXXXXXX'  #not really needed. file is read to end
 endfound=False
 isFirst = False
 outlines = []
 for line in f:
  n = n+1
  if (line.find(endstring) >= 0): 
   endfound=True
  nhw = nhw + 1
  if (line.find(firststring) >= 0): 
   print "found firststring: %s" % firststring
   firstfound=True
   # DO process this line (to get line number)
   isFirst = False 
   print "found firststring"
  # the placement of m=.. before if(not firstfound) is important detail
  m = reHeadword.search(line)
  if (not firstfound):
   continue
  if m and (not isFirst):
   # found next headword
   if (l0 != 0):
    # output the prior word
    l1 = l0
    l2 = nhw - 1
    out = "%s,%s:%s:%s,%s" %(page0,col0,hw0,l1,l2)
    outlines.append(out)
    #fout.write("%s\n" %(out,))
    nout = nout + 1
   # the base headword. This program outputs this
   hw00 = m.group(1) 
   hw0 = hw00
   # update page0,  l0 
   col0 = col
   page0 = page
   l0=nhw
   if re.search(":",hw0):
    print "Removing from ':' to end at line %s: %s" % (n,hw0)
    nb = nb + 1
    hw0 = re.sub(':.*$','',hw0)
  # step 3, search for page
  isFirst = False # required for first word handling
  pages = rePage.findall(line)
  if len(pages) > 0:
   pagelast = pages[-1]
   m = re.match(r'^([0-9]+)-([ab])[+]',pagelast)
   m1 = re.match(r'^([0-9]+)[+]',pagelast)
   if m:
    page = m.group(1) # vol-ppp
    col = m.group(2) # may be blank. Just skip this?
   elif m1:
    page = m1.group(1)
    col = ''
  if endfound:
   break
 # we must now prepare the last headword
 l1 = l0
 l2 = nhw
 out = "%s,%s:%s:%s,%s" %(page0,col0,hw0,l1,l2)
 
 outlines.append(out)
 nout = nout + 1
 
 # remove non-dictionary end-of-volume lines
 outlines1 = []
 for i in xrange(0,nout):
  j = i + 1
  if False: # skip this adjustment logic 
   if (3844 <= j) and (j <= 3906):
    continue
   if (1875 <= j) and (j <= 1884):
    continue
  outlines1.append(outlines[i])
 
 #---------Output adjusted lines
 nout = 0
 for out in outlines1:
  fout.write("%s\n" %(out,))
  nout = nout + 1
 f.close();
 fout.close();
 print "file %s has %s lines" % (filein,n)
 print "%s headwords written to file %s" % (nout,fileout)
 print "%s headwords contained a colon" % (nb,)
#-----------------------------------------------------
if __name__=="__main__":
 filein = sys.argv[1]
 fileout = sys.argv[2]
 hw0(filein,fileout)
