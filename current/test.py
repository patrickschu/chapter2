import numpy as np
import codecs
import time
import os
import clustertools as ct
import re
from collections import defaultdict
from string import punctuation
import json

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

writtennumbers=["zero", "one","two","three","four","five","six","seven","eight","nine","ten","eleven","twelve","thirteen","fourteen", "twenty", "thirty", "fourty", "fifty", "sixty"]	

for writtennumber in writtennumbers:
	writtennumberdict[writtennumber]=0

print writtennumberdict
#dirs
dir='/home/ps22344/Downloads/craig_0208/'
#dir='/Users/ps22344/Downloads/craigbalanced_0601'

exclude_post_context=["fingers","nights", "weeling","wheel",  "s", "am", "a.m.", "figures", "pm", "p.m.","dogs","tattoos", "emails", "foot", "feet", "ft", "children", "guy", "just", "of", "to", "i", "year", "years", "yr", "yrs", "days", "wheeler", "wheelers", "wheeling", "times", "or", "and", "months", "in", "kids", "weeks", "day", "days"]
exclude_pre_context= ["battlefield", "minimum", "but", "from", "got", "be", "this", "n", "first","only", "these", "has", "all", "are", "and", "feb", "april", "july", "number", "about", "playstation", "our", "on", "sleep","thanks","bedroom", "fine","before","had","except", "acres", "no", "in", "b", "with", "size", "a", "to","have", "of", "or", "the", "for", "feet", "foot", "ft", "my", "your"]+["young","incredable","friendly","very","eiight","every","servicing","like","quick","sev","our","giving","stage","last","son","speak","use","top","least","until","survived","than","those","is","buffy","im","at","after","know"]+[u'holding', u'ad', u'oh', u'gta', u'dogs', u'her', u'look', u'eyes', u'mind', u'make', u'figured', u'nearly', u'lodging', u'marred', u'start', u'taken', u'plus', u'truck', u'own', u'prefers', u'favorite', u'doorsopened', u'weather', u'other', u'gym', u'tandem', u'tongue', u'past', u'who', u'female', u'round', u'as', u'put', u'decent', u'raised', u'fairs', u'driving', u'that', u'beach', u'beach', u'just', u'country', u'carry', u'she', u'shine', u'seen', u'sober', u'dogs', u'same', u'friend', u'hmu', u'time', u'nice', u'guy', u'guy', u's', u'almost', u'o', u'unforgettable', u'zro', u'zro', u'hace', u'hoping', u'other', u'horny', u'regularly', u'nice', u'harts', u'now', u'beg', u'same', u'offing', u'answer', u'host', u'married', u'head', u'befor', u'thick', u'gym', u'f', u'drive', u'hair', u'owned', u're', u'park', u'smash', u'into', u'phase', u'havin', u'wednesday', u'large', u'finding', u'over', u'within', u'run', u'owned', u'answer', u'she', u'sitter', u'apr', u'apr', u'random', u'us', u'taking', u'hotel', u'fishing', u'were', u'interested', u'evil', u'events', u'supported', u'lvl', u'literally', u'may', u's', u'extinct', u'sending', u'hp', u'hp', u'suffered', u'waiting', u'pay', u'extinct', u'til', u'done', u'play', u'beautiful', u'then', u'plus', u'approx', u'lives', u'literally', u'get', u'found', u'someone', u'insert']

include_pre_context=["pay", "m", "w", "up", "swf","love", "here", "not", "there", "ready","lkng","me", "ask", "live", "cheer", "grateful", "thanks", "partner", "men", "man", "male", "woman", "women","looking", "lookin", "pic", "pix", "lookn", "pics", "picture", "photo"]
include_post_context=["swf","yu","who", "dead", "reading", "over", "help", "life", "your", "the", "a", "my", "our", "an", "real", "you", "u", "me", "ltr", "play", "same", "whatever", "sex", "someone", "fun"]

def rebusfinder(input_path):
	"""
 	This finds words that are represented as numbers. 
 	All combinations \W([a-z]+)\s+("+unicode(number)+")\s+([a-z]+)\W for the number put in are identified.
 	The lists exclude_pre and exclude_post word for negative contexts in 4.
 	It print the results and give type and token counts. 
	
	"""
	results=[]
	for number in [4]:
		numberregex=re.compile("\W([a-z]+)\s+("+unicode(number)+")\s+([a-z]+)\W")
		#just for now
		h0dict=defaultdict(int)
		h2dict=defaultdict(int)
		print numberregex.pattern
		for pati in [i for i in os.listdir(input_path) if not i.startswith(".")]:
			for fil in [i for i in os.listdir(os.path.join(input_path, pati)) if not i.startswith(".")]:
				result=[]
				fili=codecs.open(os.path.join(input_path, pati, fil), "r", "utf-8")
				inputad=ct.adtextextractor(fili.read(), fil)
				inputad=inputad.lower()
				wordcount=float(len(inputad))
				hits=numberregex.findall(inputad)
				#this weeds out all the phonenumbers. 
				hits=[h for h in hits if h[0] not in writtennumberdict and h[2] not in writtennumberdict]
				for h in hits:
					if h[0] in include_pre_context or h[2] in include_post_context:
						#print h
						h0dict[h[0]]=h0dict[h[0]]+1
						h2dict[h[2]]=h2dict[h[2]]+1
						result.append(h)
					elif h[0] not in exclude_pre_context and h[2] not in exclude_post_context:
						if h[2]:#:=="days":
							#print h
							h0dict[h[0]]=h0dict[h[0]]+1
							h2dict[h[2]]=h2dict[h[2]]+1
							result.append(h)
				#if len(result) > 0:
				#	print "len", len(result)
				results.append([(len(result), len(result)/wordcount)])
			print "total len", len(results)
		print "We have {} items with a token count of {}".format(len(h0dict.keys()), sum(h0dict.values()))
		h0dict={k:v for k,v in h0dict.items() if v > 0}
		print "\n\n", number, "\n\posttext here be the results\n\n"
		#print "\n".join([": ".join([k, unicode(h0dict[k])]) for k in sorted(h0dict, key=h0dict.get, reverse=True)])
		#print "\n".join([": ".join([k, unicode(h2dict[k])]) for k in sorted(h2dict, key=h2dict.get, reverse=True)])

		#print "We have {} post items with a token count of {}".format(len(h2dict.keys()), sum(h2dict.values()))
		#print "We have {} pre items with a token count of {}".format(len(h0dict.keys()), sum(h0dict.values()))
		# for t in [[x[1] for x in i] for i in results]:
			# if sum (t) > 0:
				# print t
		return [[x[0] for x in i] for i in results], [[x[1] for x in i] for i in results]
			
rebusfinder(dir)


def leetcounter(dir):
	"""
	The leetcounter identifies any words that exhibit leet features, e.g. name --> nam3 
	The list this is based on was made in /Users/ps22344/Downloads/chapter2/current/identifying_leetspeak_1008.py
	Iterates over files contained in dir.
	Returns two lists; first is absolute counts, the second relative counts	 
	Inspired by  http://www.gamehouse.com/blog/leet-speak-cheat-sheet/
	"""
	starttime=time.time()
	
	featuredict={}
	search_terms=[]
	results=[]
	resultdict=defaultdict(float)
	
	with codecs.open('/home/ps22344/Downloads/chapter2/textfiles/leetwords_1216.txt', "r", "utf-8") as inputtext:
		for line in inputtext.readlines():
			print line.rstrip("\n")
			search_terms.append(re.compile(" ("+line.rstrip("\n")+") "))
	
	for pati in [i for i in os.listdir(dir) if not i.startswith(".")]:
		print pati
		for fili in [i for i in os.listdir(os.path.join(dir, pati)) if not i.startswith(".")]:
			with codecs.open(os.path.join(dir, pati, fili), "r", "utf-8") as inputfili:
				inputad=ct.adtextextractor(inputfili.read(), fili)
			wordcount=float(len(ct.tokenizer(inputad)))
			result=[k.findall(inputad) for k in search_terms]
			for no, item in enumerate(result):
				resultdict[no]=resultdict[no]+len(item)
			results.append([(len(i), len(i)/wordcount) for i in result])
			#print results
			if sum([len(i) for i in result]) > 2:
				for n, i in enumerate(result):
					 if len(i) > 0:
						 print search_terms[n].pattern, n,i, "len", len(i)
				print os.path.join(dir, pati, fili), "\n"
				os.system("cygstart "+os.path.join(dir, pati, fili))
	endtime=time.time()
	print "This took us {} minutes".format((endtime-starttime)/60)
	#print results
	print len(results), "files processed"
	print "\n\n"
	resultdict={search_terms[k].pattern:v for k,v in resultdict.items() if v > 0}
	for k in sorted(resultdict, key=resultdict.get, reverse=True):
		print k, resultdict[k]
	print "shape of results, number of lists:", len(results),  "-- length of lists", set([len(i) for i in results])
	#1st list is absolute counts, 2nd div by word count
	return [[x[0] for x in i] for i in results], [[x[1] for x in i] for i in results]

	
def repeatedpunctuationfinder(dir):
	"""
	The repeatedpunctuationfinder uses string.punctuation to create a dictionary of regexes.
	These are used to identify non-Standard usage of punctuation. 
	Note how we hardcoded the ?!? variants into the punctuationdict from the start. 
	Iterates over files contained in dir.
	Returns two lists; first is absolute counts, the second relative counts	
	-- Source file is /Users/ps22344/Downloads/chapter2/current/punctuationcounter_0927.py ---
	"""
	starttime=time.time()
	#creating a featuredict from file
	results=[]
	resultdict=defaultdict(float)
	punctuationdict={
	re.compile(r"(?:\s|\w)(!\?|\?!)(?:\s|\w)"):0
	}

	for stringi in punctuation:
		print stringi, "-->", re.escape(stringi)
		punctuationdict[re.compile("((?:"+re.escape(stringi)+" ?){2,})")]=0	
	search_terms=punctuationdict.keys()
	for pati in [i for i in os.listdir(dir) if not i.startswith(".")]:
		print pati
		for fili in [i for i in os.listdir(os.path.join(dir, pati)) if not i.startswith(".")]:
			with codecs.open(os.path.join(dir, pati, fili), "r", "utf-8") as inputfili:
				inputad=ct.adtextextractor(inputfili.read(), fili)
			wordcount=float(len(ct.tokenizer(inputad)))
			result=[k.findall(inputad) for k in search_terms]
			for no, item in enumerate(result):
				resultdict[no]=resultdict[no]+len(item)
			results.append([(len(i), len(i)/wordcount) for i in result])
			print results
			if sum([len(i) for i in result]) > 80:
				for n, i in enumerate(result):
					 if len(i) > 0:
						 print search_terms[n].pattern, n,i, "len", len(i)
				print os.path.join(dir, pati, fili), "\n"
				os.system("cygstart "+os.path.join(dir, pati, fili))
			
	endtime=time.time()
	print "This took us {} minutes".format((endtime-starttime)/60)
	#print results
	print len(results), "files processed"
	print "\n\n"
	resultdict={search_terms[k].pattern:v for k,v in resultdict.items() if v > 0}
	for k in sorted(resultdict, key=resultdict.get, reverse=True):
		print k, resultdict[k]
	print "shape of results, number of lists:", len(results),  "-- length of lists", set([len(i) for i in results])
	#1st list is absolute counts, 2nd div by word count
	return [[x[0] for x in i] for i in results], [[x[1] for x in i] for i in results]


	"""
	The emoticonfinder takes a directory with corpus files as input. 
	It returns a list of lists with counts of each emoticon in each file in dir.
	Emoticons are read from file.
	list=[[x1feature1, x1feature2, ...], [x2feature1, x2feature2, ...]]
	We might consider making the file with emoticons an argument as well. 
	--- Original Source file is /Users/ps22344/Downloads/chapter2/current/emoticoncounter.py ---
	"""
	starttime=time.time()
	#creating a featuredict from file
	featuredict={}
	search_terms=[]
	results=[]
	resultdict=defaultdict(float)
	
	with codecs.open('/home/ps22344/Downloads/chapter2/textfiles/emolist_final_2.txt', "r", "utf-8") as inputtext:
		for line in inputtext.readlines():
			print line.rstrip("\n")
			search_terms.append(re.compile("\W("+re.escape(line.rstrip("\n"))+")(?: |<)"))
		
	for pati in [i for i in os.listdir(dir) if not i.startswith(".")]:
		print pati
		for fili in [i for i in os.listdir(os.path.join(dir, pati)) if not i.startswith(".")][:2]:
			with codecs.open(os.path.join(dir, pati, fili), "r", "utf-8") as inputfili:
				inputad=ct.adtextextractor(inputfili.read(), fili)
			result=[k.findall(inputad) for k in search_terms]
			for no, item in enumerate(result):
				resultdict[no]=resultdict[no]+len(item)
			results.append([len(i) for i in result])
			# if 11 > sum([len(i) for i in result]) > 6:
				# for n, i in enumerate(result):
					# if len(i) > 0:
						# print search_terms[n].pattern, n,i
				# print os.path.join(dir, pati, fili), "\n"
				# os.system("cygstart "+os.path.join(dir, pati, fili))
			
	endtime=time.time()
	print "This took us {} minutes".format((endtime-starttime)/60)
	#print results
	print len(results), "files processed"
	print "\n\n"
	resultdict={search_terms[k].pattern:v for k,v in resultdict.items() if v > 0}
	for k in sorted(resultdict, key=resultdict.get, reverse=True):
		print k, resultdict[k]
	print "shape of results, number of lists:", len(results),  "-- length of lists", set([len(i) for i in results])
	return results
	

