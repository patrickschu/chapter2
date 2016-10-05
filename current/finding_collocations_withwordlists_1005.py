import numpy as np
from string import punctuation
import re
import clustertools as ct
import time
import os
import codecs
from collections import defaultdict
import json 




with codecs.open("/Users/ps22344/Downloads/chapter2/current/2words_topwords.txt", "r", "utf-8") as inputfile:
	inputlist=inputfile.read().split("\n")

print inputlist
#these are the features we are investigating	
numbersdict={}

for item in inputlist:
	try:
		numbersdict[re.compile(r".*"+item+".*")]=0
	except:
		print 'ITEM', item, "DID NOT MAKE IT"

for f in numbersdict:
	print f.pattern


#search term - the collocation we're looking for
#okay this is mis-named -- this is the main word, number we're investigating
search_term="2"

#dataset
dir='/Users/ps22344/Downloads/craig_0208/'#adfiles_output_0116'
#this is just to remove html
tagregex=re.compile(r"<.*?>")


#check if we find items
starttime=time.time()


def collofinder(main_term,regex):
	for pati in [i for i in os.listdir(dir) if not i.startswith(".")]:
		"""
		this looks over the keys of a dictionary that are regex patterns. 
		it outputs findings in the corpus given in "dir" with context.
		dir needs to have subfolders. 
		the twodict counts words with a distance of 2, the onedict counts words with a distance of 1.
		"""
		print pati
		for fil in [i for i in os.listdir(os.path.join(dir, pati)) if not i.startswith(".")]:
			fili=codecs.open(os.path.join(dir, pati, fil), "r", "utf-8")
			inputad=ct.adtextextractor(fili.read(), fili)
			inputad=tagregex.sub(" ", inputad)
			words=ct.tokenizer(inputad)
			words=[w.lower() for w in words]
			#specific words processing for numbers: introduce space between number immediately followed by word-character
			hits=[w for w in words if regex.match(w) ]
			#determines length of context extracted
			context=[-3,-2,-1,0, 1,2, 3]
			for matched in hits:
				if [i for i in context if words.index(matched) + i > len(words) -1 ] and search_term in words:
					print "too long"
					print [words[words.index(matched)+t] for t in [c for c in context if c <1 ]]
				elif hits and not [i for i in context if words.index(matched) + i > len(words) -1 ] and search_term in [words[words.index(matched)+t] for t in [-1,1]] :
					print fil
					print [words[words.index(matched)+t] for t in context]
				#print words
				
		
# 			print [words[words.index(w)+i] for i in [-2,-1,0,+1,+2]]
#  			if words.index(w) not in [0, 1, len(words) -1, len(words)-2] and search_term in [words[words.index(w)+i] for i in [-2,-1,0,+1,+2]]:
#  				print [words[words.index(w)+i] for i in [-2,-1,0,+1,+2]]
		

for key in numbersdict.keys():
	print key.pattern
	collofinder(search_term, key)

print "our numbersdict", numbersdict

endtime=time.time()

print "This took us {} minutes".format((endtime-starttime)/60)
