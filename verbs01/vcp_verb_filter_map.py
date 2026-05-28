#-*- coding:utf-8 -*-
"""vcp_verb_filter_map.py
"""
from __future__ import print_function
import sys, re,codecs

class Vcpverb(object):
 def __init__(self,line):
  line = line.rstrip()
  self.line = line
  m = re.search(r'L=([^,]*), k1=([^,]*), k2=([^,]*)',line)
  self.L,self.k1,self.k2 = m.group(1),m.group(2),m.group(3)
  #self.skd=None
  self.mw = None
 
def init_vcpverb(filein):
 with codecs.open(filein,"r","utf-8") as f:
  recs = [Vcpverb(x) for x in f if x.startswith(';; Case')]
 print(len(recs),"records read from",filein)
 return recs

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
 #recs = [r for r in recs if r.cat == 'verb']
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
 'kusma':'kusmaya',
 'raSa':'raSanAya',
 'lata':'latAya',
 'vfca':'vfj',
 'zasta':'saMst',
 'sAma':'sAmaya',
 'svurcCa':'svUrC',  # vcp typo svurcCa ?
 'kapa':'kamp',
 'kfpa':'kxp',
 'krada':'krand',
 'Kuq':'KuRq',
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
  k1 = rec.k1  # the VCP spelling of root
  rec.mw = map2mw(mwverbsd,k1)
  if rec.mw != None:
   nok = nok + 1
   if rec.mw == k1:
    neq = neq + 1
   else:
    noteq = noteq + 1
 print(nok,"dhatus mapped to MW verbs")
 print(noteq," of the mapped mwspellings differ from the dhatu spellings")
 print(n-nok,"dhatus are unmapped")

def write(fileout,recs):
 n = 0
 with codecs.open(fileout,"w","utf-8") as f:
  for rec in recs:
   n = n + 1
   line = rec.line
   # add mw field
   if rec.mw == None:
    mw = '?'
   else:
    mw = rec.mw
   out1 = "mw=%s" %mw
   # remove 'code' field
   line1 = re.sub(', code=.*$','',line)
   out = '%s, %s' %(line1,out1)
   f.write(out + '\n')
 print(n,"records written to",fileout)

if __name__=="__main__": 
 filein = sys.argv[1] #  skd_verb_filter.txt
 #filein1 = sys.argv[2] # xvcp_mw_map_init.txt
 filein2 = sys.argv[2] # mwverbs1
 fileout = sys.argv[3]

 recs = init_vcpverb(filein)
 #vcpmw = init_vcpmw(filein1)
 mwverbs,mwverbsd= init_mwverbs(filein2)
 mwverbmap(mwverbsd,recs)
 write(fileout,recs)
