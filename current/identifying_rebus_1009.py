import time
import codecs
import json
import re
import os
import clustertools as ct
from collections import defauldict

starttime=time.time()

#number dictionary
numberdict={}

numbers=range(0,10)
for number in numbers:
	numberdict[number]=0


#written numbers for quality control
writtennumberdict={}

writtennumbers=["one","two","three","four","five","six","seven","eight","nine","ten","eleven","twelve","thirteen","fourteen", "twenty", "thirty", "fourty", "fifty", "sixty"]	

for writtennumber in writtennumbers:
	writtennumberdict[writtennumber]=0


#dirs
#dir='/Users/ps22344/Downloads/craig_0208/'
dir='/Users/ps22344/Downloads/craigbalanced_0601'


def rebusfinder(input_path, word_dictionary, number_dictionary, excluded_words):
	"""
 	This finds words that are represented as numbers. 
 	How is this going to happen?
 	IdK
	
	"""
	with codecs.open(word_dictionary, "r", "utf-8") as worddictionary:
		worddictionary=json.load(worddictionary)
	worddictionary={k:v for k,v in worddictionary.items() if not k in excluded_words and worddictionary[k] > 1}
	for number in number_dictionary.keys():
		numberregex=re.compile("\W([a-z]+) ("+unicode(number)+") ([a-z]+)\W")
		#just for now
		h0dict=defaultdict(int)
		h1dict=defaultdict(int)
		print numberregex.pattern
		print numberregex.findall("i see 4 you str8 i hate that")
		for pati in [i for i in os.listdir(input_path) if not i.startswith(".")]:
			for fil in [i for i in os.listdir(os.path.join(input_path, pati)) if not i.startswith(".")]:
				fili=codecs.open(os.path.join(input_path, pati, fil), "r", "utf-8")
				inputad=ct.adtextextractor(fili.read(), fil)
				inputad=inputad.lower()
				hits=numberregex.findall(inputad)
				if [h for h in hits if h[0] not in writtennumberdict and h[2] not in writtennumberdict]:
					print hits
				for h in hits:
					h0dict[h]=h0dict[h]+1
					h1dict[h]=h1dict[h]+1
		h0dict={k:v for k,v in h0dict.items() if v > 50}
		print "\n".join([": ".join([k, unicode(h0dict[k])]) for k in sorted(h0dict, key=h0dict.get, reverse=True)])

pre_context=[]
post_context=["kids", "emails"]
			
rebusfinder(dir, "worddict_full.json", numberdict, "b")



			

			
			
			
	
endtime=time.time()
print "This took us {} minutes".format((endtime-starttime)/60)	