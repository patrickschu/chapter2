import numpy as np
from string import punctuation
import re
import clustertools as ct
import time
import os
import codecs
from collections import defaultdict
import json 



#typography={
#emoticons={':)':0, ':(':0 ,...},
#counstruct out of string.puncutation

#punctuation={re.compile("\.\.+":0, ",,+":0


#these are the features we are investigating	
numbersdict={
re.compile(r"4$"):0
}
for f in numbersdict:
	print f.pattern

print numbersdict.keys()

#search term - the collocation we're looking for
search_term="i"

#dataset
dir='/Users/ps22344/Downloads/craig_0208/'#adfiles_output_0116'
tagregex=re.compile(r"<.*?>")


#check if we find items
starttime=time.time()

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
		hits=[w for w in words if any(k.match(w) for k in numbersdict.keys())]
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
		



print "our numbersdict", numbersdict

endtime=time.time()

print "This took us {} minutes".format((endtime-starttime)/60)
