# coding=utf-8
""" Dhaval Patel. 09 September 2021
python3 inputfile inTran outputfile outTran
e.g. python3 input.txt slp1 output.txt devanagari
inTran and outTran can take any valid transliteration scheme.
See indic-transliteration package for transliteration scheme details.
"""
import sys
import codecs
from indic_transliteration import sanscript


if __name__ == "__main__":
	filein = sys.argv[1]
	inTran = sys.argv[2]
	fileout = sys.argv[3]
	outTran = sys.argv[4]
	with codecs.open(filein, 'r', 'utf-8') as fin:
		data = fin.read()
		data = sanscript.transliterate(data, inTran, outTran)
		with codecs.open(fileout, 'w', 'utf-8') as fout:
			fout.write(data)
