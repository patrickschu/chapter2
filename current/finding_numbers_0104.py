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

#FINISHED PRODUCT
numbersdict={
re.compile(r"\d+"):0
}
for f in numbersdict:
	print f.pattern


#these are the features we are investigating	
numbersdict={
re.compile(r"4+$"):0
}
for f in numbersdict:
	print f.pattern



topic="4"
#dataset
dir='/Users/ps22344/Downloads/craig_0208/'#adfiles_output_0116'

outifile=codecs.open(topic+"words.txt", "a", "utf-8")
onedict=defaultdict(int)
twodict=defaultdict(int)


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
	for fili in [i for i in os.listdir(os.path.join(dir, pati)) if not i.startswith(".")]:
		fili=codecs.open(os.path.join(dir, pati, fili), "r", "utf-8")
		inputad=ct.adtextextractor(fili.read(), fili)
		words=ct.tokenizer(inputad)
		words=[w.lower() for w in words]
		#specific words processing for numbers: introduce space between number immediately followed by word-character
		if [w for w in words if any(k.match(w) for k in numbersdict.keys())]:
			if words.index(w) not in [0, 1, len(words) -1, len(words)-2]:
				twodict[words[words.index(w)-2]]=twodict[words[words.index(w)-2]]+1
				twodict[words[words.index(w)+2]]=twodict[words[words.index(w)+2]]+1
			if words.index(w) not in [0, len(words)-1]:
				onedict[words[words.index(w)-1]]=onedict[words[words.index(w)-1]]+1
				onedict[words[words.index(w)+1]]=onedict[words[words.index(w)+1]]+1
				outifile.write("\n".join([" ".join([words[words.index(w)-2], words[words.index(w)-1],w, words[words.index(w)+1], words[words.index(w)+2]]) for w in words if any(k.match(w) for k in numbersdict.keys()) and words.index(w) not in [0, 1, len(words)-1, len(words)-2]]))
			else:
				pass



print "our numbersdict", numbersdict


print "\n\ndistance of 2"
print "\n".join([": ".join([k, unicode(twodict[k])]) for k in sorted(twodict, key=twodict.get, reverse=True)])

print "\n\ndistance of 1"
print "\n\ndistance of 1"
print "\n".join([": ".join([k, unicode(onedict[k])]) for k in sorted(onedict, key=onedict.get, reverse=True)])

outifile.close()
with codecs.open(topic+"_onedict.json", "w", "utf-8") as oneout:
	json.dump(onedict, oneout)

with codecs.open(topic+"_twodict.json", "w", "utf-8") as twoout:
	json.dump(twodict, twoout)

endtime=time.time()

print "This took us {} minutes".format((endtime-starttime)/60)
