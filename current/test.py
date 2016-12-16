import numpy as np
import codecs
import time
import os
import clustertools as ct
import re
from collections import defaultdict
from string import punctuation
import json

def leetfinder(word_dictionary, dir):
	"""
	NOTE THAT THIS IDENTIFIES RATHER THAN COUNTS FEATURES.
	The leetfinder takes a dictionary of words as a json.
	It identifies any words that vary only in the use of features in leet_dictionary, which is hardcoded above.
	List of excluded_words has all the items to be ignored in the word_dictionary. 
	Both of the above have been hardcoded. 
	The word_dictionary we have been using is "worddict_full.json".
	
	-- Source file is /Users/ps22344/Downloads/chapter2/current/identifying_leetspeak_1008.py --
	"""
	starttime=time.time()
	
	#conversions from http://www.gamehouse.com/blog/leet-speak-cheat-sheet/
	leet_dictionary={
	"i":[1],
	#"r":[2],
	"e":[3],
	#"a":["@"], #note that this is still a thing in m@l3s
	#"t":[7],
	#"b":[8],
	#"g":[9, 6],
	"o":[0,8],
	"l":[1],
	"s":["$"]#[5]
	}
	
	excluded_words=['wl','ftl','tol','xl','jo','lo','thoe','yo','aso', 'zerofive', 'fond', 'ano', 'xo','astro','ando','do','poc','ao','ho','mo', 'so','mayo','amo','ol','el','bul','woudl','weho','ase','toe','fined','bfe','ve','te', 'talke','withe','reali', 'muchi', 'ani','outi','toi','tio','dip','jessi','ami', 'oi', 'wi','rl','psl', 'mel', 'al','dl','fl','xbl','ala','uop','rot','lotr','ko','qi','fi','mei','di','ki','ri','ai','a7', 'of', "a7x", 'wb', 'ob', 'tob', 'sixe', 'ine', 'donte', 'de', 'ore', 'me2', 'qe', 'fore', 'looke', 'ae', 'ice', 'wo']
	
	with codecs.open(word_dictionary, "r", "utf-8") as worddictionary:
		worddictionary=json.load(worddictionary)
	originalworddictonary=worddictionary
	worddictionary={k:v for k,v in worddictionary.items() if not k in excluded_words and worddictionary[k] > 1}
	totalhits=[]
	for leetkey in leet_dictionary.keys():
		#leetkey is a letter: a,e,i
		characterregex=re.compile(leetkey)
		for number  in leet_dictionary[leetkey]:
			number=unicode(number)
			print "We're looking at {} being replaced with {}".format(characterregex.pattern, number)
			#replacement characters come first
			result=[(w, characterregex.sub(number, w), originalworddictonary[characterregex.sub(number, w)]) for w in worddictionary.keys() if originalworddictonary.get(characterregex.sub(number, w), None) and leetkey in w]
			print result
			print "Total results", sum([count for word,subword,count in result])
			totalhits.append(sum([count for word,subword,count in result]))
	print "All told, that makes {} hits in a {} word corpus".format(sum(totalhits), sum(originalworddictonary.values()))
	print totalhits
	#save to file what this outputs, then run over iterator

	
leetfinder('worddict_full.json', '/home/ps22344/Downloads/craig_0208')
	
	
	
	
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
		for fili in [i for i in os.listdir(os.path.join(dir, pati)) if not i.startswith(".")][:2]:
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
	

