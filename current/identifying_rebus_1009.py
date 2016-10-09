import time
import codecs
import json
import re
import os
import clustertools as ct

starttime=time.time()

#number dictionary
numberdict={}

numbers=range(0,10)
for number in numbers:
	numberdict[number]=0


#written numbers for quality control
writtennumberdict={}

writtennumbers=["one","two","three","four","five","six","seven","eight","nine","ten","eleven","twelve","thirteen","fourteen"]	

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
		numberregex=re.compile("\W(\w+) ("+unicode(number)+") (\w+)\W")
		
		print numberregex.pattern
		print numberregex.findall("i see 4 you str8 i hate that")
		for pati in [i for i in os.listdir(input_path) if not i.startswith(".")]:
			for fil in [i for i in os.listdir(os.path.join(input_path, pati)) if not i.startswith(".")]:
				fili=codecs.open(os.path.join(input_path, pati, fil), "r", "utf-8")
				inputad=ct.adtextextractor(fili.read(), fil)
				inputad=inputad.lower()
				if numberregex.findall(inputad):
					print "\n\nbefore"
					print numberregex.findall(inputad)
					hits=numberregex.findall(inputad)
					print "after"
					print [h for h in hits if h[0] not in writtennumberdict and h[2] not in writtennumberdict]
# 					for g in hits:
# 						if g[0] in writtennumberdict:
# 							print "\n",g[0], "\n"
						


			
rebusfinder(dir, "worddict_full.json", numberdict, "b")



			

			
			
			
	
endtime=time.time()
print "This took us {} minutes".format((endtime-starttime)/60)	