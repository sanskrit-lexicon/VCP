""" utf8_to_cp1252.py Jan 16, 2014
 Does the inverse of the conversion done by cp1252_to_utf8.py
  
"""
import sys, re
cp1252 = {
    # from http://www.microsoft.com/typography/unicode/1252.htm
    u"\u20AC": "\x80", # EURO SIGN
    u"\u201A": "\x82", # SINGLE LOW-9 QUOTATION MARK
    u"\u0192": "\x83", # LATIN SMALL LETTER F WITH HOOK
    u"\u201E": "\x84", # DOUBLE LOW-9 QUOTATION MARK
    u"\u2026": "\x85", # HORIZONTAL ELLIPSIS
    u"\u2020": "\x86", # DAGGER
    u"\u2021": "\x87", # DOUBLE DAGGER
    u"\u02C6": "\x88", # MODIFIER LETTER CIRCUMFLEX ACCENT
    u"\u2030": "\x89", # PER MILLE SIGN
    u"\u0160": "\x8A", # LATIN CAPITAL LETTER S WITH CARON
    u"\u2039": "\x8B", # SINGLE LEFT-POINTING ANGLE QUOTATION MARK
    u"\u0152": "\x8C", # LATIN CAPITAL LIGATURE OE
    u"\u017D": "\x8E", # LATIN CAPITAL LETTER Z WITH CARON
    u"\u2018": "\x91", # LEFT SINGLE QUOTATION MARK
    u"\u2019": "\x92", # RIGHT SINGLE QUOTATION MARK
    u"\u201C": "\x93", # LEFT DOUBLE QUOTATION MARK
    u"\u201D": "\x94", # RIGHT DOUBLE QUOTATION MARK
    u"\u2022": "\x95", # BULLET
    u"\u2013": "\x96", # EN DASH
    u"\u2014": "\x97", # EM DASH
    u"\u02DC": "\x98", # SMALL TILDE
    u"\u2122": "\x99", # TRADE MARK SIGN
    u"\u0161": "\x9A", # LATIN SMALL LETTER S WITH CARON
    u"\u203A": "\x9B", # SINGLE RIGHT-POINTING ANGLE QUOTATION MARK
    u"\u0153": "\x9C", # LATIN SMALL LIGATURE OE
    u"\u017E": "\x9E", # LATIN SMALL LETTER Z WITH CARON
    u"\u0178": "\x9F"  # LATIN CAPITAL LETTER Y WITH DIAERESIS
}
#cp1252_rev = {}
#for k,v in cp1252.iteritems():
# cp1252_rev[v] = k
import unicodedata
def adjust_utf8(s):
 """ convert a string, changing extended ascii characters
     to &#xHHHH; form, taking into account cp1252 code conversions
 """
 out=[]
 for c in s:
  ic = ord(c)
  if (ic > 127):
   h = cp1252.get(c)
   if (not h):
    #h = "&#x%0.4X;?" % ic
    h = chr(ic) # does this get ascii?
  else:
   h = chr(ic)
  out.append(h)
 ans = ''.join(out)
 return ans


def make_ea(filein,fileout):
 # slurp txt file into list of lines
 import codecs
 f = codecs.open(filein,encoding='utf-8',mode='r')
 fout = open(fileout,'w')
 #fout = codecs.open(fileout,encoding='utf-8',mode='w')
 n = 0
 for line in f:
  n = n+1
  if n > 1000000:
   print "debug stopping"
   break
  line = line.strip() # remove starting or ending whitespace
  # construct output
  data = adjust_utf8(line)
  out = "%s\n" % data
  fout.write( out)
  # check that out is well-formed xml
 # write closing line
 fout.close()

if __name__=="__main__":
 filein = sys.argv[1] # X.txt
 fileout = sys.argv[2] # Y.txt
 make_ea(filein,fileout)
