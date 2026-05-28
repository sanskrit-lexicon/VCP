#-*- coding:utf-8 -*-
"""preverb1.py
 
 
"""
from __future__ import print_function
import sys, re,codecs
from parseheadline import parseheadline
#import transcoder
#transcoder.transcoder_set_dir('transcoder')

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
 recs = [r for r in recs if r.cat == 'preverb']
 print(len(recs),"verbs returned from mwverbs")
 d = {}
 for rec in recs:
  k1 = rec.k1
  if k1 in d:
   print('init_mwverbs: Unexpected duplicate',k1)
  d[k1] = rec
 return recs,d


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

def yesno(flag):
 if flag:
  return 'yes'
 else:
  return 'no'

def write(fileout,recs,tranout):
 tranin = 'slp1'
 n = 0
 nyes = 0
 nno = 0
 with codecs.open(fileout,"w","utf-8") as f:
  for irec,rec in enumerate(recs):
   entry = rec.entry
   upasargas = rec.upasargas
   preverbs = rec.preverbs
   mwpreverbs = rec.mwpreverbs
   mwpreverbs_found = rec.mwpreverbs_found
   mwpreverbs_parse = rec.mwpreverbs_parse
   k1 = entry.metad['k1']  
   L =  entry.metad['L']
   k2 = entry.metad['k2']
   #code = rec.code
   if rec.mw== '?': #None:
    mw = '?'
   elif rec.mw== k1:
    mw = rec.mw+ ' (same)'
   else:
    mw = rec.mw+ ' (diff)'
   out1 = ';; Case %04d: L=%s, k1=%s, k2=%s, #upasargas=%s, mw=%s' %(irec+1,L,k1,k2,len(upasargas),mw)
   if len(upasargas) == 0:
    f.write(out1+'\n')
    continue
   #add 1 more field to first line
   iyes = len([mwfound for mwfound in mwpreverbs_found if mwfound])
   ino  = len([mwfound for mwfound in mwpreverbs_found if not mwfound])
   out1 = ';; Case %04d: L=%s, k1=%s, k2=%s, #upasargas=%s (%s/%s), mw=%s' %(irec+1,L,k1,k2,len(upasargas),iyes,ino,mw)
   outarr = []
   outarr.append(out1)
   # one line for each upasarga
   for iupa,upa in enumerate(upasargas):
    icase = iupa + 1
    preverb = preverbs[iupa]
    mwpreverb = mwpreverbs[iupa]
    mwfound = mwpreverbs_found[iupa]
    if mwfound:
     nyes = nyes + 1
     parse = mwpreverbs_parse[iupa]
    else:
     nno = nno + 1
     parse = ''
    outarr.append('%02d %10s %10s %20s %20s %s %s'%(icase,upa,k1,preverb,mwpreverb,yesno(mwfound),parse))
   outarr.append(';')
   for out in outarr:
    f.write(out + '\n')
   n = n + 1
 print(n,"records written to",fileout)
 print(nyes,"mwpreverb spellings found")
 print(nno,"mwpreverb spellings NOT found")

class Vcpverb(object):
 def __init__(self,line):
  line = line.rstrip()
  self.line = line
  m = re.search(r'L=([^,]*), k1=([^,]*), k2=([^,]*), mw=(.*)$',line)
  self.L,self.k1,self.k2,self.mw = m.group(1),m.group(2),m.group(3),m.group(4)
  self.upasargas = []
  self.upasargas_raw = []
  self.entry = None
  self.preverbs = []
  self.mwpreverbs = []
  self.mwpreverbs_found = []
  self.mwpreverbs_parse = []

def init_vcpverbs(filein):
 with codecs.open(filein,"r","utf-8") as f:
  recs = [Vcpverb(x) for x in f if x.startswith(';; Case')]
 print(len(recs),"records read from",filein)
 return recs

def find_entries(recs,entries):
 # dictionary for entries
 d = {}
 for entry in entries:
  d[entry.metad['L']]= entry
 # 
 for irec,rec in enumerate(recs):
  L = rec.L
  try:
   entry = d[L]
   rec.entry = entry
   entry.marked = True
  except:
   print('find_entries. bad L=',rec.L)
   print('record # ',irec+1)
   print('  line = ',rec.line)
   exit(1)

def upasarga_join(a,b):
 if (a,b) == ('nis','nira'):  # kf, line 195622 page 2170b
  return 'nir'
 if (a,b) == ('nis','nir'):  # kfza, line 197996 page 2196
  # also kzipa, jYA
  return 'nir'
 if (a,b) == ('pra','ni'):
  return 'praRi'
 if (a,b) == ('uda','graha'):
  return 'ud'
 #if (a,b) == ('sam','ni'):
 # return sanni
 a1 = a[0:-1]
 a2 = a[-1]
 b1 = b[0]
 b2 = b[1:]
 if (a2,b1) in sandhimap:
  c = sandhimap[(a2,b1)]
  return a1+c+b2
 return a+b
  
def  map_upasarga(u):
 if '+' not in u:
  return u
 if u.startswith('ava + avagame'):  # line 160527, L=12456, k1=kala
  return 'ava'
 parts = re.split(r'[ +]+',u)
 ans = parts[0]
 for i,part in enumerate(parts[1:]):
  ans = upasarga_join(ans,part)
 return ans

class Upasarga(object):
 def __init__(self,raw,joined):
  self.raw = raw
  self.joined = joined
  self.count = 0

def find_upasargas(recs):
 nrec = 0
 nupa = 0
 uarr = {} # distinct upasargas count
 for rec in recs:
  entry = rec.entry
  upasargas = []
  upasargas_raw = []
  lines = entry.datalines
  for iline,line in enumerate(lines):
   m = re.search(r'^<HI>([a-zA-Z +]+) [+] ',line)
   if not m:
    continue
   upasarga_raw = m.group(1)
   if upasarga_raw != None:
    upasarga = map_upasarga(upasarga_raw)
    upasargas.append(upasarga)
    upasargas_raw.append(upasarga_raw)
    if upasarga_raw not in uarr:
     urec = Upasarga(upasarga_raw,upasarga)
     uarr[upasarga_raw] = urec
    else:
     urec = uarr[upasarga_raw]
    urec.count = urec.count + 1
    if False:  # dbg
     k1 = entry.metad['k1']
     L  = entry.metad['L']
     linenum = entry.linenum1 + iline + 1
     out = '%7d:%s:%s:%s:%s' %(linenum,k1,upasarga_raw,upasarga,line)
     if '+' in upasarga_raw:
      out = '!' + out
     print(out)
   rec.upasargas = upasargas
  if len(upasargas) > 0:
   nrec = nrec + 1
   nupa = nupa + len(upasargas)
 print(nupa,"upasargas found in",nrec,"entries")
 if False: # dbg
  keys = sorted(uarr.keys())
  for uraw in keys:
   rec = uarr[uraw]
   print('%02d %s = %s' %(rec.count,rec.raw,rec.joined))

sandhimap = {
 ('i','a'):'ya',
 ('i','A'):'yA',
 ('i','i'):'I',
 ('i','I'):'I',
 ('i','u'):'yu',
 ('i','U'):'yU',
 ('i','f'):'yf',
 ('i','F'):'yF',
 ('i','e'):'ye',
 ('i','E'):'yE',
 ('i','o'):'yo',
 ('i','O'):'yO',

 ('u','a'):'va',
 ('u','A'):'vA',
 ('u','i'):'vi',
 ('u','I'):'vI',
 ('u','u'):'U',
 ('u','U'):'U',
 ('u','f'):'vf',
 ('u','F'):'vF',
 ('u','e'):'ve',
 ('u','E'):'vE',
 ('u','o'):'vo',
 ('u','O'):'vO',

 ('a','a'):'A',
 ('a','A'):'A',
 ('A','a'):'A',
 ('A','A'):'A',
 
 ('a','i'):'e',
 ('A','i'):'e',
 ('a','I'):'e',
 ('A','I'):'e',
 
 ('a','u'):'o',
 ('A','u'):'o',
 ('a','U'):'o',
 ('A','U'):'o',
 
 ('a','f'):'Ar',
 ('A','f'):'Ar',
 ('a','e'):'e',
 ('d','s'):'ts',
 ('a','C'):'acC', # pra+Cad = pracCad
 ('i','C'):'icC',
 ('d','q'):'qq',  # ud + qI
 ('d','k'):'tk',
 ('d','K'):'tK',
 ('d','c'):'tc',
 ('d','C'):'tC',
 ('d','w'):'tw',
 ('d','W'):'tW',
 ('d','t'):'tt',
 ('d','T'):'tT',
 ('d','p'):'tp',
 ('d','P'):'tP',
 ('d','s'):'ts',
 ('d','n'):'nn',

 ('i','st'):'izw',
 ('s','h'):'rh', # nis + han -> nirhan
 ('m','s'):'Ms', # sam + saYj -> saMsaYj
 ('m','S'):'MS',
 ('m','k'):'Mk',
 ('m','K'):'MK',
 ('m','c'):'Mc',
 ('m','C'):'MC',
 ('m','w'):'Mw',
 ('m','W'):'MW',
 ('m','t'):'Mt',
 ('m','T'):'MT',
 ('m','p'):'Mp',
 ('m','P'):'MP',

 ('m','v'):'Mv',
 ('m','l'):'Ml',
 ('m','r'):'Mr',
 ('m','n'):'Mn',
 
 ('s','k'):'zk', # nis + kf -> nizkf
 ('s','g'):'rg',
 ('s','G'):'rG',
 ('s','j'):'rj',
 ('s','q'):'rq',
 ('s','d'):'rd',
 ('s','D'):'rD',
 ('s','b'):'rd',
 ('s','B'):'rB',
 ('s','m'):'rm',
 ('s','n'):'rn',
 ('d','l'):'ll',
 ('d','h'):'dD',
 ('d','S'):'cC',
 

}
def join_prefix_verb(pfx,root):
 if pfx.endswith('t'):  
  pfx = pfx[0:-1] + 'd' # ud, od
 if pfx.endswith('ud') and (root == 'sTA'):
  return pfx[0:-2] + 'ut' + 'TA'  # ud + sTA = utTA
 if (pfx == 'saMpra') and (root in ['nad','nam','naS']):
  pfx = 'sampra'
  root = 'R' + root[1:]
  return pfx + root
 if (pfx == 'pra') and (root == 'nakz'):
  return 'pranakz' # odd, since mw has aBipraRakz
 pfx1,pfx2 = (pfx[0:-1],pfx[-1])
 root1,root2 = (root[0],root[1:])
 if (pfx2,root1) in sandhimap:
  return pfx1 + sandhimap[(pfx2,root1)] + root2
 if len(root) > 1:
  root1,root2 = (root[0:2],root[2:])
  if (pfx2,root1) in sandhimap:
   return pfx1 + sandhimap[(pfx2,root1)] + root2
 if root == 'i':
  if pfx == 'dus':
   return 'duri'
  if pfx == 'nis':
   return 'niri'
 if 'saMpra' in pfx:
  pfx = pfx.replace('saMpra','sampra')
  return pfx + root
 if  pfx.endswith(('pari','pra')) and root.startswith('n'):
  return pfx + 'R' + root[1:]  # pra + nad -> praRad
 if pfx.endswith('nis') and root.startswith(('a','I','u','U')):
  pfx = pfx.replace('nis','nir')
  return pfx + root
 ans = pfx + root
 d = {'duscar':'duScar'}
  
 if ans in d:
  ans = d[ans]
 return ans

mwpreverb_adjustments = {
 'apAYc':'apAc',
 'parAn':'parAR',
 'nisf':'nirf',
 'nisfC':'nirfC',
 'atyarj':'atyfj',
 'nirnI':'nirRI',
 'parAnI':'parARI',
 'paryAnI':'paryARI',
 'pratiparAnI':'pratiparARI',
 'vinirnI':'vinirRI',
 'sampranI':'sampraRI',
 'aByutci':'aByucci',
 'aByujji':'aByujji',
 'niscft':'niScft',
 'nissic':'niHzic',
 'nissiD':'niHziD',
 'sampratisiD':'sampratiziD',
 'nizkzip':'niHkzip',
 'antarcar':'antaScar',
 'niscar':'niScar',
 'protcar':'proccar',
 'viniscar':'viniScar',
 'niscat':'niScat',
 'nisci':'niSci',
 'vinisci':'viniSci',
 'prodhA':'prodDA',
 'antarCid':'antaSCid',
 'anuCid':'anucCid',
 'apotCad':'apocCad',
 'ACad':'AcCad',
 'samACad':'samAcCad',
 'ACid':'AcCid',
 'avACid':'avAcCid',
 'samACid':'samAcCid',
 'ACfd':'AcCfd',
 'anuCo':'anucCo',
 'ACo':'AcCo',
 'nisstan':'niHzwan',
 'vinisstan':'vinizwan',
 'anustu':'anuzwu',
 'anustuB':'anuzwuB',
 'avastamB':'avazwamB',
 'utstamB':'uttamB',
 'paryavastamB':'paryavazwamB',
 'pratyutstamB':'pratyuttamB',
 'aBizwf':'aBistf',
 'nizwf':'nistf',
 'anUtsTA':'anUtTA',
 'upotsTA':'upotTA',
 'nissTA':'niHzWA',
 'protsTA':'protTA',
 'sampratisTA':'sampratizWA',
 'nirkAS':'nizkAS',
 'nirkuz':'nizkuz',
 'nirkas':'nizkas',
 'nirkf':'nizkf',
 'nirkfz':'nizkfz',
 'nirKan':'nizKan',
 'acCagam':'acCAgam',
 'paryAnah':'paryARah',
 'vipratisiD':'vipratiziD',
 'parAnud':'parARud',
 'purarDA':'puroDA',
 'anuviso':'anuvizo',
 'nirnij':'nirRij',
 #'':'',
 #'':'',

}
def adjust_mwpreverb(preverb,mwdict):
 if preverb in mwpreverb_adjustments:
  x = mwpreverb_adjustments[preverb]
  if x in mwdict:
   return x
 if preverb in mwdict:
  return preverb # no adjustment needed
 if re.search(r'sa[mM]p',preverb):
  x = preverb.replace('saMp','samp')
  if x in mwdict:
   return x
  x = preverb.replace('samp','saMp')
  if x in mwdict:
   return x
  return preverb
 if re.search(r'.*r.*n$',preverb):  #parAn -> paraR, etc
  x = preverb[0:-1]+'R'
  if x in mwdict:
   return x
 if 'samh' in preverb:
  x = preverb.replace('samh','saMh')
  if x in mwdict:
   return x
 if 'utc' in preverb:
  x = preverb.replace('utc','ucc')
  if x in mwdict:
   return x
 if 'utC' in preverb:
  x = preverb.replace('utC','ucC')
  if x in mwdict:
   return x
 if 'udj' in preverb:
  x = preverb.replace('udj','ujj')
  if x in mwdict:
   return x
 if preverb.endswith('isad'):
  x = re.sub(r'isad$','izad',preverb)
  if x in mwdict:
   return x
 if re.search(r'is',preverb):
  x = re.sub(r'is',r'iz',preverb)
  if x in mwdict:
   return x
 if re.search(r'isT',preverb):
  x = re.sub(r'isT',r'izW',preverb)
  if x in mwdict:
   return x
 if re.search(r'us',preverb):
  x = re.sub(r'us',r'uz',preverb)
  if x in mwdict:
   return x
 if re.search(r'usT',preverb):
  x = re.sub(r'usT',r'uzW',preverb)
  if x in mwdict:
   return x
 if re.search(r'niss',preverb):
  x = re.sub(r'niss',r'niHs',preverb)
  if x in mwdict:
   return x
 if re.search(r'nisS',preverb):
  x = re.sub(r'nisS',r'niHS',preverb)
  if x in mwdict:
   return x
 if re.search(r'niszW',preverb):
  x = re.sub(r'niszW',r'niHzW',preverb)
  if x in mwdict:
   return x
 if re.search(r'nisv',preverb):
  x = re.sub(r'nisv',r'nirv',preverb)
  if x in mwdict:
   return x
 if re.search(r'udm',preverb):
  x = re.sub(r'udm',r'unm',preverb)
  if x in mwdict:
   return x
 if re.search(r'udh',preverb):
  x = re.sub(r'udh',r'udD',preverb)
  if x in mwdict:
   return x
 if re.search(r'sam[gGjJdDbByrlvSzs]',preverb):
  x = re.sub(r'sam([gGjJdDbByrlvSzs])',r'saM\1',preverb)
  if x in mwdict:
   return x
 if re.search(r'antar',preverb):
  x = re.sub(r'antar',r'antaH',preverb)
  if x in mwdict:
   return x
 if preverb.endswith(('kf','df','pf')):
  x = preverb[0:-1]+'F'
  if x in mwdict:
   return x
 return preverb

def join_upasargas(recs,mwpreverbs_dict):
 for rec in recs:
  upasargas = rec.upasargas
  if len(upasargas) == 0:
   continue
  if rec.mw == '?':
   print(len(upasargas),'upasargas, but no mw root',rec.line)
   continue
  
  #mwrec = rec.mwrec
  k1 = rec.k1
  kmw = rec.mw
  rec.mwpreverbs = []
  rec.preverbs = []
  rec.mwpreverbs_found = []
  rec.mwpreverbs_parse = []
  for u in upasargas:
   vcp_preverb = join_prefix_verb(u,k1)
   if False and (k1 == 'kzip'):
    print('vcp',u,k1,vcp_preverb)
   rec.preverbs.append(vcp_preverb)
   mw_preverb0 = join_prefix_verb(u,kmw)
   mw_preverb = adjust_mwpreverb(mw_preverb0,mwpreverbs_dict)
   if False and (k1 == 'kzip'):
    print('mw',u,kmw,mw_preverb0,mw_preverb)
   rec.mwpreverbs.append(mw_preverb)
   if mw_preverb in mwpreverbs_dict:
    mwprerec = mwpreverbs_dict[mw_preverb]
    mwprerec.used = True
    rec.mwpreverbs_found.append(True)
    rec.mwpreverbs_parse.append(mwprerec.parse)
   else:
    rec.mwpreverbs_found.append(False)
    rec.mwpreverbs_parse.append(None)

def skipmw_unused(rec):
 if rec.line.endswith(('+kf','+BU')):
  return True
 if rec.k1 == rec.parse.replace('+',''):
  return True
 return False

def write_mw_unused(mwrecs):
 fileout = 'preverb1_temp_mw_unused.txt'
 n = 0
 with codecs.open(fileout,'w','utf-8') as f:
  for rec in mwrecs:
   if not rec.used:
    out = rec.line
    if skipmw_unused(rec):
     continue
    n = n + 1
    f.write(out+'\n')
 print(n,"records written to",fileout)

if __name__=="__main__": 
 tranout = sys.argv[1] # deva or slp1
 filein = sys.argv[2] #  xxx.txt (path to digitization of xxx
 filein1 = sys.argv[3] # vcp_verb_filter_map.txt
 filein2 = sys.argv[4] # mwverbs1
 fileout = sys.argv[5] # 
 entries = init_entries(filein)
 recs = init_vcpverbs(filein1)
 mwrecs,mwdict = init_mwverbs(filein2)  # mw preverbs
 find_entries(recs,entries)  # assign entry to each vcp verb record
 find_upasargas(recs)  # get list of upasargas
 join_upasargas(recs,mwdict)
 write(fileout,recs,tranout)
 write_mw_unused(mwrecs)
