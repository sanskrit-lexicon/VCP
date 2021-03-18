# coding=utf-8
import sys,re,codecs

if __name__ == "__main__":
 filein = sys.argv[1] # vcp.txt
 fileout = sys.argv[2] # vcp1a.txt
 fileout1 = sys.argv[3]  # map file
 f = codecs.open(filein,"r","utf-8")
 fout = codecs.open(fileout,"w","utf-8")
 fmap = codecs.open(fileout1,"w","utf-8")
 n = 0
 outlines = []
 outmap = []
 for iline,line in enumerate(f):
  line = line.rstrip('\r\n')
  if line.startswith(('<L>','<LEND>')):
   # skip meta lines
   continue
  if line.startswith('[Page'):
   page = line
   if outlines == []:
    continue
   else:
    outlines[-1] = outlines[-1] + ' ' + page # append page to previous line
    continue
  if iline == 1:
   newline = line + page
   outlines.append(newline)
   n = n + 1
   outmap.append('%s %s' %(n,iline+1))
   continue
  newline = re.sub(r'^(.*?)¦',r'<HI>{@\1@}¦',line)
  outlines.append(newline)
  n = n + 1
  outmap.append('%s %s' %(n,iline+1))
 print(len(outlines))
 f.close()
 for line in outlines:
  fout.write(line+'\n')
 fout.close()
 for line in outmap:
  fmap.write(line+'\n')
 fmap.close()
 
