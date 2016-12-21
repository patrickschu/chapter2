# -*- coding: utf-8 -*-

import codecs
import re
import clustertools as ct
import time
from collections import defaultdict
import os



#; and spellings that represent prosody or nonlinguistic sounds, such as a “calling voice” (helloooo), laughter, and other (nonhuman) noises
def anyoftheseregex(regexstring):
	"""
	The anyofthesregex iterates over all instances with "+" in a regex to construct a new pattern.
	THe new pattern replaces one instance of + with a {2,}. 
	Thus, this will get us a string to match Hhello, Heeeeello but not Hheello.
	"""
	print "we run the anyoftheseregex on", regexstring
	#print regexstring.split("+")
	result=[i for i in regexstring.split("+") if i]
	outputregex=[]
	for number, item in enumerate(result):
		temp=[i for i in regexstring.split("+") if i]
		temp[number]=item+"{2,}"
		outputregex.append(temp)
		
	anyregex=")|(?:".join(["".join(i) for i in outputregex])
	#print "("+anyregex+")"
	return "(("+anyregex+"))"
	

def prosodycounter(input_dir):
	"""
	 
	Returns a list of lists where each list contains raw and per word counts.
	
	"""
	start=time.time()
	
	#creating the search terms
	prosodyitems=[
	"\s(\*(?:laugh|cough|smack|giggle)\*)\s",

	"\W([Ee][Rr])\W",

	"\W((?:[Hh][Aa]){1,}[Hh]?)\W",
	"\W((?:[Hh][Uu]){1,}[Hh]?)\W",
	"\W((?:[Hh][Ee]){2,}[Hh]?)\W",
	"\W([Hh][Oo]{2,})\W",
	"\W([Hh][Mm]{1,})\W",

	"\W([Hh]e+y{2,})\W",
	"\W([Hh]e{2,}[Yy]+)\W",
	"\W"+anyoftheseregex("[Hh]+[Ee]+[Ll][Ll]+[Oo]+")+"\W",

	"\W([Mm]{2,})\W",
	"\W((?:[Mm][Hh]){1,})\W",

	"\W([Ss][Oo]{2,})\W",

	"\W([Uu][Hh]+)\W",
	"\W([Uu][Mm]+)\W",

	"\W([Yy][Aa]+[Yy]+)\W",
	"\W([Yy]+[Aa]+[Hh]?)\W"
	]
	excludelist=[]
	
	#dicts to store results
	dicti=defaultdict(float)
	matchesdicti=defaultdict(list)
	results=[]
	
	prosody_list=[re.compile(i) for i in prosodyitems]
	print "{} items in the prosody_list, {} unique".format(len(prosody_list), len(set(prosody_list)))
	print [i.pattern for i in prosody_list]
	#iterate and match
	for dir in [i for i in os.listdir(input_dir) if not i.startswith(".")]:
		print dir
		for fili in [i for i in os.listdir(os.path.join(input_dir, dir)) if not i.startswith(".")][:1000]:
			with codecs.open(os.path.join(input_dir, dir, fili), "r", "utf-8") as inputtext:
				inputad=ct.adtextextractor(inputtext.read(), fili).lower()
			#result is a list of lists which contain matches for each regex/acronym
			wordcount=float(len(ct.tokenizer(inputad)))
			result=[([m for m in i.findall(inputad) if not m in excludelist], i.pattern) for i in prosody_list] 
			#print result
			results.append([(len(matches), len(matches)/wordcount) for matches, pattern in result])
			for matches, pattern in result:
				#print pattern
				#the dicti is {pattern:count, pattern: count, ...}
				dicti[pattern]=dicti[pattern]+len(matches)
				matchesdicti[pattern]=matchesdicti[pattern]+matches
	#print matchesdicti
	print [i for i in sorted(dicti, key=dicti.get, reverse=True)]
	#print "\n".join([":".join((i, str(dicti[i]), "|".join(set(matchesdicti[i])))) for i in sorted(dicti, key=dicti.get, reverse=True)])	

	end=time.time()
	print "This took us {} minutes".format((end-start)/60)
	# for u in [[x[0] for x in i] for i in results]:
		# print u
	print "shape of results, number of lists:", len(results),  "-- length of lists", set([len(i) for i in results])
	return [[x[0] for x in i] for i in results], [[x[1] for x in i] for i in results] 

prosodycounter('/home/ps22344/Downloads/craig_0208')	

#anyoftheseregex("[Hh]+[Ee]+[Ll][Ll]+[Oo]+")	
plus=[]
minus=[]

def listmaker():
	with codecs.open ("/home/ps22344/Downloads/chapter2/textfiles/non_standard_words_0920.txt", "r", "utf-8") as inputfile:
		for lini in inputfile.read().split(")\n(u"):
			print lini, "\n"
			ini=raw_input("X FOR YES ")
			if ini == "X":
				plus.append(lini)
			if ini == "ENDE":
				print plus
			else:
				minus.append(lini)