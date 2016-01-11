#!/usr/bin/env python
# This Python file uses the following encoding: utf-8
from __future__ import division
import re, sys, codecs
def distancescore(s1,s2):
	alphabet = 'aAiIuUfFxeoEOHhyvrlYmNRnMJBGQDjbgqdKPCWTcwtvkpSzs'
	lenalpha = len(alphabet)
	corrnum = range(0,len(alphabet))
	s1score = 0
	for letter in s1:
		s1score += corrnum[alphabet.index(letter)] / lenalpha
	s2score = 0
	for letter in s2:
		s2score += corrnum[alphabet.index(letter)] / lenalpha
	distance = abs(s1score-s2score)
	return distance
print distancescore('Ta','pa')
print distancescore('Ta','Ti')