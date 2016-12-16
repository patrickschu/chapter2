"""
This compiles all the tools needed for extraction of e-grammar features as defined by Herring.
"""
# BE FLEXIBLE WITH INPUT DATA SET SO WE CAN USE FULL OR BALANCED
# BE SOMEWHAT FLEXIBLE IN HOW WE AGGRAGATE OVER FEATURES
# So we need dir as input
# do we want corpus counts as result or featurelists
# maybe: dict={feature:count, feature_2: count, ...}



import numpy as np
from string import punctuation
import re
import clustertools as ct
import time
import os
import codecs
from collections import defaultdict
import json 

###SECTION 1
###TYPOGRAPHY


def emoticonfinder(dir):
	"""
	THIS STILL NEEDS THE OUTPUT FUNCTION OF PUNCTFINDER
	The emoticonfinder takes a directory with corpus files as input. 
	It returns a list of lists with counts of each emoticon in each file in dir.
	Emoticons are read from file.
	list=[[x1feature1, x1feature2, ...], [x2feature1, x2feature2, ...]]
	We might consider making the file with emoticons an argument as well. 
	--- Original Source file is /Users/ps22344/Downloads/chapter2/current/emoticoncounter.py ---
	"""
	starttime=time.time()
	#creating a featuredict from file
	featuredict={}
	search_terms=[]
	results=[]
	resultdict=defaultdict(float)
	
	with codecs.open('/home/ps22344/Downloads/chapter2/textfiles/emolist_final_2.txt', "r", "utf-8") as inputtext:
		for line in inputtext.readlines():
			print line.rstrip("\n")
			search_terms.append(re.compile("\W("+re.escape(line.rstrip("\n"))+")(?: |<)"))
		
	for pati in [i for i in os.listdir(dir) if not i.startswith(".")]:
		print pati
		for fili in [i for i in os.listdir(os.path.join(dir, pati)) if not i.startswith(".")]:
			with codecs.open(os.path.join(dir, pati, fili), "r", "utf-8") as inputfili:
				inputad=ct.adtextextractor(inputfili.read(), fili)
			result=[k.findall(inputad) for k in search_terms]
			for no, item in enumerate(result):
				resultdict[no]=resultdict[no]+len(item)
			results.append([len(i) for i in result])
			# if 11 > sum([len(i) for i in result]) > 6:
				# for n, i in enumerate(result):
					# if len(i) > 0:
						# print search_terms[n].pattern, n,i
				# print os.path.join(dir, pati, fili), "\n"
				# os.system("cygstart "+os.path.join(dir, pati, fili))
			
	endtime=time.time()
	print "This took us {} minutes".format((endtime-starttime)/60)
	#print results
	print len(results), "files processed"
	print "\n\n"
	resultdict={search_terms[k].pattern:v for k,v in resultdict.items() if v > 0}
	for k in sorted(resultdict, key=resultdict.get, reverse=True):
		print k, resultdict[k]
	print "shape of results, number of lists:", len(results),  "-- length of lists", set([len(i) for i in results])
	return results
	

	"""
	The emoticonfinder takes a directory with corpus files as input. 
	We might consider making the file with emoticons an argument as well. 
	The emoticonfinder creates a list of relevant emoticons from a text file. 
	Then counts how often they occur in files in dir.
	--- Source file is /Users/ps22344/Downloads/chapter2/current/emoticoncounter.py ---
	"""
	starttime=time.time()
	#creating a featuredict from file
	featuredict={}
	with codecs.open('/Users/ps22344/Downloads/chapter2/textfiles/emolist_final.txt', "r", "utf-8") as inputtext:
		for line in inputtext.readlines():
			featuredict[line.rstrip("\n")]=0
	#test formatting
	for k in featuredict:
		if k.startswith(" "):
	for pati in [i for i in os.listdir(dir) if not i.startswith(".")]:
		print pati
		for fili in [i for i in os.listdir(os.path.join(dir, pati)) if not i.startswith(".")]:
			fili=codecs.open(os.path.join(dir, pati, fili), "r", "utf-8")
			inputad=ct.adtextextractor(fili.read(), fili)
			words=ct.tokenizer(inputad)
			for item in words:
				if item in featuredict:
					featuredict[item] = featuredict[item]+1
	print featuredict
	endtime=time.time()
	print "This took us {} minutes".format((endtime-starttime)/60)


def repeatedpunctuationfinder(dir):
	"""
	The repeatedpunctuationfinder uses string.punctuation to create a dictionary of regexes.
	These are used to identify non-Standard usage of punctuation. 
	Note how we hardcoded the ?!? variants into the punctuationdict from the start. 
	Iterates over files contained in dir.
	Returns two lists; first is absolute counts, the second relative counts	
	-- Source file is /Users/ps22344/Downloads/chapter2/current/punctuationcounter_0927.py ---
	"""
	starttime=time.time()
	#creating a featuredict from file
	results=[]
	resultdict=defaultdict(float)
	punctuationdict={
	re.compile(r"(?:\s|\w)(!\?|\?!)(?:\s|\w)"):0
	}

	for stringi in punctuation:
		print stringi, "-->", re.escape(stringi)
		punctuationdict[re.compile("((?:"+re.escape(stringi)+" ?){2,})")]=0	
	search_terms=punctuationdict.keys()
	for pati in [i for i in os.listdir(dir) if not i.startswith(".")]:
		print pati
		for fili in [i for i in os.listdir(os.path.join(dir, pati)) if not i.startswith(".")]:
			with codecs.open(os.path.join(dir, pati, fili), "r", "utf-8") as inputfili:
				inputad=ct.adtextextractor(inputfili.read(), fili)
			wordcount=float(len(ct.tokenizer(inputad)))
			result=[k.findall(inputad) for k in search_terms]
			for no, item in enumerate(result):
				resultdict[no]=resultdict[no]+len(item)
			results.append([(len(i), len(i)/wordcount) for i in result])
			print results
			if sum([len(i) for i in result]) > 80:
				for n, i in enumerate(result):
					 if len(i) > 0:
						 print search_terms[n].pattern, n,i, "len", len(i)
				print os.path.join(dir, pati, fili), "\n"
				os.system("cygstart "+os.path.join(dir, pati, fili))
			
	endtime=time.time()
	print "This took us {} minutes".format((endtime-starttime)/60)
	#print results
	print len(results), "files processed"
	print "\n\n"
	resultdict={search_terms[k].pattern:v for k,v in resultdict.items() if v > 0}
	for k in sorted(resultdict, key=resultdict.get, reverse=True):
		print k, resultdict[k]
	print "shape of results, number of lists:", len(results),  "-- length of lists", set([len(i) for i in results])
	#1st list is absolute counts, 2nd div by word count
	return [[x[0] for x in i] for i in results], [[x[1] for x in i] for i in results]
	"""
	The repeatedpunctuationfinder uses string.punctuation to create a dictionary of regexes.
	These are used to identify non-Standard usage of punctuation. 
	Note how we hardcoded the ?!? variants into the punctuationdict from the start. 
	The returned punctuationdict= {regex_object: count_of_matches, regex_object_2: count_of_matches,}
	THIS DOES NOT ITERATE OR ANYTHING
	
	-- Source file is /Users/ps22344/Downloads/chapter2/current/punctuationcounter_0927.py ---
	"""
	punctuationdict={
	re.compile(r"(?:\s|\w)(!\?|\?!)(?:\s|\w)"):0
	}

	for stringi in punctuation:
		print stringi, "-->", re.escape(stringi)
		punctuationdict[re.compile(re.escape(stringi)+"{2,}")]=0	

	for i in punctuationdict:
		result=i.findall(testi)
		if result:
			print i.pattern
			print result
		punctuationdict[i]=len(result)
	print punctuationdict


def leetcounter(dir):
	"""
	The leetcounter identifies any words that exhibit leet features, e.g. name --> nam3 
	The list this is based on was made in /Users/ps22344/Downloads/chapter2/current/identifying_leetspeak_1008.py
	Iterates over files contained in dir.
	Returns two lists; first is absolute counts, the second relative counts	 
	Inspired by  http://www.gamehouse.com/blog/leet-speak-cheat-sheet/
	"""
	starttime=time.time()
	
	featuredict={}
	search_terms=[]
	results=[]
	resultdict=defaultdict(float)
	
	with codecs.open('/home/ps22344/Downloads/chapter2/textfiles/leetwords_1216.txt', "r", "utf-8") as inputtext:
		for line in inputtext.readlines():
			print line.rstrip("\n")
			search_terms.append(re.compile(" ("+line.rstrip("\n")+") "))
	
	for pati in [i for i in os.listdir(dir) if not i.startswith(".")]:
		print pati
		for fili in [i for i in os.listdir(os.path.join(dir, pati)) if not i.startswith(".")]:
			with codecs.open(os.path.join(dir, pati, fili), "r", "utf-8") as inputfili:
				inputad=ct.adtextextractor(inputfili.read(), fili)
			wordcount=float(len(ct.tokenizer(inputad)))
			result=[k.findall(inputad) for k in search_terms]
			for no, item in enumerate(result):
				resultdict[no]=resultdict[no]+len(item)
			results.append([(len(i), len(i)/wordcount) for i in result])
			#print results
			if sum([len(i) for i in result]) > 2:
				for n, i in enumerate(result):
					 if len(i) > 0:
						 print search_terms[n].pattern, n,i, "len", len(i)
				print os.path.join(dir, pati, fili), "\n"
				os.system("cygstart "+os.path.join(dir, pati, fili))
	endtime=time.time()
	print "This took us {} minutes".format((endtime-starttime)/60)
	#print results
	print len(results), "files processed"
	print "\n\n"
	resultdict={search_terms[k].pattern:v for k,v in resultdict.items() if v > 0}
	for k in sorted(resultdict, key=resultdict.get, reverse=True):
		print k, resultdict[k]
	print "shape of results, number of lists:", len(results),  "-- length of lists", set([len(i) for i in results])
	#1st list is absolute counts, 2nd div by word count
	return [[x[0] for x in i] for i in results], [[x[1] for x in i] for i in results]


#the rebusfinder needs to be here; it finds instance of "4" for "for. 
#/Users/ps22344/Downloads/chapter2/current/identifying_rebus_1009.py

# the rebusfinder 2 needs to be here; it finds instances of "2" for "to".
# /Users/ps22344/Downloads/chapter2/current/identifying_rebus_2_1012.py

# the rebusfinder too needs to be here; it finds instances of "2" for "too". 
# /Users/ps22344/Downloads/chapter2/current/rebusfinder_too_1108.py
# done

# the capsfinder needs to be here. it does not yet exist but measures non-standard capitalization
# the capsfinder is here E:\cygwin\home\ps22344\Downloads\chapter2\current\capsfinder_1203.py

# the singleletterfinder needs to be here. it does not yet exist but finds things like "c u"
# here it is E:\cygwin\home\ps22344\Downloads\chapter2\current\charactercounter_1129.py


###SECTION 2
###ORTHOGRAPHY




#clippings
#/Users/ps22344/Downloads/chapter2/current/clippingcounter_1120.py

#abbreviations
##Abbreviations. Do we want to split that up into clippings etc?
#the acronymcounter counts alphabetisms and acronyms
#it does not distinguish between them as of now
#/Users/ps22344/Downloads/chapter2/current/acronymcounter_1115.py

#phonetically motivated letter substitution


#eye dialect


#spellings representing prosody or non-linguistic sounds such as laughter 




###SECTION 3
###WORD LEVEL




###SECTION 4
###UTTERANCE LEVEL
