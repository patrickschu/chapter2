import numpy as np
from string import punctuation
import re
import clustertools as ct
import time
import os
import codecs
from collections import defaultdict
import json 




#identify words that differ in a number vs letter only
#take text, tokenize
#check with dict

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

t=re.compile("ss")
#dirs
dir='/Users/ps22344/Downloads/craig_0208/'
#dir='/Users/ps22344/Downloads/craigbalanced_0601'

def dictbuilder(input_path, output_file):
	"""
	reads files in input_path	
	input_path needs to have subfolders. 
	removes numbers.
	"""
	worddict=defaultdict(int)
	for pati in [i for i in os.listdir(input_path) if not i.startswith(".")]:
		print pati
		for fil in [i for i in os.listdir(os.path.join(input_path, pati)) if not i.startswith(".")]:
			fili=codecs.open(os.path.join(input_path, pati, fil), "r", "utf-8")
			inputad=ct.adtextextractor(fili.read(), fil)
			inputad=inputad.lower()
			tokenized=ct.tokenizer(inputad)
			tokenized=[re.sub("\W","", i) for i in tokenized]
			tokenized=[i for i in tokenized if not re.match("\d+", i)]
			for token in [i for i in tokenized if i]:
				worddict[token]=worddict[token]+1
	print ("\n".join([":".join((k, unicode(worddict[k]))) for k in sorted(worddict, key=worddict.get, reverse=True) if worddict[k] > 50]))
	print "We created a dictionary of {} total words with {} types".format(sum(worddict.values()), len(worddict.keys()))		
	if output_file:
		with codecs.open(output_file, "w", "utf-8") as outputfile:
			json.dump(worddict, outputfile)	
			print "Dict written to ", outputfile

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
			


			
#dictbuilder(dir, "worddict_full.json")
leetfinder("worddict_full.json", leetdict, ['wl','ftl','tol','xl','jo','lo','thoe','yo','aso', 'zerofive', 'fond', 'ano', 'xo','astro','ando','do','poc','ao','ho','mo', 'so','mayo','amo','ol','el','bul','woudl','weho','ase','toe','fined','bfe','ve','te', 'talke','withe','reali', 'muchi', 'ani','outi','toi','tio','dip','jessi','ami', 'oi', 'wi','rl','psl', 'mel', 'al','dl','fl','xbl','ala','uop','rot','lotr','ko','qi','fi','mei','di','ki','ri','ai','a7', 'of', "a7x", 'wb', 'ob', 'tob', 'sixe', 'ine', 'donte', 'de', 'ore', 'me2', 'qe', 'fore', 'looke', 'ae', 'ice', 'wo'])



			

			
			
			
	
endtime=time.time()
print "This took us {} minutes".format((endtime-starttime)/60)	