# coding=utf-8
"""
The above coding=utf-8 is required in python2 versions, so the broken-bar
character in reHeadword is properly interpreted. 
See http://www.python.org/dev/peps/pep-0263/
headword.py contains the regular expression for recognizing headwords.
for vac.
Examples:
a#1<tab>
afRin<tab>
"""
#reHeadword = r'^(([^\t]+)#([0-9]+)\t)|(([^\t]+)\t)'
reHeadword = r'^([^\t#]+)'





