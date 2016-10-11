import time
import codecs
import json
import re
import os
import clustertools as ct
from collections import defaultdict

starttime=time.time()

#number dictionary
numberdict={}

numbers=[4]#range(11,20)
for number in numbers:
	numberdict[number]=0


#written numbers for quality control
writtennumberdict={}

writtennumbers=["one","two","three","four","five","six","seven","eight","nine","ten","eleven","twelve","thirteen","fourteen", "twenty", "thirty", "fourty", "fifty", "sixty"]	

for writtennumber in writtennumbers:
	writtennumberdict[writtennumber]=0

print writtennumberdict
#dirs
dir='/Users/ps22344/Downloads/craig_0208/'
#dir='/Users/ps22344/Downloads/craigbalanced_0601'

exclude_post_context=["s", "am", "a.m.", "figures", "pm", "p.m.","dogs","tattoos", "emails", "foot", "feet", "ft", "children", "guy", "just", "of", "to", "i", "year", "years", "yr", "yrs", "days", "wheeler", "wheelers", "wheeling", "times", "or", "and", "months", "in", "kids", "weeks", "day", "days"]
exclude_pre_context= ["our", "on", "sleep","thanks","bedroom", "fine","before","had","except", "acres", "no", "in", "b", "with", "size", "a", "to","have", "of", "or", "the", "for", "feet", "foot", "ft", "my", "your"]+["young","incredable","friendly","very","eiight","every","servicing","like","quick","sev","our","giving","stage","last","son","speak","use","top","least","until","survived","than","those","is","buffy","im","at","after","know"]

include_pre_context=["looking", "lookin", "pic"]
include_post_context=["the", "a"]

def rebusfinder(input_path, word_dictionary, number_dictionary, excluded_words):
	"""
 	This finds words that are represented as numbers. 
 	All combinations \W([a-z]+)\s+("+unicode(number)+")\s+([a-z]+)\W for the number put in are identified.
 	The lists exclude_pre and exclude_post word for negative contexts in 4.
 	It print the results and give type and token counts. 
	
	"""
	#with codecs.open(word_dictionary, "r", "utf-8") as worddictionary:
	#	worddictionary=json.load(worddictionary)
	#worddictionary={k:v for k,v in worddictionary.items() if not k in excluded_words and worddictionary[k] > 1}
	for number in number_dictionary.keys():
		numberregex=re.compile("\W([a-z]+)\s+("+unicode(number)+")\s+([a-z]+)\W")
		#just for now
		h0dict=defaultdict(int)
		h2dict=defaultdict(int)
		print numberregex.pattern
		for pati in [i for i in os.listdir(input_path) if not i.startswith(".")]:
			for fil in [i for i in os.listdir(os.path.join(input_path, pati)) if not i.startswith(".")]:
				fili=codecs.open(os.path.join(input_path, pati, fil), "r", "utf-8")
				inputad=ct.adtextextractor(fili.read(), fil)
				inputad=inputad.lower()
				hits=numberregex.findall(inputad)
				#this weeds out all the phonenumbers. 
				hits=[h for h in hits if h[0] not in writtennumberdict and h[2] not in writtennumberdict]
				for h in hits:
					if h[0] in include_pre_context or h[2] in include_post_context:
						print h
					elif h[0] not in exclude_pre_context and h[2] not in exclude_post_context:
						if h[2]:#:=="days":
							#print h
							h0dict[h[0]]=h0dict[h[0]]+1
							h2dict[h[2]]=h2dict[h[2]]+1
		print "We have {} items with a token count of {}".format(len(h0dict.keys()), sum(h0dict.values()))
		h0dict={k:v for k,v in h0dict.items() if v > 0}
		print "\n\n", number, "\n\npretext here be the results\n\n"
		print "\n".join([": ".join([k, unicode(h0dict[k])]) for k in sorted(h0dict, key=h0dict.get, reverse=True)])
		#print "\n".join([": ".join([k, unicode(h2dict[k])]) for k in sorted(h2dict, key=h2dict.get, reverse=True)])

		print "We have {} items with a token count of {}".format(len(h0dict.keys()), sum(h0dict.values()))



##4: 'a' is def bad pretext, 'the' also, and 'for'; "have" can be legit for 2
##2: 'to' is not cool as pretext


#think these thru for each number. not that we accidentally exclude good things
#
good_pre_context=[]#["friend", "looking","lookin", "pic", "picture", "pix", "pics"]
good_post_context=[]#["trade", "tonight"]

			
rebusfinder(dir, "worddict_full.json", numberdict, "b")



			

			
			
			
	
endtime=time.time()
print "This took us {} minutes".format((endtime-starttime)/60)	