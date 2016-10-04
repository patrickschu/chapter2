import numpy as np
from string import punctuation
import re
import clustertools as ct
import time
import os
import codecs
from collections import defaultdict
import json 


"""
Other than "finding_numbers.py", this regexes thru full strings rather than tokenized text.
It does not help anything in establishing frequent context but rather to discover features. 
Tokenization after all does destroy some constructions. 
It does not save anything to file. 
"""


#FINISHED PRODUCT
numbersdict={
re.compile(r"\d+"):0
}
for f in numbersdict:
	print f.pattern


#these are the features we are investigating	

numbersdict={}

for numba in [0,1,2,3,5,6,7,8,9]:
	numbersdict[re.compile(".{,20}\W+"+unicode(numba)+"\W+.{,20}")]=0
	
#numbersdict={re.compile(".*5sunshyne.*"):0}


for f in numbersdict:
	print f.pattern

#dataset
dir='/Users/ps22344/Downloads/craig_0208/'#adfiles_output_0116'




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
		inputad=inputad.lower()
		matches=[k.findall(inputad) for k in numbersdict.keys()]
		if sum([len(i) for i in matches]) > 0:
			print "hits", sum([len(i) for i in matches]), fil
			print matches
		



print "our numbersdict", numbersdict



endtime=time.time()

print "This took us {} minutes".format((endtime-starttime)/60)
