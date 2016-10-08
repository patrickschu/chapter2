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
"i":1,
"r":2,
"e":3,
"a":4,
"t":7,
"b":8,
"g":9,
"o":0
}


#dirs
dir='/Users/ps22344/Downloads/craig_0208/'
dir='/Users/ps22344/Downloads/craigbalanced_0601'

def dictbuilder(input_path):
	"""
	reads files in input_path	
	input_path needs to have subfolders. 
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
			for token in [i for i in tokenized if i]:
				worddict[token]=worddict[token]+1
	print ("\n".join([":".join((k, unicode(worddict[k]))) for k in sorted(worddict, key=worddict.get, reverse=True) if worddict[k] > 50]))
			
			
			
dictbuilder(dir)
			
			
			
	
endtime=time.time()
print "This took us {} minutes".format((endtime-starttime)/60)	