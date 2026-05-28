""" vcpjoinlines.py  Mar 4, 2014
   Utility program to 'convert' lines from vcp to one big line for
   inserting into vac.
   Some pre-adjustment is required:
   - remove <> <P>, etc.
   - change utf-8 double-quotes to <q>, </q>
   - remove [Page...]
"""
import sys
def vcpjoinines(filein,fileout):
 f = open(filein,'r')
 lines = []
 for line in f:
  line = line.rstrip('\n\r')
  if not line.endswith('-'):
   line = line + ' '
  lines.append(line)
 f.close()
 joinedline = ''.join(lines)
 fout = open(fileout,'w')
 fout.write(joinedline)
 fout.close()

if __name__=="__main__":
 filein = sys.argv[1] # 
 fileout = sys.argv[2] # 
 vcpjoinines(filein,fileout)
 
