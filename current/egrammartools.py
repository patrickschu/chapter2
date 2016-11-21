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
	leetdict={
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



#the rebusfinder needs to be here; it finds instance of "4" for "for. 
#/Users/ps22344/Downloads/chapter2/current/identifying_rebus_1009.py

# the rebusfinder 2 needs to be here; it finds instances of "2" for "to".
# /Users/ps22344/Downloads/chapter2/current/identifying_rebus_2_1012.py

# the rebusfinder too needs to be here; it finds instances of "2" for "too". 
# /Users/ps22344/Downloads/chapter2/current/rebusfinder_too_1108.py
# done

# the capsfinder needs to be here. it does not yet exist but measures non-standard capitalization

# the singleletterfinder needs to be here. it does not yet exist but finds things like "c u"

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
