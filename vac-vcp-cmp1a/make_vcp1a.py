# coding=utf-8
import sys,re,codecs

if __name__ == "__main__":
 filein = sys.argv[1]
 fileout = sys.argv[2]
 f = codecs.open(filein,"r","utf-8")
 fout = codecs.open(fileout,"w","utf-8")
 n = 0
 outlines = []
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
   continue
  newline = re.sub(r'^(.*?)¦',r'<HI>{@\1@}¦',line)
  outlines.append(newline)
 print(len(outlines))
 f.close()
 for line in outlines:
  fout.write(line+'\n')
 fout.close()
 
