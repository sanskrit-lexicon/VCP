#-*- coding:utf-8 -*-
"""analyze_preverb.py
 
 
"""
from __future__ import print_function
import sys, re,codecs
from parseheadline import parseheadline

class Entry(object):
 Ldict = {}
 def __init__(self,lines,linenum1,linenum2):
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
  self.verb = None  # value of verb attribute root|genuineroot|pre|gati|nom
  self.parse = None  # string value of parse attribute (for pre/gati
  self.cps  = None  # string value of cp attribute
  
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

class Upasarga(object):
 def __init__(self,raw,joined):
  self.raw = raw
  self.joined = joined
  self.count = 0

known_upasargas = [
 'anu','aBi','aDi','ava','ati','apa',
 'A',
 'ud','upa',
 'dur',
 'nir',
 'parA','pari','pra','prati',
 'vi',
 'sam',

 'anu + pra',
 'vi + ni',
 'pari + upa',
 'pari + sam',
 'sam + upa',
 'prati + upa',
]
def known_upasarga(x):
 if x in known_upasargas:
  return x
 else:
  return None

#class Change(object):
# def __init__(self,):

def get_upasarga_raw(line):
 if not line.startswith('<HI>'):
  return None
 regex = r'<HI>([a-zA-Z]+)--([a-zA-Z]+)--'
 m = re.search(regex,line)
 if m:
  x = "%s + %s" %(m.group(1),m.group(2))
  if known_upasarga(x) == None:
   return None
  newline = re.sub(regex,'<HI>' + x + ' + ',line)
  return newline
 regex = r'<HI>([a-zA-Z]+)--'
 m = re.search(regex,line)
 if m:
  x = m.group(1)
  if known_upasarga(x) == None:
   return None
  newline = re.sub(regex,'<HI>' + x + ' + ',line)
  return newline
 return None

def make_transactions(entries):
 ans = []
 case = 0
 for entry in entries:
  marks = []
  for iline,line in enumerate(entry.datalines):
   newline = get_upasarga_raw(line)
   if newline == None:
    continue 
   a = []
   L = entry.metad['L']
   k1 = entry.metad['k1']
   case = case + 1
   a.append(';Case %03d: L=%s, k1=%s' %(case,L,k1))
   linenum1 = entry.linenum1  # line number for meta line
   linenum = linenum1 + iline + 1
   a.append('%s old %s'%(linenum,line))
   a.append('%s new %s'%(linenum,newline))
   ans.append(a)
 return ans

def write(fileout,transactions):
 n = 0
 with codecs.open(fileout,"w","utf-8") as f:
  for transaction in transactions:
   outarr = transaction
   outarr.append(';')
   n = n + 1
   for out in outarr:
    f.write(out + '\n')
 print(n,"records written to",fileout)

if __name__=="__main__": 
 filein = sys.argv[1] #  xxx.txt (path to digitization of xxx
 #filein1 = sys.argv[2] 
 fileout = sys.argv[2] # 
 entries = init_entries(filein)
 #recs = init_preverb3(filein1)
 transactions = make_transactions(entries)

 write(fileout,transactions)
