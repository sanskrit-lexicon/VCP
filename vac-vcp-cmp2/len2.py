# coding=utf-8
""" vac-vcp-cmp2/len2.py  Jan 15, 2021

    Usage - python3 len2.py vcp1.txt vac1.txt hwdiff.tsv len2.tsv

    Compare the data of vac1.txt and vcp1.txt.
    Highlight the different words for typo correction

    Requirements: simplediff (for diff highlighting)
"""
import sys
import codecs
import re
from collections import defaultdict
from simplediff import html_diff
from parseheadline import parseheadline


class Vac(object):
    def __init__(self, line):
        line = line.rstrip()
        self.keyraw, self.lnum, self.entryraw = line.split('\t')
        # aMSa#1 -> aMSa
        key = re.sub('#[0-9]+$', '', self.keyraw)
        # aMsa(se)BAra -> aMsaBAra
        key = re.sub(r'\([^)]*\)', '', key)
        self.key = key
        self.entry = trim_entry(self.entryraw)


class Vcp(object):
    def __init__(self, key1, entryraw, lnum, pc, key2):
        self.key = key1
        self.entryraw = entryraw
        self.lnum = lnum
        self.pc = pc
        self.key2 = key2
        self.entry = trim_entry(self.entryraw)


def trim_entry(entry):
    splt = entry.split('<page>')
    ent = splt[0]
    #  Remove line endings
    ent = re.sub(r'\n', ' ', ent)
    # Remove xml like tags
    ent = re.sub(r'<[^>]*>', '', ent)
    # Replace all non character items by a space
    ent = re.sub(r'[^a-zA-Z]', ' ', ent)
    # Only one space remains between words
    ent = re.sub(r'[ ]+', ' ', ent)
    # Remove preceding and trailing whitespaces
    ent = ent.lstrip()
    ent = ent.rstrip()
    return ent


def uniq(input):
    output = []
    outputset = set()
    for x in input:
        if x not in outputset:
            output.append(x)
            outputset.add(x)
    return output


def init_vac(vacfile):
    result = defaultdict(list)
    with codecs.open(vacfile, 'r', 'utf-8') as fin:
        for line in fin:
            vac = Vac(line)
            result[vac.key].append(vac)
    return result


def init_vcp(vcpfile):
    result = defaultdict(list)
    with codecs.open(vcpfile, 'r', 'utf-8') as fin:
        entryraw = ''
        startWrite = False
        for line in fin:
            if line.startswith('<L>'):
                meta = parseheadline(line)
                key1 = meta['k1']
                lnum = meta['L']
                pc = meta['pc']
                key2 = meta['k2']
                startWrite = True
            elif startWrite:
                entryraw += line
            if line.startswith('<LEND>'):
                vcp = Vcp(key1, entryraw, lnum, pc, key2)
                result[key1].append(vcp)
                entryraw = ''
                startWrite = False
    return result


def compare_dicts(vcprecs, vacrecs, hwdifffile, outputfile):
    fout = codecs.open(outputfile, 'w', 'utf-8')
    with codecs.open(hwdifffile, 'w', 'utf-8') as flog:
        keysToSearch = []
        keysToSearch += vcprecs.keys()
        keysToSearch += vacrecs.keys()
        keysToSearch = uniq(keysToSearch)
        keysToSearch = sorted(keysToSearch)

        for key in keysToSearch:
            if len(vcprecs[key]) != len(vacrecs[key]):
                print(key)
                # print(key, len(vcprecs[key]), len(vacrecs[key]))
                flog.write(key + '\t' + str(len(vcprecs[key])) + '\t' + str(len(vacrecs[key])) + '\n')

                """
                for vac in vacrecs[key]:
                    print('VAC', vac.entry)
                """
                joinedVacEntry = ' '.join([vac.entry for vac in vacrecs[key]])
                joinedVacEntry = trim_entry(joinedVacEntry)
                joinedVcpEntry = ' '.join([vcp.entry for vcp in vcprecs[key]])
                joinedVcpEntry = trim_entry(joinedVcpEntry)
                if joinedVcpEntry == '' or joinedVacEntry == '':
                    fout.write(key + '\t' + joinedVacEntry + '\t' + joinedVcpEntry + '\n')
                elif joinedVacEntry != joinedVcpEntry:
                    diff2 = html_diff(joinedVacEntry, joinedVcpEntry)
                    fout.write(key + '\t' + diff2 + '\t' + joinedVcpEntry + '\n')
    fout.close()


def create_html(diffTsvfile, htmlfile):
    fout = codecs.open(htmlfile, 'w', 'utf-8')
    with codecs.open(diffTsvFile, 'r', 'utf-8') as fin:
        for lin in fin:
            lin = lin.rstrip()


if __name__ == "__main__":
    vcpfile = sys.argv[1]
    vacfile = sys.argv[2]
    hwdifffile = sys.argv[3]
    outputfile = sys.argv[4]
    print('Initializing vcp file')
    vcprecs = init_vcp(vcpfile)
    # print(vcprecs)
    print('Initializing vac file')
    vacrecs = init_vac(vacfile)
    # print(vacrecs)
    print('Comparing the headwords.')
    compare_dicts(vcprecs, vacrecs, hwdifffile, outputfile)
