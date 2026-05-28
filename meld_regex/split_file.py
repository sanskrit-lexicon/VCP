# coding=utf-8
""" Dhaval Patel. 13 February 2022
python3 split_file.py inputfile outputfolder length prefix
"""
import sys
import codecs
import os

def split_file(filein, outfolder, length, prefix):
	fin = codecs.open(filein, 'r', 'utf-8')
	cnt = 0
	length = int(length)
	for lin in fin:
		if cnt % length == 0:
			start = cnt
			p = '%06d' % cnt
			end = cnt + length
			q = '%06d' % end
			outfile = os.path.join(outfolder, prefix + '_' + str(p) + '_' + str(q) + '.txt')
			fout = codecs.open(outfile, 'w', 'utf-8')
			print(outfile)
		fout.write(lin)
		cnt += 1
	
if __name__ == "__main__":
	filein = sys.argv[1]
	outfolder = sys.argv[2]
	lines = sys.argv[3]
	prefix = sys.argv[4]
	split_file(filein, outfolder, lines, prefix)
