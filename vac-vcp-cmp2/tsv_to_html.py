# coding=utf-8
""" tsv_to_html.py
    Dhaval Patel
    15 Jan 2021

    Usage - tsv_to_html.py tsvfile htmlfile
"""
import codecs
import sys


def link_entry(key, dictcode):
    link = "https://sanskrit-lexicon.uni-koeln.de/scans/csl-apidev/getword.php?dict=" + dictcode + "&key=" + key
    return '<a href="' + link + '" target="_blank">' + key + '</a>'


def link_pdf(key, dictcode):
    link = "https://sanskrit-lexicon.uni-koeln.de/scans/csl-apidev/servepdf.php?dict=" + dictcode + "&key=" + key
    return '<a href="' + link + '" target="_blank">' + key + '</a>'


def convert(tsvfile, htmlfile):
    fin = codecs.open(tsvfile, 'r', 'utf-8')
    fout = codecs.open(htmlfile, 'w', 'utf-8')
    fout.write("<!DOCTYPE html>\n<html>\n<head>\n<title>Diff</title>\n<style>table, th, td {  border: 1px solid black;} table { width:100%; table-layout: fixed; overflow-wrap: break-word;}</style></head>\n")
    fout.write('<body>\n<table style="width:100%">')
    for lin in fin:
        fout.write("<tr>\n")
        lin = lin.rstrip()
        items = lin.split('\t')
        first = True
        for item in items:
            if first:
                fout.write("<td>" + link_entry(item, 'vcp') + "</td>\n")
                fout.write("<td>" + link_pdf(item, 'vcp') + "</td>\n")
                first = False
            else:
                fout.write("<td>" + item + "</td>\n")
        fout.write("</tr>\n")
    fout.write("</body>\n</html>")


if __name__ == "__main__":
    tsvfile = sys.argv[1]
    htmlfile = sys.argv[2]
    convert(tsvfile, htmlfile)
