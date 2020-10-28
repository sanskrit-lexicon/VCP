#-*- coding:utf-8 -*-
"""abbrev0
 
 
"""
from __future__ import print_function
import sys, re,codecs
from parseheadline import parseheadline
import transcoder
transcoder.transcoder_set_dir('transcoder')

# for Sanskrit sorting
slp_from = "aAiIuUfFxXeEoOMHkKgGNcCjJYwWqQRtTdDnpPbBmyrlvSzsh"
slp_to =   "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvw"
slp_from_to = str.maketrans(slp_from,slp_to)


class Entry(object):
 Ldict = {}
 def __init__(self,lines,linenum1,linenum2):
  # linenum1,2 are int
  self.metaline = lines[0]
  self.lend = lines[-1]  # the <LEND> line
  self.datalines = lines[1:-1]  # the non-meta lines
  # parse the meta line into a dictionary
  #self.meta = Hwmeta(self.metaline)
  self.metad = parseheadline(self.metaline)
  self.linenum1 = linenum1
  self.linenum2 = linenum2
  #L = self.meta.L
  L = self.metad['L']
  if L in self.Ldict:
   print("Entry init error: duplicate L",L,linenum1)
   exit(1)
  self.Ldict[L] = self
  #  extra attributes
  self.marked = False # from a filter of markup associated with verbs
  self.markcode = None
  self.markline = None

def init_entries(filein):
 # slurp lines
 with codecs.open(filein,encoding='utf-8',mode='r') as f:
  lines = [line.rstrip('\r\n') for line in f]
 recs=[]  # list of Entry objects
 inentry = False  
 idx1 = None
 idx2 = None
 for idx,line in enumerate(lines):
  if inentry:
   if line.startswith('<LEND>'):
    idx2 = idx
    entrylines = lines[idx1:idx2+1]
    linenum1 = idx1 + 1
    linenum2 = idx2 + 1
    entry = Entry(entrylines,linenum1,linenum2)
    recs.append(entry)
    # prepare for next entry
    idx1 = None
    idx2 = None
    inentry = False
   elif line.startswith('<L>'):  # error
    print('init_entries Error 1. Not expecting <L>')
    print("line # ",idx+1)
    print(line.encode('utf-8'))
    exit(1)
   else: 
    # keep looking for <LEND>
    continue
  else:
   # inentry = False. Looking for '<L>'
   if line.startswith('<L>'):
    idx1 = idx
    inentry = True
   elif line.startswith('<LEND>'): # error
    print('init_entries Error 2. Not expecting <LEND>')
    print("line # ",idx+1)
    print(line.encode('utf-8'))
    exit(1)
   else: 
    # keep looking for <L>
    continue
 # when all lines are read, we should have inentry = False
 if inentry:
  print('init_entries Error 3. Last entry not closed')
  print('Open entry starts at line',idx1+1)
  exit(1)

 print(len(lines),"lines read from",filein)
 print(len(recs),"entries found")
 return recs

def mark_entries(entries):
 """ vcp abbreviations  
   Words ending in '0' (zero)
   Two kinds:  Grammatical  (probably on line 1 or 2)
   Literary:  on subsequent lines
   Add attributes gr_abbrevs, ls_abbrevs to each entry
 """
 n = 0
 for entry in entries:
  # first exclude known non-verbs
  k1 = entry.metad['k1']
  L  = entry.metad['L']
  metaline = entry.metaline
  code = None
  linenum1 = entry.linenum1  # integer line number of metaline  
  datalines = entry.datalines
  gr_abbrevs = []  # grammatical (based on line 1,2
  ls_abbrevs = []  # non-grammatical
  for iline,line in enumerate(datalines):
   if line.startswith('[Page'):
    continue  # skip page break lines
   line = line.replace('<>',' ')  # all lines start this way
   abbrevs = re.findall('[a-zA-Z]+0',line)
   if len(abbrevs) == 0:
    continue  # no abbreviations on line
   # classify abbrevs as 'gr' or 'ls'.  
   # Don't worry about duplicates now
   if iline in [0,1]:
    gr_abbrevs = gr_abbrevs + abbrevs
   else:
    ls_abbrevs = ls_abbrevs + abbrevs
  entry.gr_abbrevs = gr_abbrevs
  entry.ls_abbrevs = ls_abbrevs
  if (len(gr_abbrevs)+len(ls_abbrevs)) > 0:
   n = n + 1
 print(n,'entries have abbreviations')

def write(fileout,entries):
 tranin = 'slp1'
 n = 0
 with codecs.open(fileout,"w","utf-8") as f:
  for ientry,entry in enumerate(entries):
   if not entry.marked:
    continue
   line = entry.datalines[0]
   linenum = entry.linenum1 + 1
   out = '%7d:%s' %(linenum,line)
   f.write(out+'\n')
   n = n + 1
 print(n,"records written to",fileout)

def write_verbs(fileout,entries):
 n = 0
 with codecs.open(fileout,"w","utf-8") as f:
  for ientry,entry in enumerate(entries):
   code = entry.markcode
   if not code:
    continue
   n = n + 1
   outarr = []
   k1 = entry.metad['k1']  
   L =  entry.metad['L']
   k2 = entry.metad['k2']
   outarr.append(';; Case %04d: L=%s, k1=%s, k2=%s, code=%s' %(n,L,k1,k2,code))
   linenum = entry.linenum1 + 1
   line = entry.datalines[0]
   outarr.append('%6s: %s'%(linenum,line))
   outarr.append(';')
   for out in outarr:
    f.write(out+'\n')
 print(n,"verbs written to",fileout)

class Outrec(object):
 def __init__(self,a,ngr,nls,gr_samples,ls_samples):
  self.abbrev = a
  self.ngr = ngr  # number of 'grammar' abbreviations
  self.nls = nls  # number of 'non-grammar' abbreviations
  self.gr_hws = gr_samples  # sample of headwords with the abbreviation
  self.ls_hws = ls_samples  

def prepare_recs(entries,minabbrev):
 recs = []  # list of Outrec objects returned
 dgr = {}
 dls = {}
 def addab(abbrevs,d):
  for a in abbrevs:
   if a not in d:
    d[a] = 0
   d[a] = d[a] + 1
 
 for entry in entries:
  addab(entry.gr_abbrevs,dgr)
  addab(entry.ls_abbrevs,dls)

 # get first 5 examples
 gr_exs = {}
 ls_exs = {}
 for entry in entries:
  for a in entry.gr_abbrevs:
   if a not in gr_exs:
    gr_exs[a] = []
   if entry not in gr_exs[a]:
    gr_exs[a].append(entry)

  for a in entry.ls_abbrevs:
   if a not in ls_exs:
    ls_exs[a] = []
   if entry not in ls_exs[a]:
    ls_exs[a].append(entry)

 #print('gr abbrevs')
 #gr_keys = dgr.keys()
 gr_keys = sorted(dgr.keys(),key = lambda x: x.translate(slp_from_to))
 #for a in gr_keys:
 # print(a,dgr[a])

 #print('ls abbrevs')
 #ls_keys = dls.keys()
 ls_keys = sorted(dls.keys(),key = lambda x: x.translate(slp_from_to))

 #for a in ls_keys:
 # print(a,dls[a])
 keys = gr_keys
 # get additional ls keys, avoid dups
 for a in ls_keys:
  if a not in dgr:
   keys.append(a)
 print("ALL ABBREVS",len(keys))
 all_keys = sorted(keys,key = lambda x: x.translate(slp_from_to))
 nprint = 0
 for a in all_keys:
  ngr = 0
  nls = 0
  gr_samples = []
  ls_samples = []
  if a in dgr:
   ngr = dgr[a]
   #if a == 'akarmma0':print('dbg gr:',a,gr_exs[a])
   gr_samples = [entry.metad['k1'] for entry in gr_exs[a][0:5]]
  if a in dls:
   nls = dls[a]
   ls_samples = [entry.metad['k1'] for entry in ls_exs[a][0:5]]
  na = ngr + nls
  if na >= minabbrev:
   print(a,ngr,nls,gr_samples,ls_samples)
   rec = Outrec(a,ngr,nls,gr_samples,ls_samples)
   recs.append(rec)
 nrecs = len(recs)
 print(nrecs,"abbreviations printed with',minabbrev,'or more instances")
 return recs

def make_link_md(k,tranout):
 # assume k is slp1 spelling of VCP headword
 # make a Github markdown link to a display of this headword at Cologne
 tranin = 'slp1'
 ktran = transcoder.transcoder_processString(k,tranin,tranout)
 href = 'https://www.sanskrit-lexicon.uni-koeln.de/scans/awork/apidev/sample/list-0.2.php?dict=vcp&input=slp1&output=%s&key=%s' %(tranout,k)
 link = '[%s](%s)' %(ktran,href)
 return link

def write_md(fileout,tranout,recs,minabbrev):
 outarr = []
 tranin = 'slp1'
 outarr.append('## VCP abbreviations with %s or more instances'%minabbrev)
 outarr.append('|seq|abbrev|#gr|#ls|gr|ls|')
 outarr.append('|---|---|---|---|---|---|')
 for irec,rec in enumerate(recs):
  # Outrec object
  outa = []  
  nrec = irec+1
  outa.append("%s"%nrec) # sequence number
  a = transcoder.transcoder_processString(rec.abbrev,tranin,tranout)
  outa.append(a)  # the abbreviation
  outa.append('%s'% rec.ngr)
  outa.append('%s'% rec.nls)
  gr_refs = [make_link_md(k1,tranout) for k1 in rec.gr_hws]
  ls_refs = [make_link_md(k1,tranout) for k1 in rec.ls_hws]
  outa.append(' '.join(gr_refs))
  outa.append(' '.join(ls_refs))
  # make a markdown table row
  out = ' | '.join(outa)
  out = '|' + out + '|'  
  outarr.append(out)
 with codecs.open(fileout,"w","utf-8") as f:
  for out in outarr:
   f.write(out+'\n')

if __name__=="__main__": 
 option = sys.argv[1]  # tranout,format-option
 filein = sys.argv[2] #  xxx.txt (path to digitization of xxx)
 fileout = sys.argv[3] # 
 entries = init_entries(filein)
 mark_entries(entries)
 tranout,printopt,minabbrev_str = option.split(',')
 minabbrev = int(minabbrev_str)
 outrecs = prepare_recs(entries,minabbrev)
 if printopt == 'md':
  write_md(fileout,tranout,outrecs,minabbrev)
 else:
  print('unknown print option',printopt)
  exit(1)
