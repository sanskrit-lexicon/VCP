#-*- coding:utf-8 -*-
"""verb1.py
 
 
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
  self.marks = []  # verb markup markers, in order found, if any

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

def  make_correction(entry,iline,oldline,newline,upasarga,upasarga1):
 outarr = []
 d = entry.metad
 outarr.append('; key = %s, L = %s,  %s -> %s'%(d['k1'],d['L'],upasarga,upasarga1))
 lnum = entry.linenum1 + iline +1
 outarr.append('%s old %s' %(lnum,oldline))
 outarr.append('%s new %s' %(lnum,newline))
 outarr.append(';')
 return outarr

def mark_entries_verb(entries,pwnonverbsd):
 for entry in entries:
  # first exclude known non-verbs
  k1 = entry.metad['k1']
  if k1 in pwnonverbsd:
   continue
  # might be a verb. look for upasarga pattern
  marks = []
  for iline,line in enumerate(entry.datalines):
   m = re.search(r'<ab>(Desid.|Intens.|Caus.)</ab>',line)
   if m:
    form = m.group(1)
    marks.append(form)
   m = re.search(r'<div n="p">— Mit {#(.*?)#}',line)
   if m:
    upasarga = m.group(1)
    # look for cases with {#xxx#} contains more than upasarga
    if not re.search(r'^[*]?[a-zA-Z]*$',upasarga):    
     upasarga = '{#%s#}' % upasarga
     upasarga1 = re.sub(r'^{#([*]?.*?)([^a-zA-Z].*)#}$',r'{#\1#}{#\2#}',upasarga)
     upasarga2 = re.sub(r'#}{# *, *',r'#}, {#',upasarga1)
     newline = line.replace(upasarga,upasarga2)
     correction_lines = make_correction(entry,iline,line,newline,upasarga,upasarga2)
     for c in correction_lines:
      print(c)
     # correct upasarga for marks
     m = re.search(r'<div n="p">— Mit {#(.*?)#}',newline)
     upasarga = m.group(1)
    # add upasarga to the list of marks
    marks.append(upasarga)
    
  if len(marks) == 0:
   continue
  # remove cases where ONLY Desid.|Intens.|Caus. is present in marks
  marks = [x for x in marks if x not in ['Desid.','Intens.','Caus.']]
  if len(marks) > 0:
   """ Consider cases like 
     {#*marImfja#}¦ <lex>Adj.</lex> vom <ab>Intens.</ab> von {#marj#}.
    which should NOT be marked as verb
   """
   isverb = True  # tentatively
   line = entry.datalines[0]
   if re.search(r'¦ *<lex>',line):
    print(entry.metad['k1'],entry.metad['L'],' NOT A VERB')
    isverb = False #  No, mistaken identity!
   if isverb:
    entry.marked = True
    entry.marks = marks

def merge_marked_entries(entries):
 d = {}
 keys = []
 for entry in entries:
  if not entry.marked:
   continue
  k1 = entry.metad['k1']
  if k1 not in d:
   d[k1] = []
   keys.append(k1)
  d[k1].append(entry)
 entrylists = []
 for k1 in keys:
  entrylists.append(d[k1])
 return entrylists

def find_upasarga_lines(entry):
 lines = entry.datalines
 outlines = []  # returned
 for iline,line in enumerate(lines):
  m = re.search(r'^<HI>[^ ]+ +[+] ',line)
  if m:
   outlines.append(line)
   lines[iline] = '*' + line
 return outlines

class Dhatu(object):
 def __init__(self,line):
  line = line.rstrip('\r\n')
  self.line = line
  m = re.search(r'L=([^,]*), k1=([^,]*), k2=([^,]*), #upasargas=([^, ]*).*?, mw=([^ ]*)',line)
  self.L,self.k1,self.k2,self.numupas,self.mwverb = m.group(1),m.group(2),m.group(3),m.group(4),m.group(5)

def init_verbs(filein):
 # slurp lines
 with codecs.open(filein,encoding='utf-8',mode='r') as f:
  recs = [Dhatu(line) for line in f if line.startswith(';;')]
 print(len(recs),'records from',filein)
 return recs

def find_entries(recs,entries):
 # dictionary for entries
 d = {}
 for entry in entries:
  L = entry.metad['L']
  d[L]= entry
 # 
 for irec,rec in enumerate(recs):
  L = rec.L
  rec.entry = d[L]

class MWVerb(object):
 def __init__(self,line):
  line = line.rstrip()
  self.line = line
  self.k1,self.L,self.cat,self.cps,self.parse = line.split(':')
  self.used = False

def init_mwverbs(filein):
 with codecs.open(filein,"r","utf-8") as f:
  recs = [MWVerb(x) for x in f]
 print(len(recs),"mwverbs read from",filein)
 recs = [r for r in recs if r.cat == 'verb']
 #recs = [r for r in recs if r.cat in ['root','genuineroot']]
 #recs = [r for r in recs if r.cat == 'verb']
 print(len(recs),"verbs returned from mwverbs")
 d = {}
 for rec in recs:
  k1 = rec.k1
  if k1 in d:
   print('init_mwverbs: Unexpected duplicate',k1)
  d[k1] = rec
 return recs,d

def insert_nasal(k):
 k1 = k[0:-1]
 e = k[-1]
 if e in 'kKgG':
  return k1+'N'+e
 if e in 'cCjJ':
  return k1+'Y'+e
 if e in 'wWqQ':
  return k1+'R'+e
 if e in 'tTdD':
  return k1+'n'+e
 if e in 'pPbB':
  return k1+'m'+e
 if e in 'Ss':
  return k1+'M'+e
 if e in 'v ':
  return k1+'n'+e
 return k

map2mw_special = {
 'Rardda':'nard',
 'RI':'nI',
 'Ru':'nu',
 'RU':'nU',
 'zu':'su',
 'zU':'sU',
 'ambara':'ambarya',
 'uzas':'uzasya',
 'Una':'Unaya',
 'UrRRu':'UrRu',
 'kaRqU':'kaRqUya',
 'kadqa':'kaqq',
 'kAkza':'kANkz',
 'kAla':'kAlaya',
 'kiroqAwa':'kiroqAwya',
 'kuwumba':'kuwumbaya',
 'kudra':'kundr',
 'kumAra':'kumAraya',
 'kumAla':'kumAlaya',
 'kuzuBa':'kuzuBya',
 'keta':'ketaya',
 'kelA':'kelAya',
 'KelA':'KelAya',
 'gadgada':'gadgadya',
 'gAtra':'gAtraya',
 'guRa':'guRaya',
 'gudra':'gundr',
 'gUrha':'gUrD',  # ??
 'gfha':'gfhaya',
 'goDA':'goDAya',
 'goma':'gomaya',
 'Gaza':'GaMz',
 'GiRa':'GiRR',
 'cihna':'cihnaya',
 'curaRa':'curaRya',
 'Cardda':'Cfd',
 'Cidra':'Cidraya',
 'jiva':'jinv',
 'Jf':'JF',
 'qiba':'qimb',
 'Riva':'ninv',
 'Risa':'niMs',
 'tatra':'tantraya',
 'tadra':'tandr',
 'tantas':'taMs',
 'taruza':'tF',
 'tIra':'tIraya',
 'tutTa':'tutTaya',
 'turaRa':'turaRya',
 'tfnha':'tfh',
 'trA':'trE',
 'tvarAyas':'tvarAyasya',
 'daRqa':'daRqaya',
 'danSa':'daMS',
 'daridrA':'drA',  # intensive
 'dava':'danv',
 'duvas':'duvasya',
 'dravat':'dravatya',
 'dravas':'dravasya',
 'drAkza':'drANkz',
 'Diva':'Dinv',
 'DmAkza':'DmANkz',
 'Dra':'DrA',
 'DrAkza':'DrANkz',
 'Dvansa':'DvaMs',
 'nf':'nF',
 'paRasya':'panasya',   # vcp alternate spelling. Also in MW
 'pampas':'pampasya',
 'pAra':'pAraya',
 'piva':'pinv',
 'purARa':'purARya',
 'puzpa':'puzpya',
 'pUra':'pF',
 'bana':'van',
 'baha':'baMh',
 'byaDa':'vyaD',  # alternate spelling vyaDa
 'byuza':'vyuz',
 'Biza':'viz', # ?
 'BranSa':'BraMS',
 'Brasja':'Brajj',
 'BrASaM':'BrAS',
 'matra':'mantr',
 'masja':'majj',
 'mAkza':'mANkz',
 'mUtra':'mUtraya',
 'yatra':'yantr',
 'rava':'raRv',
 'riba':'rimb',
 'riva':'riRv',
 'larva':'larb',
 'lasja':'lajj',
 'vara':'vf',
 'vardDa':'varD',
 'vAkza':'vANkz',
 'Sansa':'SaMs',
 'zaRa':'san',
 'zanca':'saYc',
 'zanja':'saYj',
 'zarjja':'sarj',
 'zasja':'sajj',
 'zi':'si',
 'zunBa':'SumB',
 'zfnBa':'sfmB',
 'zE':'sE',
 'zo':'so',
 'zwu':'stu',
 'zwE':'stE',
 'zwyE':'styE',
 'zWaga':'sTag',
 'zWala':'sTal',
 'zWA':'sTA',
 'zRasa':'snas',
 'zRA':'snA',
 'zmi':'smi',
 'zvanja':'svaYj',
 'zvartta':'svart',
 'saNgrAma':'saMgrAm', # mw preverb
 'sapara':'saparya',
 'sAra':'sAraya',
 'sika':'sek',
 'stoma':'stomaya',
 'spardDa':'sparD',
 'sransa':'sraMs',
 'hillola':'hillolaya',
 'hfRI':'hfRIya',
 'hriRI':'hriRIya',
 'zRiha':'snih',
 'zRu':'snu',
 'zRuca':'snuc',
 'zRusa':'snus',
 'zRuha':'snuh',
 'zRE':'snA',
 'izuDa':'izuDya',
 'Ceda':'Cid',
 #'':'',
 #'':'',
 #'':'',
 #'':'',

}
def map2mw(d,k1):
 if k1 in d:
  return k1
 if k1 in map2mw_special:
  return map2mw_special[k1]
 if not k1.endswith('a'):
  return None
 k = k1[0:-1] # remove final 'a'
 if k in d:
  return k
 k2 = re.sub(r'n([cCjJ])',r'Y\1',k)
 if k2 in d:
  return k2
 k2 = re.sub(r'n([pPbB])',r'm\1',k)
 if k2 in d:
  return k2
 k2 = re.sub(r'(.)\1',r'\1',k)
 if k2 in d:
  return k2
 k2 = re.sub(r'(.)\1',r'\1',k)
 k2 = re.sub(r'cC','C',k)
 if k2 in d:
  return k2
 k2 = insert_nasal(k)
 if k2 in d:
  return k2
 k2 = re.sub(r'^R','n',k)
 if k2 in d:
  return k2
 k2 = re.sub(r'^zw','st',k)
 if k2 in d:
  return k2
 k2 = re.sub(r'^z','s',k)
 if k2 in d:
  return k2

 return None  # no match

def mwverbmap(mwverbsd,recs):
 nok = 0
 neq = 0  
 noteq = 0
 n = len(recs)
 for rec in recs:
  entry = rec.entry
  k1 = entry.metad['k1']  # the VCP spelling of root
  rec.mwverb = map2mw(mwverbsd,k1)
  if rec.mwverb != None:
   nok = nok + 1
   if rec.mwverb == k1:
    neq = neq + 1
   else:
    noteq = noteq + 1
 print(nok,"dhatus mapped to MW verbs")
 print(noteq," of the mapped mwspellings differ from the dhatu spellings")
 print(n-nok,"dhatus are unmapped")

def transcode_line(x,tranin,tranout):
 """ For VCP. Take into account xml-like markup
 """
 if re.search(r'^\[Page.*?\]$',x):
  return x
 parts = re.split(r'(<[^>]*>)',x)
 newparts = []
 for part in parts:
  if part.startswith('<'):
   newparts.append(part)
  else:
   newpart = transcoder.transcoder_processString(part,tranin,tranout)
   newparts.append(newpart)
 y = ''.join(newparts)
 return y

def write(fileout,recs,tranout):
 tranin = 'slp1'
 n = 0
 with codecs.open(fileout,"w","utf-8") as f:
  for irec,rec in enumerate(recs):
   entry = rec.entry
   k1 = entry.metad['k1']  
   L =  entry.metad['L']
   k2 = entry.metad['k2']
   mw = rec.mwverb
   if mw == '?':
    pass
   elif mw == k1:
    mw = mw + ' (same)'
   else:
    mw = mw + ' (diff)'
   outarr = []
   outarr.append(';; Case %04d: L=%s, k1=%s, k2=%s, #upasargas=%s, mw=%s' %(irec+1,L,k1,k2,rec.numupas,mw))
   for x in entry.datalines:
    m = re.search(r'^<HI>([a-zA-Z +]+) [+] ',x)
    if m:
     x = '*' + x
    y = transcode_line(x,tranin,tranout)
    outarr.append(y)
   outarr.append(';' + ('-'*70))
   outarr.append(';')
   n = n + 1
   for out in outarr:
    f.write(out + '\n')
 print(n,"records written to",fileout)


if __name__=="__main__": 
 tranout = sys.argv[1] # deva or slp1
 filein = sys.argv[2] #  xxx.txt (path to digitization of xxx)
 filein1 = sys.argv[3] # vcp_preverb1.txt
 fileout = sys.argv[4] # 
 entries = init_entries(filein)
 dhatus = init_verbs(filein1)
 find_entries(dhatus,entries)
 write(fileout,dhatus,tranout)
