# coding=utf-8
""" match1c.py
 In this variant, the ORIGINAL lines of vac are broken, based upon the
 squashed lines.
 match1b:
  Joins all the lines of vac into one block. Then does match with
  vcp lines.

  Interactive usage:
>>> import match1b # first time
>>> reload(match1b) # subsequently
>>> cmprecs = match1b.init_cmp()
>>> terecs=match1b.init_digitization("vac1.txt")
>>> vcprecs=match1b.init_digitization("vcp1.txt")
>>> match1b.match1_lnum_print(104526,terecs,vcprecs,cmprecs=cmprecs,matchonly=False)
"""

import codecs,re,sys
from levenshtein import *

class Token(object):
 def __init__(self,i1,i2,markup,s,j1,j2):
  self.i1 = i1
  self.i2 = i2
  self.type = markup
  self.string = s
  self.j1 = j1
  self.j2 = j2

def squash(regex,regex1,line):
 # Feb 15. Special logic for adding a space, or other text
 line = re.sub(r'<add>(.*?)</add>',r"\1",line)
 line = re.sub(r'<drop>(.*?)</drop>',r"",line)
 # Feb 24, after 11% done. added 'dup'. Functionally like drop,
 # But it indicates that this is a duplicate of a preceding section.
 # This is a common occurrence in Tirupati edition.
 line = re.sub(r'<dup>(.*?)</dup>',r"",line) 
 # Feb 24. Introduce a form for a change, where old text is in an
 # attribute.  The old text should have no '<>'. 
 # <chg old="x">y</chg>  is equivalent to <drop>x</drop><add>y</add>,
 # but more expressive for simple changes.
 line = re.sub(r'<chg old=[^<>]*?>(.*?)</chg>',r"\1",line)
 splits = re.split(regex,line)
 tokens = []
 # For each token, token.string = line[i1:i2]
 # 
 i2 = -1  
 j1 = -1
 j2 = -1
 squashlist = []
 for split in splits:
  if not split: # Sometimes, None is one of the splits
   continue
  if split == '':  # may be caught by previous, not sure
   continue
  i1 = i2 + 1
  i2 = i1 + len(split)
  if re.match(regex1,split):
   markup = True
   k1 = None
   k2 = None
  else:
   markup = False
   squashlist.append(split)
   j1 = j2 + 1
   j2 = j2 + len(split)
   k1 = j1
   k2 = j2
  token = Token(i1,i2,markup,split,k1,k2)
  tokens.append(token)
 line1 = ''.join(squashlist)
 return (tokens,line1)

def te_squash(line):
 """ remove 'insignificant' characters from a string line
 """
 return squash(Vac.regex,Vac.regex1,line)

class Vac(object):
 #baseregex = r'(^.*?\t[0-9]+\t)|(\([0-9/ ,]+\))|([0-9 .+!_,*%/`-]+)|(<page>.*?</page>)|(<column>.*?</column>)|(<.*?>)'
 baseregex = r'(<lb/>.*?\t[0-9]+\t)|(^.*?\t[0-9]+\t)|(\([0-9/ ,]+\))|([0-9 .+!_,*%/`{}-]+)|(<page>.*?</page>)|(<column>.*?</column>)|(<.*?>)'
 regex = re.compile(baseregex)
 regex1 = re.compile("^%s$" % baseregex)
 def __init__(self,line,idx):
  line = line.rstrip('\n\r')
  self.line = line
  if re.search(r'^</?[^>]*?>$',line):
   self.hwtag = True
   #print "Vac hw: %s" % line
  else:
   self.hwtag=False
  self.lineadjust = line
  self.i1 = 0
  self.i2 = 0
  (self.tokens,self.squash) = te_squash(self.lineadjust)
  self.squashlen = len(self.squash)

def vcp_squash(line):
 """ remove 'insignificant' characters from a string line
 """
 return squash(Vcp.regex,Vcp.regex1,line)

class Vcp(object):
 baseregex = u'(\[Page.*?\])|(\([0-9/ ,]+\))|([0-9 ~.+!_,“”’‘¦*{@@}/-]+)|(<.*?>)|({[?][?]})'
 regex = re.compile(baseregex)
 regex1 = re.compile("^%s$" % baseregex)
 def __init__(self,line,lnum):
  line = line.rstrip('\n\r')
  self.line = line
  self.lnum = lnum
  if re.search(r'^<HI>',line):
   self.hwtag = True
  else:
   self.hwtag=False
  #lineadjust = re.sub(r'^<.*?>','',line) # remove initial
  #lineadjust = re.sub(u'[“”]','"',lineadjust) # normal quotes
  #if self.hwtag:
  # lineadjust = re.sub(u'¦','',lineadjust)
  # lineadjust = re.sub(r'^{@(.*?)@}','%\g<1>%',lineadjust) 
  self.lineadjust = line
  (self.tokens,self.squash) = vcp_squash(self.lineadjust)
  self.squashlen = len(self.squash)
  if re.search(r'Page1298b',self.squash): # dbg
   out = [(t.type,t.string) for t in self.tokens]
   print "dbg VCP: ",out

def dist(a,b):
 # distance between 2 numbers
 return abs(a-b)

def end_block(i2,te,txt2):
 """ te is a  vac record. Assume this corresponds, for some i3, to
   the subsequence txt2[i2:i3+1] of txt2.
   Maybe can find i3 just by looking at (possibly adjusted) text lengths
 """
 n1tot= te.squashlen
 # n2tots is list of pairs (j2,n2tot), where
 # j2 is an index into txt2 and
 # n2tot is cumulative length(txt[i2]+...txt[j2])
 n2tots = [] 
 n2tot = 0
 j2 = i2
 ntxt2 = len(txt2)
 while j2 < ntxt2:
  n2 = txt2[j2].squashlen
  n2tot = n2tot + n2
  n2tots.append((j2,n2tot))
  if n2tot < n1tot: 
   # keep going, unless txt2 is depleted
   if (j2+1) < ntxt2:
    j2 = j2 + 1
    continue
   # otherwise, break loop, without incrementing j2
   break
  # Now, n2tot >= n1tot
  break
 # Decide what subscript into txt2 to return
 if n2tot < n1tot:
  # not enought txt2.
  # so j2+1 = ntxt2, and we must use j2
  return j2
 (j2b,n2btot) = n2tots[-1] # last element of n2tots
 # If there was only 1 element of n2tots, use it
 if len(n2tots) == 1:
  return j2b
 (j2a,n2atot) = n2tots[-2]
 # Pick between j2a and j2b according to which corresponding
 # n2atot and n2btot is closest to n1tot. If a tie, go with j2a.
 if dist(n1tot,n2atot) <= dist(n1tot,n2btot):
  return j2a
 return j2b

def te_findlines(txt1,txt2):
 """ txt1 is a sequence of Vac objects
     txt2 is a sequence of Vcp objects
     To each element te of txt1, if te is not marked as hwtag, then
     set te.i1 and te.i2; so that
     te corresponds to the slice txt2[te.i1,te.i2+1]

 """
 i2 = 0 # current index in txt2
 for i1 in xrange(0,len(txt1)):
  te = txt1[i1]
  if te.squashlen == 0:
   continue  # Feb 14
  if te.hwtag:
   continue # nothing to adjust
  # assume each other line of txt1 corresponds to a sequence of lines of txt2
  i3 = end_block(i2,te,txt2)
  te.i1 = i2
  te.i2 = i3
  if (i3+1)<len(txt2):
   i2 = i3+1
  else:
   i2 = i3

def best_end_match1(s1,s2,k):
 """ returns False or a pair that partitions s2 """
 n1 = len(s1)
 n2 = len(s2)
 if k > n1:
  return False
 t1 = s1[-k:] # last k chars of s1
 mmax = n1 + 5
 ioffsets = []
 kbeg=0
 while True:
  ioffset = s2.find(t1,kbeg)
  if ioffset == -1:
   break
  m = ioffset+k
  if m > mmax:
   return False
  ioffsets.append(ioffset)
  if m > n1: 
   break
  kbeg = m
 if len(ioffsets) == 0:
  return False
 j2 = ioffsets[-1] # last
 m2 = j2+k
 a2 = s2[0:m2]
 b2 = s2[m2:]
 if len(ioffsets) == 1:
  return (a2,b2)
 j1 = ioffsets[-2] # penultimate
 m1 = j1+k
 a1 = s2[0:m1]
 b1 = s2[m1:]
 #print "n1,s1=",n1,s1
 d1=dist(n1,m1)
 #print "m1,a1,d1=",m1,a1,d1
 d2=dist(n1,m2)
 #print "m2,a2,d2=",m2,a2,d2

 if d1 <= d2:
  return (a1,b1)
 return (a2,b2)

def best_initial_match1(s1,s1next,s2,k):
 """ returns False or a pair that partitions s2 """
 n1 = len(s1)
 n2 = len(s2)
 n1next = len(s1next)
 if k > n1next:
  return False
 t1 = s1next[0:k] # first k chars of s1
 mmax = n1 + 5
 ioffsets = []
 kbeg=0
 while True:
  ioffset = s2.find(t1,kbeg)
  if ioffset == -1:
   break
  m = ioffset
  if m > mmax:
   return False
  ioffsets.append(ioffset)
  if len(ioffsets) >= 10:
   print "ERROR best_initial_match1",offsets
   exit(1)
  if m > n1-5: 
   break
  kbeg = m+1
 if len(ioffsets) == 0:
  return False
 j2 = ioffsets[-1] # last
 m2 = j2
 a2 = s2[0:m2]
 b2 = s2[m2:]
 if len(ioffsets) == 1:
  return (a2,b2)
 j1 = ioffsets[-2] # penultimate
 m1 = j1
 a1 = s2[0:m1]
 b1 = s2[m1:]
 #print "n1,s1=",n1,s1
 d1=dist(n1,m1)
 #print "m1,a1,d1=",m1,a1,d1
 d2=dist(n1,m2)
 #print "m2,a2,d2=",m2,a2,d2

 if d1 <= d2:
  return (a1,b1)
 return (a2,b2)

def unused_te_partition(te,txt2):
 """ partition te.squash to match corresponding txt2 lines
 """
 parts = []
 curte=te.squash
 for i in xrange(te.i1,te.i2+1):
  t = txt2[i].squash
  (a,b) = best_initial_match(t,curte)
  parts.append(a)
  curte = b
 return parts

def best_initial_match(s1,s1next,s2):
 """ s1 should be the initial part of s2. However, due to minor differences,
     we may say that the partition (a,b) of s2 is the best match of a to s1
 """
 n1 = len(s1)
 n2 = len(s2)
 if n2 == 0:  # Mar 14, 2014
  return ('','')
 if s2.startswith(s1):
  a = s1
  if s1 == s2:
   b=''
  else:
   b = s2[n1:]
  return (a,b)
 if n1 >= n2:
  #a = s1
  a = s1[0:n2] # Mar 14, 2014
  b = ''
  return (a,b)
 # As default, use a segment of 
 k = 5
 # Look for a match on the 'END' 
 while (k > 1): 
  maybe = best_end_match1(s1,s2,k)
  if maybe:
   break
  k = k - 1
 if maybe:
  (a,b) = maybe
  return (a,b)
 # look for beginning of s1next
 k = 5
 if not s1next:
  k = 0
  maybe=False
 while (k > 1): 
  maybe = best_initial_match1(s1,s1next,s2,k)
  if maybe:
   break
  k = k - 1
 if maybe:
  (a,b) = maybe
  return (a,b)
 # no luck. just partition by number of characters 
 a = s2[0:n1]
 b = s2[n1:]
 return (a,b)

class Calc(object):
 def __init__(self,t,d,s1,te):
  self.t = t
  self.d = d
  self.s1 = s1
  self.te = te # a Vac object

def match1_calc(te,txt2):
 # compute teparts
 teparts = []
 # curte is the remaining part of the squashed te string. 
 # initially, it is the whole string.
 curte=te.squash 
 ntxt2 = len(txt2)
 for i in xrange(0,ntxt2):
  t = txt2[i].squash
  if (i+1)<ntxt2:
   tnext = txt2[i+1].squash
  else:
   tnext = None
  (a,b) = best_initial_match(t,tnext,curte)
  teparts.append(a)
  curte = b
 # Mar 15, 2014.  Typically, curte should be the empty string.
 # But, It is possible that curte is not empty.  In any case,
 # append curte to the last teparts
 teparts[ntxt2-1] = "%s%s" % (teparts[ntxt2-1],curte)
 ntot = 0
 totarr = []
 #j = 0 # index into teparts
 outarr = [] # array of Calc records, one for each tepart
 dtot = 0
 for i in xrange(0,ntxt2):
  t = txt2[i]
  s2 = t.squash
  #s1 = teparts[j]
  s1 = teparts[i]
  d = levenshtein(s1,s2)
  dtot = dtot + d
  totarr.append(s2)
  outarr.append(Calc(t,d,s1,te))
  #j = j + 1
 return outarr

def match1_calc0(recs1,l1a,l1b,recs2,l2a,l2b):
 lines1 = [line for line in recs1[l1a-1:l1b]]
 line1 = '<lb/>'.join(lines1)
 te = Vac(line1,0)
 txt2 = []
 l2 = l2a
 for line in recs2[l2a-1:l2b]:
  txt2.append(Vcp(line,l2))
  l2 = l2 + 1
 return match1_calc(te,txt2) 

def match1_print(recs1,l1a,l1b,recs2,l2a,l2b):
 calcarr = match1_calc0(recs1,l1a,l1b,recs2,l2a,l2b)
 outarr=[]
 out = "teparts length = " % len(calcarr)
 outarr.append(out)
 dtot = sum([calcrec.d for calcrec in calcarr])
 for calcrec in calcarr:
  t = calcrec.t
  d = calcrec.d
  s1 = calcrec.s1
  s2 = t.squash
  out = "vcp line# %s, d=%s" %(t.lnum,d)
  outarr.append(out)
  out = "  vcp: %s" % s2
  outarr.append(out)
  out = "   te: %s" % s1
  outarr.append(out)
  outarr.append("")
 out = "Total Levenshtein distance: %s" %dtot
 outarr.append(out)
 out = '\n'.join(outarr)
 print "%s\n\n" % out.encode('utf-8')


def init_digitization(filein):
 f = codecs.open(filein,encoding='utf-8',mode='r')
 recs = [line.rstrip() for line in f]
 f.close()
 return recs

def init_recs():
 filein1 = "vac2.txt"
 filein2 = "vcp0.txt"
 recs1 = init_digitization(filein1)
 recs2 = init_digitization(filein2)
 return (recs1,recs2)

class Hw_chunk(object):
 def __init__(self,data):
  # data = x:l1,l2
  (x,l1str,l2str) = re.split(r'[:,]',data)
  self.hw = x
  self.l1 = int(l1str)
  self.l2 = int(l2str)
  self.missing = False
  if self.l1 == -1:
   self.missing = True
  self.len = -1
  self.squashlen = -1

class Hw_cmp(object):
 def __init__(self,line):
  line = line.rstrip()
  (cmp1,cmptype,cmp2) = re.split(r' ',line)
  self.line = line
  cmprec = (cmp1,cmptype,cmp2)
  cmp1keys = re.split(r';',cmp1)
  cmp2keys = re.split(r';',cmp2)
  self.chunks1 = [Hw_chunk(x) for x in cmp1keys]
  self.chunks2 = [Hw_chunk(x) for x in cmp2keys]
  self.len1 = 0
  self.squashlen1 = 0
  self.len2 = 0
  self.squashlen2 = 0
  self.pctdiff = 0

def init_cmp():
 filecmp = "hwcmpvcp1.txt"
 f = codecs.open(filecmp,encoding='utf-8',mode='r')
 recs = [Hw_cmp(line) for line in f]
 f.close()
 return recs

def find_cmp_vcp(lnum,cmprecs):
 for cmprec in cmprecs:
  chunks2 = cmprec.chunks2
  for chunk in chunks2:
   if chunk.missing:
    continue
   if (chunk.l1 <= lnum) and (lnum <= chunk.l2):
    return cmprec
 return None

def cmp_missing(cmprec):
 for chunk1 in cmprec.chunks1:
  if chunk1.missing:
   return True
 for chunk2 in cmprec.chunks2:
  if chunk2.missing:
   return True
 return False

def match1_lnum(lnum,recs1,recs2,cmprecs=None):
 if not cmprecs:
  cmprecs = init_cmp()
 cmprec = find_cmp_vcp(lnum,cmprecs)
 if not cmprec:
  #print "match1_lnum fails. Could not file cmprec for lnum=",lnum
  #print "cmprecs # entries = ",len(cmprecs)
  return None
 if cmp_missing(cmprec):
  #print "match1_lnum: Missing data\n",cmprec.line
  return None
 lines1 = []
 for chunk1 in cmprec.chunks1:
  for l in xrange(chunk1.l1-1,chunk1.l2):
   lines1.append(recs1[l])
 line1 = '<lb/>'.join(lines1)
 te = Vac(line1,0)

 txt2 = []
 for chunk2 in cmprec.chunks2:
  for l in xrange(chunk2.l1-1,chunk2.l2):
   line = recs2[l]
   lnum = l + 1
   txt2.append(Vcp(line,lnum))
 calcarr = match1_calc(te,txt2)
 return (cmprec.line,calcarr)

def match1_lnum_print(lnum,recs1,recs2,cmprecs=None,matchonly=False):
 result = match1_lnum(lnum,recs1,recs2,cmprecs);
 if not result:
  print "match1_lnum_print: No data"
  return
 (matchline,calcarr) = result
 match = False
 dmax=9 # a tunable parameter
 chkdiff=0
 mchkdiff=3
 outkeep = []
 ichkdiff0=-1
 iout = 0
 for calcrec in calcarr:
  if chkdiff >= mchkdiff:
   print "WARNING: chkdiff premature stop"
   break
  t = calcrec.t
  d = calcrec.d
  s1 = calcrec.s1
  s2 = t.squash  
  l = t.lnum
  m = True  #re.match(r'vcp line# ([0-9]+), d=([0-9]+)',out)
  outarr=[]
  out = "vcp line# %s, d=%s" %(t.lnum,d)
  outarr.append(out)
  out = "  vcp: %s" % s2
  outarr.append(out)
  out = "   te: %s" % s1
  outarr.append(out)
  outarr.append("")
  if m:
   #out = "\n%s" % out
    #d = int(m.group(2))
   if (d > 9): 
    outarr[0] = "%s (CHKDIFF)" % outarr[0]
    chkdiff = chkdiff+1
    if ichkdiff0 == -1:
     ichkdiff0 = iout
   #l = int(m.group(1))
   if (l == lnum):
    outarr[0] = "%s MATCHline" % outarr[0]
    match=True
   else:
    match=False
  if matchonly:
   if match:
     for out in outarr:
      outkeep.append(out)
      iout = iout + 1
     #print "%s" % out.encode('utf-8')
  else:
   for out in outarr:
    outkeep.append(out)
    iout = iout + 1
 # write out (part of) outkeep
 if chkdiff != 0:
  i1 = max(ichkdiff0 - (3*5),0)
 else:
  i1 = 0
 for i in xrange(i1,len(outkeep)):
  out = outkeep[i]
  print "%s" % out.encode('utf-8')
 # write extra comment, if needed
 if chkdiff != 0:
  print "Found %s distances > %s" %(chkdiff,dmax)
 print matchline.encode('utf-8')

def print_tokens(tokens):
 """ for debugging """
 lt = len(tokens)
 for itok in xrange(0,lt):
  t = tokens[itok]
  print itok,t.i1,t.i2,t.type,t.string,t.j1,t.j2

def recover_vac1(tokens,k1,k2,kmax):
 """ returns a string as a concatenation of parts of the tokens
     The cases when k1 = 0 
 """
 if k1 >= kmax:
  # an error condition. The original partition was faulty somehow.
  # provisionally, just return the <MISSING> string
  return "<MISSING>"
 ansarr=[]
 itok0 = 0
 lt = len(tokens)
 if k1 == 0:
  # include the initial batch of markup.
  for token in tokens:
   if token.j1:
    break
   else:
    if re.search(r'\t',token.string): # skip
     pass
    else:
     ansarr.append(token.string) 
    itok0 = itok0 + 1
 #print "DBG1",itok0,lt
 itok1list = [itok  for itok in xrange(itok0,lt) if (not tokens[itok].type) and (tokens[itok].j1 <= k1 < (tokens[itok].j2+1))]
 if len(itok1list) ==0:
  itok1 = itok0
 else:
  itok1 = itok1list[0] # itok1list should be a singleton
 itok2list = [itok  for itok in xrange(itok1,lt) if (not tokens[itok].type) and (tokens[itok].j1 < k2 <= (tokens[itok].j2+1))]
 if len(itok2list) == 0:
  itok2 = lt
  #print "k2=",k2," and itok2list is empty"
 else:
  itok2 = itok2list[0] # itok2list should be a singleton
 #print "DBG2",itok1,itok2
 # possibly only part of token string at itok1 is used
 # string at itok1 goes from j1 to j2.  j1 <= k1 < j2
 token = tokens[itok1]
 m1 = max(token.j1,k1)
 try:
  m2 = min(token.j2+1,k2)
 except:
  print "PROBLEM: itok1 = ",itok1
  print "\nrecover_vac1 DBG: k1,k2,kmax=",k1,k2,kmax
  print_tokens(tokens)
  return "PROBLEM recover_vac1"
 ansarr.append(token.string[m1-token.j1:m2-token.j1])
 # all of intermediate token strings are used
 for itok in xrange(itok1+1,min(itok2,lt)): # was itok2+1
  token = tokens[itok]
  ansarr.append(token.string)
 # possibly, only part of token string at itok2 is used
 # string at itok2 goes from j1 to j2.  j1 < k2 <= j2
 # it is possible the itok1 == itok2
 if itok2 < lt:
  token = tokens[itok2]
  if itok1 == itok2:
   j1a = m2
  else:
   j1a = token.j1
  n1 = max(j1a,k1)
  n2 = min(token.j2+1,k2)
  temp=token.string[n1-j1a:n2-j1a]
  #print "DBG1 : itok2=",itok2,"string=",token.string,"temp=",temp
  ansarr.append(temp)
 # if k2 == kmax, add the rest of the tokens to ansarr
 if k2 == kmax:
  for itok in xrange(itok2+1,lt):  # Mar 15
   token = tokens[itok]
   ansarr.append(token.string)
   #print "DBG2 :",token.string
 # hopefully, we've got everything!
 ans = ''.join(ansarr)
 #print "recover_vac1: itok1,itok2 = ",itok1,itok2
 #print "recover_vac1:",k1,k2,kmax,"\n    ",ans
 return ans

def recover_vac(calcarr):
 """ add attribute 's1vac' to each Calc element of calcarr.
     This is the part of the original Vac string that pertains to the
     s1 element.  Does not return anything.
 """
 k = 0
 dbg=False
 if dbg:
  tokens = calcarr[0].te.tokens
  print "recover_vac: tokens follow"
  print_tokens(tokens)
 for calcrec in calcarr:
  k1 = k
  k2 = k + len(calcrec.s1)
  te = calcrec.te
  tokens = te.tokens
  #calcrec.s1vac = calcrec.s1  # temporary
  if dbg:
   print "call recover_vac1:",k1,k2,te.squashlen," s1=",calcrec.s1
  calcrec.s1vac = recover_vac1(tokens,k1,k2,te.squashlen)
  if dbg:
   print "return recover_vac:",calcrec.s1vac
  k = k2
 return

def match1_lnum_print1(lnum,recs1,recs2,cmprecs=None,matchonly=False):
 result = match1_lnum(lnum,recs1,recs2,cmprecs);
 if not result:
  print "match1_lnum_print: No data"
  return
 (matchline,calcarr) = result
 recover_vac(calcarr)
 match = False
 dmax=9 # a tunable parameter
 chkdiff=0
 mchkdiff=3
 outkeep = []
 ichkdiff0=-1
 iout = 0
 for calcrec in calcarr:
  if chkdiff >= mchkdiff:
   print "WARNING: chkdiff premature stop"
   break
  t = calcrec.t # a Vcp object
  d = calcrec.d
  te = calcrec.te  # a Vac object
  s1_squash = calcrec.s1  # squashed vcp
  s1 = calcrec.s1vac
  #s2 = t.squash  
  tokens = t.tokens
  token_strings = [tok.string for tok in tokens]
  s2 = ''.join(token_strings)
  l = t.lnum
  m = True  #re.match(r'vcp line# ([0-9]+), d=([0-9]+)',out)
  outarr=[]
  out = "vcp line# %s, d=%s" %(t.lnum,d)
  outarr.append(out)
  out = "  vcp: %s" % s2
  outarr.append(out)
  out = "   te: %s" % s1_squash
  outarr.append(out)
  out = "   te: %s" % s1
  outarr.append(out)
  outarr.append("")
  if m:
   #out = "\n%s" % out
    #d = int(m.group(2))
   if (d > 9): 
    outarr[0] = "%s (CHKDIFF)" % outarr[0]
    chkdiff = chkdiff+1
    if ichkdiff0 == -1:
     ichkdiff0 = iout
   #l = int(m.group(1))
   if (l == lnum):
    outarr[0] = "%s MATCHline" % outarr[0]
    match=True
   else:
    match=False
  if matchonly:
   if match:
     for out in outarr:
      outkeep.append(out)
      iout = iout + 1
     #print "%s" % out.encode('utf-8')
  else:
   for out in outarr:
    outkeep.append(out)
    iout = iout + 1
 # write out (part of) outkeep
 if chkdiff != 0:
  i1 = max(ichkdiff0 - (3*5),0)
 else:
  i1 = 0
 for i in xrange(i1,len(outkeep)):
  out = outkeep[i]
  print "%s" % out.encode('utf-8')
 # write extra comment, if needed
 if chkdiff != 0:
  print "Found %s distances > %s" %(chkdiff,dmax)
 print matchline.encode('utf-8')

def match1_lnum_print2(lnum,recs1,recs2,cmprecs=None):
 result = match1_lnum(lnum,recs1,recs2,cmprecs);
 if not result:
  print "match1_lnum_print: No data"
  return
 (matchline,calcarr) = result
 recover_vac(calcarr)
 outarr=[]
 for calcrec in calcarr:
  t = calcrec.t # a Vcp object
  d = calcrec.d
  if (d > 9):
   d = 'X'
  #te = calcrec.te  # a Vac object
  #s1 = calcrec.s1vac # o
  #s2 = t.line  # vcp
  #l = t.lnum
  vcptokens = t.tokens
  vcp_token_strings = [tok.string for tok in t.tokens]
  vcp_line_adj = ''.join(vcp_token_strings)
  vcpout = "%06d:%s: vcp: %s" % (t.lnum,d,vcp_line_adj)
  vacout = "%06d:%s:  te: %s" % (t.lnum,d,calcrec.s1vac)
  outarr.append((vcpout,vacout))
 # write out outkeep
 i1 = 0
 for i in xrange(i1,len(outarr)):
  (vcpout,vacout) = outarr[i]
  print "%s" % vcpout.encode('utf-8')
  print "%s" % vacout.encode('utf-8')
  print ""
 print matchline.encode('utf-8')

def printadj_helper(lnum,recs1,recs2,cmprecs):
 """ returns an array 
 """
 result = match1_lnum(lnum,recs1,recs2,cmprecs);
 outarr=[]
 if result == None:
  return outarr
 (matchline,calcarr) = result
 try:
  recover_vac(calcarr)
 except:
  print "printadj_helper: error1: lnum=",lnum
  return outarr
 for calcrec in calcarr:
  t = calcrec.t # a Vcp object
  d = calcrec.d
  if (d > 9):
   d = 'X'
  #te = calcrec.te  # a Vac object
  #s1 = calcrec.s1vac # o
  #s2 = t.line  # vcp
  #l = t.lnum
  vcp_token_strings = [tok.string for tok in t.tokens]
  vcp_line_adj = ''.join(vcp_token_strings)
  #vcpout = "%06d:%s: vcp: %s" % (t.lnum,d,vcp_line_adj)
  #vacout = "%06d:%s:  te: %s" % (t.lnum,d,calcrec.s1vac)
  out = (t.lnum,d,vcp_line_adj,calcrec.s1vac)
  outarr.append(out)
 return outarr

class VacVcp:
 def __init__(self,lnum,d,data):
  self.lnum = lnum
  self.d = d
  self.data = data 

def printadj(fileout1,fileout2,recs1,recs2,cmprecs=None):
 if not cmprecs:
  cmprecs = init_cmp()
 vacrecs = []
 vcprecs = []
 nrecs2 = len(recs2)
 for i in xrange(0,nrecs2):
  lnum = i+1
  vacrec = VacVcp(lnum,'?','NA')
  vcprec = VacVcp(lnum,'?',recs2[i])
  vacrecs.append(vacrec)
  vcprecs.append(vcprec)
 mdx = 1000000 # make smaller, for debugging
 ndx = 0
 for cmprec in cmprecs:
  chunk2 = cmprec.chunks2[0]
  lnum2 = chunk2.l1
  ansarr = printadj_helper(lnum2,recs1,recs2,cmprecs)
  if len(ansarr) == 0:
   # change 'd' code in vcprecs and vacrecs to '!'
   # The range of lines for this cmprec (from hwcmpvcp1.txt file)
   # has a VACMISSING designation.
   for chunk2 in cmprec.chunks2:
    for indx in xrange(chunk2.l1-1,chunk2.l2):
     vacrecs[indx].d = '!'
     vcprecs[indx].d = '!'
   continue # superfluos, since ansarr is empty, so is next loop
  for (lnum,d,vcpadj,vacadj) in ansarr:
   indx = lnum - 1
   vacrecs[indx]=VacVcp(lnum,d,vacadj)
   vcprecs[indx]=VacVcp(lnum,d,vcpadj)
   #print indx,vacrecs[indx]
   ndx = ndx + 1
   if ndx > mdx:
    print "DBG: printall_val: stopping after %s headwords" % ndx
    break
  if ndx > mdx:
   break
 # for lines unused in vcp, similarly mark the line as unused in vac
 for indx in xrange(0,nrecs2):
  if vcprecs[indx].d == '!':
     vacrecs[indx].d = '!'
     vacrecs[indx].data = ''
 
 # write the outputs
 f1 = codecs.open(fileout1,encoding='utf-8',mode='w')
 f2 = codecs.open(fileout2,encoding='utf-8',mode='w')
 for indx in xrange(0,nrecs2):
  if indx > mdx:
   break
  vacrec = vacrecs[indx]
  vacout = "%06d:%s:  te: %s" % (vacrec.lnum,vacrec.d,vacrec.data)
  f1.write("%s\n" % vacout)
  vcprec = vcprecs[indx]
  vcpout = "%06d:%s: vcp: %s" % (vcprec.lnum,vcprec.d,vcprec.data)
  f2.write("%s\n" % vcpout)
 f1.close()
 f2.close()
 print "%s records written to %s" % (nrecs2,fileout1)
 print "%s records written to %s" % (nrecs2,fileout2)

def old_printadj(fileout1,fileout2,recs1,recs2,cmprecs=None):
 if not cmprecs:
  cmprecs = init_cmp()
 vacrecs = []
 vcprecs = []
 nrecs2 = len(recs2)
 for i in xrange(0,nrecs2):
  lnum = i+1
  d = '?' # line not represented in vac
  vacrec = "%06d:%s: vcp: %s" % (lnum,d,'NA')
  d = '!' # line unused in vcp
  vcprec = "%06d:%s: vcp: %s" % (lnum,d,recs2[i])
  vacrecs.append(vacrec)
  vcprecs.append(vcprec)
 mdx = 1000000
 ndx = 0
 for cmprec in cmprecs:
  chunk2 = cmprec.chunks2[0]
  lnum2 = chunk2.l1
  ansarr = printadj_helper(lnum2,recs1,recs2,cmprecs)
  for (lnum,d,vcpadj,vacadj) in ansarr:
   indx = lnum - 1
   vacrecs[indx]="%06d:%s:  te: %s" % (lnum,d,vacadj)
   vcprecs[indx]="%06d:%s: vcp: %s" % (lnum,d,vcpadj)
   #print indx,vacrecs[indx]
   ndx = ndx + 1
   if ndx > mdx:
    print "DBG: printall_val: stopping after %s headwords" % ndx
    break
  if ndx > mdx:
   break
 # for lines unused in vcp, similarly mark the line as unused in vac

 # write the outputs
 f1 = codecs.open(fileout1,encoding='utf-8',mode='w')
 f2 = codecs.open(fileout2,encoding='utf-8',mode='w')
 for indx in xrange(0,nrecs2):
  f1.write("%s\n" % vacrecs[indx])
  f2.write("%s\n" % vcprecs[indx])
 f1.close()
 f2.close()
 print "%s records written to %s" % (ndx,fileout1)
 print "%s records written to %s" % (ndx,fileout2)

def match1_lnum_chkdiff(lnum0,recs1,recs2,cmprecs=None):
 more = True
 nrecs2 = len(recs2)
 lnum = lnum0-1
 cmprec_prev=None
 while more and ((lnum+1) < nrecs2):
  lnum = lnum + 1 #
  cmprec = find_cmp_vcp(lnum,cmprecs)
  if not cmprec:
   continue
  if cmprec == cmprec_prev:
   continue
  cmprec_prev = cmprec
  result = match1_lnum(lnum,recs1,recs2,cmprecs);
  if not result:
   continue
  (matchline,calcarr) = result
  dmaxfound = max([calc.d for calc in calcarr])
  dmax = 9
  if dmaxfound <= dmax:
   print "OK ",matchline
   continue
  else:
   match1_lnum_print(lnum,recs1,recs2,cmprecs=cmprecs)
   break

def vac_for_missing(filein,filein1,fileout):
 """ filein is a file of 'missing' records (vcp_missing.txt)
     filein1 is vac2.txt (TE edition split into comparable lines)
     fileout shows corresponding lines from vcp_missing and vac
 """
 recsin = init_digitization(filein)
 nin = len(recsin)
 vacrecs = init_digitization(filein1)
 nin1 = len(vacrecs)
 vacdict = {} # hash on lnum
 i = 0
 for vacrec in vacrecs: 
  i = i + 1
  m = re.match(r'^([^:]*):([^:]*):([^:]*): (.*)$',vacrec)
  if m:
   (lnumstr,d,data) = (m.group(1),m.group(2),m.group(4))
  else:  # some lines have no data
   m = re.match(r'^([^:]*):([^:]*):([^:]*):(.*)$',vacrec)
   if m:
    (lnumstr,d,data) = (m.group(1),m.group(2),m.group(4))
   else:
    print "PARSE ERROR at line %s in file %s:\n %s" % (i,filein1,vacrec)
    break
  lnum = int(lnumstr)
  vacdict[lnum] = i-1 # index into vacrecs
 # now match. Construct outarr
 outarr = []
 i = 0
 for rec in recsin:
  i = i + 1
  m = re.match(r'^([^:]*): (.*)$',rec)
  if not m:
   print "PARSE ERROR at line %s in file %s:\n %s" % (i,filein,rec)
   break
  (lnumstr,vcpdata) = (m.group(1),m.group(2))
  lnum = int(lnumstr)
  if lnum not in vacdict:
   print "LOOKUP ERROR at line %s in file %s:\n %s" % (i,filein,rec)
   break
  vacindx = vacdict[lnum]
  outarr1=[]
  outarr1.append(72*'-')
  vcpline = "%s:%s: vcp: %s" %(lnumstr,' ',vcpdata)
  m = re.search(r'^<.*?>',vcpdata)
  if m:
   offset = ' '*len(m.group(0))
  else:
   offset = ''
  for j in xrange( max(vacindx-3,0),min(vacindx+4,nin1)):
   vacline = vacrecs[j]
   vacline = re.sub(r' vcp:','  te:',vacline) # correct an error, 
   vacline = re.sub(r'  te:','  te:%s'% offset,vacline) # improve alignment
   vacline = re.sub(r'<page>.*$','',vacline) # remove tail part
   vacline = re.sub(r'<q>',u'“',vacline)  # convert quotes to vcp form
   vacline = re.sub(r'</q>',u'”',vacline)  # convert quotes to vcp form
   vacline = re.sub(r'<.*?>','',vacline)  # remove pseudo-xml markup
   if j != vacindx:
    outarr1.append(vacline)
   else:
    outarr1.append('')
    outarr1.append(vacline)
    outarr1.append(vcpline)
    outarr1.append('')
  outarr.append(outarr1)
 # write the output
 f = codecs.open(fileout,encoding='utf-8',mode='w')
 for outarr1 in outarr:
  for out in outarr1:
   f.write('%s\n' % out)
 f.close()

  
def select_missing(filein,fileout):
 """ filein is original vcp file (vcp0)
     fileout is output. 
     Select lines from filein with {??} pattern, noting the linenumber
     write the line-number and the line to fileout.
 """
 recsin = init_digitization(filein)
 nin = len(recsin)
 f = codecs.open(fileout,encoding='utf-8',mode='w')
 nout=0
 for i in xrange(0,nin):
  rec = recsin[i]
  lnum = i+1
  if re.search(r'{[?]',rec):
   f.write("%06d: %s\n" %(lnum,rec))
   nout = nout + 1
 f.close()
 print "%s / %s records from %s written to %s" % (nout,nin,filein,fileout)

if __name__=="__main__":
 filein1 = sys.argv[1] # vac1.txt
 filein2 = sys.argv[2] # vcp.txt
 fileout = sys.argv[3] # diff
 te_findlines1_main(filein1,filein2,fileout)
 
