# coding=utf-8
""" Dhaval Patel. 11 August 2021
python3 merge_corrected_file_with_vcp.py ../../../cologne/csl-orig/v02/vcp/vcp.txt vcp_first_10000.txt vcp_corrected_file.txt
"""
import sys
import codecs
import re


def strip_correction(corrin):
    """Return corrections as a list."""
    result = [lin.split(': vcp: ')[-1] for lin in corrin if ':?:' not in lin]
    result = [lin.replace('{@', '') for lin in result]
    result = [lin.replace('@}', '') for lin in result]
    result = [lin.replace('<HI>', '') for lin in result]
    result = [re.sub(r' \[Page.*\]$', '', lin) for lin in result]
    return result


if __name__ == "__main__":
    fin = codecs.open(sys.argv[1], 'r', 'utf-8')
    corrin = codecs.open(sys.argv[2], 'r', 'utf-8')
    fout = codecs.open(sys.argv[3], 'w', 'utf-8')
    corrected_data = strip_correction(corrin)
    corr_len = len(corrected_data)
    counter = 0
    for lin in fin:
        if lin.startswith('[Page'):
            fout.write(lin)
        elif lin.startswith('<H>'):
            fout.write(lin)
        elif lin.startswith('<L>'):
            fout.write(lin)
        elif lin.startswith('<LEND>'):
            fout.write(lin)
        elif counter < corr_len:
            lout = corrected_data[counter]
            counter += 1
            fout.write(lout)
        else:
            fout.write(lin)
