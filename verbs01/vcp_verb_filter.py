#-*- coding:utf-8 -*-
"""vcp_verb_filter.py
 
 
"""
from __future__ import print_function
import sys, re,codecs
from parseheadline import parseheadline
import transcoder
transcoder.transcoder_set_dir('transcoder')

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

def mark_entries_verb(entries,exclusions,inclusions):
 """ vcp verbs:  """
 nexc = 0
 ninc = 0
 for entry in entries:
  # first exclude known non-verbs
  k1 = entry.metad['k1']
  L  = entry.metad['L']
  metaline = entry.metaline
  code = None
  linenum1 = entry.linenum1  # integer line number of metaline  
  datalines = entry.datalines
  line0 = datalines[0]
  #regexes = [u'¦ *[a-zA-Z]+e ', u'¦ *[a-zA-Z]+O ', u'¦ *[a-zA-Z]+A[mM] ']
  # 05-11-2020. Allow trailing space 'OR' comma
  regexes = [u'¦ *[a-zA-Z]+e[ ,]', u'¦ *[a-zA-Z]+O[ ,]', u'¦ *[a-zA-Z]+A[mM][ ,]']
  for iregex,regex in enumerate(regexes):
   if re.search(regex,line0):
    code = iregex + 1
    break
  if L in inclusions: #(linenum1+1)  in inclusions:
    ninc = ninc + 1
    code = len(regexes)+1
    #print('include:',metaline)
  elif not re.search(r'0',line0) :
   code = None
   continue
  if True:  #dbg
   if L=='10344':
    print('chk:',k1,L,code,line0)
  if L in exclusions: #(linenum1+1) in exclusions:
   nexc = nexc + 1
   #print('exclude:',metaline)
   continue
  entry.markcode = code
  entry.marked = True
  #entry.markline = datalines[0]
  #entry.marklinenum=linenum1 + 1
  continue
  # patterns of first line that indicate non-verb
  
  if re.search(r' klI,',datalines[0]): # neuter
   continue
  if re.search(r' puM,',datalines[0]): # masculine 
   continue
  if re.search(r' strI,',datalines[0]): # feminine
   continue
  if re.search(r' tri,',datalines[0]): # 3-genders ?
   continue
  
  # patterns in additional lines
  for iline,line in enumerate(datalines):
   if iline == 0:  #handled above
    continue
   if re.search(' iti kavikalpadrumaH',line):
    code = 10
   elif re.search('<>iti kavikalpadrumaH',line):
    code = 11
   elif re.search(' iti kavikalpa-',line): 
    code = 12
   elif re.search(' iti kavi-',line):
    code = 13
   elif re.search('kavikalpalat',line):
    continue  # kavakalpalatA NOT a verb indicator
   elif L in ['8480','31310','37770','42132']:
    code = 14  # kUpa, varRa, sapa, hrapa
   elif re.search('[< ]kavi',line):
    # 13 cases.  These are alphabet letters
    pass
   if code != None:
    entry.markcode = code
    entry.markline = line
    entry.marklinenum=entry.linenum1 + (iline+1)
    break # for iline,line
 print(nexc,"special exclusions applied")
 print(ninc,"special inclusions applied")

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

def write1(fileout,recs):
 n = 0
 with codecs.open(fileout,"w","utf-8") as f:
  for irec,rec in enumerate(recs):
   entry = rec.entry
   if rec.line1.strip() != entry.datalines[0].strip():
    print(' rec.line1=',rec.line1)
    print('entry line=',entry.datalines[0])
    print('Error at record',irec+1)
    exit(1)
   upasargas=find_upasarga_lines(entry)
   k1 = entry.metad['k1']  
   L =  entry.metad['L']
   k2 = entry.metad['k2']
   outarr = []
   outarr.append('; Case %04d: L=%s, k1=%s, k2=%s, #upasargas=%s' %(irec+1,L,k1,k2,len(upasargas)))
   outarr.append(rec.line1)
   for x in upasargas:
    outarr.append(x)
   outarr.append(';')
   n = n + 1
   for out in outarr:
    f.write(out + '\n')
 print(n,"records written to",fileout)

def find_entries(recs,entries):
 # dictionary for entries
 d = {}
 for entry in entries:
  d[entry.linenum1]= entry
 # 
 for irec,rec in enumerate(recs):
  try:
   linenum = int(rec.linenum)
  except:
   print('find_entries. bad linenum=',rec.linenum)
   print('record # ',irec+1)
   print('  line = ',rec.line)
   exit(1)
  rec.entry = d[linenum-1]

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

def init_extras(filein):
 with codecs.open(filein,encoding='utf-8',mode='r') as f:
  d = {}
  for line in f:
   line = line.rstrip('\r\n')
   if not line.startswith(';'):
    m = re.search(r'<L>(.*?)<',line)
    L = m.group(1)
    d[L] = line
 print(len(d.keys()),"records read from",filein)
 return d

def previous_init_extras(filein):
 with codecs.open(filein,encoding='utf-8',mode='r') as f:
  d = {}
  for line in f:
   line = line.rstrip('\r\n')
   if not line.startswith(';'):
    m = re.search(r'^(.*?):(.*)$',line)
    linenum = int(m.group(1))
    d[linenum] = m.group(2) 
 print(len(d.keys()),"records read from",filein)
 return d

if __name__=="__main__": 
 filein = sys.argv[1] #  xxx.txt (path to digitization of xxx
 filein1 = sys.argv[2] # exclusions  
 filein2 = sys.argv[3] # inclusions  
 fileout = sys.argv[4] # 
 entries = init_entries(filein)
 exclusions = init_extras(filein1)
 inclusions = init_extras(filein2)
 mark_entries_verb(entries,exclusions,inclusions)
 #write(fileout,entries) # for debugging comparison with VCP-Dhatus.txt
 write_verbs(fileout,entries)
