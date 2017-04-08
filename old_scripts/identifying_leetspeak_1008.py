import numpy as np
from string import punctuation
import re
import clustertools as ct
import time
import os
import codecs
from collections import defaultdict
import json 

#final version to make text file

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
	originalworddictionary=worddictionary
	worddictionary={k:v for k,v in worddictionary.items() if not k in excluded_words and worddictionary[k] > 1}
	totalhits=[]
	outputfile=codecs.open("leetwords_1216.txt", "a", "utf-8")
	for leetkey in leet_dictionary.keys():
		#leetkey is a letter: a,e,i
		characterregex=re.compile(leetkey)
		for number  in leet_dictionary[leetkey]:
			number=unicode(number)
			print "We're looking at {} being replaced with {}".format(characterregex.pattern, number)
			#replacement characters come first
			result=[(w, characterregex.sub(number, w), originalworddictionary[characterregex.sub(number, w)]) for w in worddictionary.keys() if originalworddictionary.get(characterregex.sub(number, w), None) and leetkey in w]
			print "!!!!!", [i[1] for i in result]
			for word in [i[1] for i in result]:
				outputfile.write(word+"\n")
			print "Total results", sum([count for word,subword,count in result])
			totalhits.append(sum([count for word,subword,count in result]))
	print "All told, that makes {} hits in a {} word corpus".format(sum(totalhits), sum(originalworddictionary.values()))
	outputfile.close()
	print totalhits
	#save to file what this outputs, then run over iterator

	
leetfinder('worddict_full.json', '/home/ps22344/Downloads/craig_0208')
####OLD FILE

#conversions from http://www.gamehouse.com/blog/leet-speak-cheat-sheet/

starttime=time.time()

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


#dirs
dir='/Users/ps22344/Downloads/craig_0208/'
#dir='/Users/ps22344/Downloads/craigbalanced_0601'


def leetfinder(word_dictionary, leet_dictionary, excluded_words):
	"""
	The leetfinder takes a dictionary of words as a json.
	It identifies any words that vary only in the use of features in leet_dictionary, which is hardcoded above.
	List of excluded_words has all the items to be ignored in the word_dictionary. 
	
	"""
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
			


			
leetfinder("worddict_full.json", leetdict, ['wl','ftl','tol','xl','jo','lo','thoe','yo','aso', 'zerofive', 'fond', 'ano', 'xo','astro','ando','do','poc','ao','ho','mo', 'so','mayo','amo','ol','el','bul','woudl','weho','ase','toe','fined','bfe','ve','te', 'talke','withe','reali', 'muchi', 'ani','outi','toi','tio','dip','jessi','ami', 'oi', 'wi','rl','psl', 'mel', 'al','dl','fl','xbl','ala','uop','rot','lotr','ko','qi','fi','mei','di','ki','ri','ai','a7', 'of', "a7x", 'wb', 'ob', 'tob', 'sixe', 'ine', 'donte', 'de', 'ore', 'me2', 'qe', 'fore', 'looke', 'ae', 'ice', 'wo'])



			

			
			
			
	
endtime=time.time()
print "This took us {} minutes".format((endtime-starttime)/60)	