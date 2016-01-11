"""hw1.py  ejf Oct 1,2013 for vcp
 Usage - python hw1_dhaval.py vcphw0.txt vcphw1_dhaval.txt vcphw1_dhaval_note.txt
 Read  hw0.txt, whose lines were created with:
 out = "%s:%s:%s,%s" %(page,hw,l1,l2)

 'Normalize' all headword spellings, but still leave in HK.
 Then output the same format, using the normalized headword
 Here are the normalizations:
 - Change 'D.' to 'D'
 - Remove parenthetical parts (these represent alternate spellings)
 - Remove {??}  (unreadable text)
 - Remove space
 - Remove ' (avagraha)
 - Remove trailing ',' or '-'
 - Change ira--IrSAyAM to ira
 Jan 30, 2014 read/write utf-8. 
 Nov 20, 2014.  Manually adjust some 'UrdD' headwords
"""
import re
import sys
import codecs
import levenshtein
import alphabetdistance
hw_override = {'UrdDa(rdDva)':'UrdDva',
  'UrdDa(rdDva)kaca':'UrdDvakaca',
  'UrdDa(rdDva)kaRWa':'UrdDvakaRWa',
  'UrdDa(rdDva)karmman':'UrdDvakarmman',
  'UrdDa(rdDva)manTin':'UrdDvamanTin',
  'UrdDa(rdDva)mAna':'UrdDvamAna',
  'UrdDa(dDva)ka':'UrdDvaka',
  'kuve(be)ra':'kubera',
  'Karva(rba)':'Karba',
  'navava(ba)DU':'navabaDU' ,
  'purU(ru)ravasa':'puru(rU)ravasa',
  'pUrRakU(ku)wa':'pUrRaku(kU)wa'
  }
def bracketseparator(filein):
 fin = codecs.open(filein,'r','utf-8')
 fout = codecs.open('bracketwords.txt','w','utf-8')
 data = fin.readlines()
 counter = 0
 for hw in data:
  hw = hw.strip()
  if re.search('\(.*\)',hw):
   fout.write(hw+"\n")
   counter += 1
 print counter, "words have brackets and are put in bracketwords.txt"
 fout.close()
def separator(hw):
 hw = hw.strip()
 page,hw,lines = hw.split(':')
 l1,l2 = lines.split(',')
 return (page,hw,l1,l2)
def glueto(hw):
	global counter1, counter2
	hw = hw.replace(' ','')
	hw = hw.replace('*','')
	m = re.search('(.*)[(](.+)[)](.*)',hw)
	pre, mid, post = re.sub('[^a-zA-Z]','',m.group(1)), re.sub('[^a-zA-Z]','',m.group(2)), re.sub('[^a-zA-Z]','',m.group(3))
	# decide the place to change
	print pre, mid, post
	prelev = levenshtein.levenshtein(pre[-len(mid):],mid)
	postlev = levenshtein.levenshtein(post[:len(mid)],mid)
	out = hw+":404"
	if re.search('.{1}[(].{1}[)]',hw): # a(A)nEpuRa
		#print hw, "5"
		out = mid+post+":5"
	elif re.search('abBr.{1}[(]Br.{1}[)]',hw): # abBra(Bra)puzpa, abBro(Bro)tTa
		#print hw, "6"
		out = "a"+mid+post+":6"
	elif re.search('UrdDa[(]rdDva[)]',hw): # abBra(Bra)puzpa, abBro(Bro)tTa
		#print hw, "7"
		out = "UrdDva"+post+":7"
	elif prelev < postlev:
		if pre[-len(mid):].startswith(mid[0]) and len(pre)>=len(mid) and not pre[-len(mid):]==mid:
			#print hw, "1"
			out = pre[:-len(mid)]+mid+post+":1"
		elif pre[-len(mid):].endswith(mid[-1]) and len(pre)>=len(mid) and not pre[-len(mid):]==mid:
			#print hw, "2"
			out = pre[:-len(mid)]+mid+post+":2"
	elif postlev < prelev:
		if post[:len(mid)].startswith(mid[0]) and len(post)>=len(mid) and not post[:len(mid)]==mid:
			#print hw, "3"
			out = pre+mid+post[len(mid):]+":3"
		elif post[:len(mid)].endswith(mid[-1]) and len(post)>=len(mid) and not post[:len(mid)]==mid:
			#print hw, "4"
			out = pre+mid+post[len(mid):]+":4"
	elif alphabetdistance.distancescore(pre[:-len(mid)],mid) < alphabetdistance.distancescore(post[:len(mid)],mid):
		print hw, "8"
		out = pre[:-len(mid)]+mid+post+":8"
	elif alphabetdistance.distancescore(pre[:-len(mid)],mid) > alphabetdistance.distancescore(post[:len(mid)],mid):
		print hw, "9"
		out = pre+mid+post[len(mid):]+":9"
	return out
def bracketanalyser(filein):
 fin = codecs.open(filein,'r','utf-8')
 midbracketfile = codecs.open('midbracket.txt','w','utf-8') # There is no entry which has '(' at the starting.
 endbracketfile = codecs.open('endbracket.txt','w','utf-8')
 data = fin.readlines()
 fin.close()
 incount = len(data)
 counter1 = 0
 counter2 = 0
 for hw in data:
  hw = hw.strip()
  if re.search('[:].+[(].+[)].+[:]',hw):
   (page,headword,l1,l2) = separator(hw)
   out = page+":"+headword+":"+l1+","+l2+":"+glueto(headword)
   midbracketfile.write(out+"\n")
   counter1 += 1
  elif re.search('[)][:]',hw):
   endbracketfile.write(hw+"\n")
   counter2 += 1
 print counter1, "entries written to midbracket.txt"
 print counter2, "entries written to endbracket.txt"
 print counter1+counter2, "/", incount, "entries written to respective files"
 midbracketfile.close()
 endbracketfile.close()
 fin = codecs.open('midbracket.txt','r','utf-8')
 data = fin.readlines()
 fin.close()
 hwlistfile = codecs.open('../data/hw1.txt','r','utf-8')
 validatedfile = codecs.open('validated.txt','w','utf-8')
 nonvalidatedfile = codecs.open('nonvalidated.txt','w','utf-8')
 basehwlist = [member.strip() for member in hwlistfile.readlines()]
 print "validating the suggested items against the list of headwords in ../data/hw1.txt"
 validatecounter = 0
 nonvalidatecounter = 0
 for line in data:
  line=line.strip()
  (page,hw,l1l2,suggest,code) = line.split(':')
  if suggest in basehwlist and not code=="404":
   validatedfile.write(line+"\n")
   validatecounter += 1
  elif re.search('v.*[(].*b.*[)]',hw) and suggest.replace('b','v') in basehwlist: # ava(ba)hitTA, pUrva(rba)karmman etc specific for bengal dictionaries
   validatedfile.write(line+"\n")
   validatecounter += 1
  elif re.search('b.*[(].*v.*[)]',hw) and suggest.replace('v','b') in basehwlist: # karbU(rvU)ra etc specific for bengal dictionaries
   validatedfile.write(line+"\n")
   validatecounter += 1
  elif re.search('[(].*b.*[)].*v.*',hw) and suggest.replace('b','v') in basehwlist: # ava(ba)hitTA, pUrva(rba)karmman etc specific for bengal dictionaries
   validatedfile.write(line+"\n")
   validatecounter += 1
  elif re.search('[(].*v.*[)].*b.*',hw) and suggest.replace('v','b') in basehwlist: # karbU(rvU)ra etc specific for bengal dictionaries
   validatedfile.write(line+"\n")
   validatecounter += 1
  elif re.search('S.*[(].*s.*[)]',hw) and suggest.replace('s','S') in basehwlist: # kASU(sU)taro etc
   validatedfile.write(line+"\n")
   validatecounter += 1
  elif re.search('S.*[(].*z.*[)]',hw) and suggest.replace('z','S') in basehwlist: # kASU(sU)taro etc
   validatedfile.write(line+"\n")
   validatecounter += 1
  else:
   nonvalidatedfile.write(line+"\n")
   nonvalidatecounter += 1
 print validatecounter, "validated entries"
 print nonvalidatecounter, "non validated entries"
   
def hw_normalize(hw):
 hw0 = hw
 if hw in hw_override:
  print "Note: %s -> %s" %(hw,hw_override[hw])
  hw = hw_override[hw]
 hw = re.sub(r"[*]","",hw) # special nukta coding
 hw = re.sub(r"\(.*?\)","",hw)
 hw = re.sub(r"{[?][?]}","",hw)
 hw = re.sub(r" ","",hw)
 hw = re.sub(r"'","",hw)
 hw = re.sub(r"[,]$","",hw)
 hw = re.sub(r"[-]+$","",hw)
 hw = re.sub(r"ira--IrzAyAM","ira",hw)
 #hw = re.sub(r"M~","M",hw) # candra-bindu changed to M
 #hw = re.sub(r"[^a-z0-9]$","",hw)
 m = re.search(r'([^a-zA-Z])',hw)
 if m:
  c = m.group(1)
  cint = ord(c)
  out = "headword '%s' (%s) has unexpected character '%s' = %s" %(hw,hw0,c,cint)
  print out.encode('utf-8')
 return hw
def hw1(filein,fileout,filenote):
 f = codecs.open(filein,encoding='utf-8',mode='r')
 fout = codecs.open(fileout,'w','utf-8')
 fnote = codecs.open(filenote,'w','utf-8')
 n = 0
 nnote = 0
 nout = 0 # number of headword lines written to output
 for line in f:
  n = n+1
  line = line.strip() # remove starting or ending whitespace
  (pagecol,hw0,line12) = re.split(':',line)
 
  hw = hw_normalize(hw0)
  out = "%s:%s:%s" %(pagecol,hw,line12)
  fout.write("%s\n" % out);
  nout = nout + 1
  if ((hw != hw0) and ((hw+"-")!=hw0)):
   out = "%s:  '%s' => '%s'  :%s" %(pagecol,hw0,hw,line12)
   fnote.write("%s\n" % out);
   nnote = nnote + 1
 f.close()
 fout.close()
 fnote.close()
 print "file %s has %s lines" % (filein,n)
 print "%s headwords written to file %s" % (nout,fileout)
 print "%s headwords with normalization changes written to %s" % (nnote,filenote)
#-----------------------------------------------------
if __name__=="__main__":
 filein=sys.argv[1] 
 fileout =sys.argv[2] 
 filenote =sys.argv[3]
 #hw1(filein,fileout,filenote)
 bracketseparator(filein)
 bracketanalyser('bracketwords.txt')
