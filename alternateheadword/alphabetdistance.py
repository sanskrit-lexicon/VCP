#!/usr/bin/env python
# This Python file uses the following encoding: utf-8
from __future__ import division
import re, sys, codecs
def distancescore(s1,s2):
	"""
	presumes that s1 and s2 are of equal length as of now
	"""
	alphabet = 'aAiIuUfFxeoEOHhyvrlYmNRnMJBGQDjbgqdKPCWTcwtvkpSzs'
	lenalpha = len(alphabet)
	corrnum = range(0,len(alphabet))
	s1score = 0
	for letter in s1:
		s1score += corrnum[alphabet.index(letter)] / lenalpha
	s1score = s1score
	s2score = 0
	for letter in s2:
		s2score += corrnum[alphabet.index(letter)] / lenalpha
	s2score = s2score
	distance = abs(s1score-s2score)
	return distance
