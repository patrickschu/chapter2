import numpy as np
import codecs
import time
import os
import clustertools as ct
import re
from collections import defaultdict
from string import punctuation


t=np.array([[1,1], [2,2]])


print t, "\n---"

print np.column_stack((t, [[1000,1000,0], [2000,2000,0]]))

def repeatedpunctuationfinder(dir):
	"""
	The repeatedpunctuationfinder uses string.punctuation to create a dictionary of regexes.
	These are used to identify non-Standard usage of punctuation. 
	Note how we hardcoded the ?!? variants into the punctuationdict from the start. 
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
			wordcount=len(ct.tokenize(inputad))
			result=[k.findall(inputad) for k in search_terms]
			for no, item in enumerate(result):
				resultdict[no]=resultdict[no]+len(item)
			results.append([(len(i), len(i)/wordcount) for i in result])
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
	return [i[0] for i in results], [i[1] for i in results]

repeatedpunctuationfinder("/home/ps22344/Downloads/craig_0208")
	

def emoticonfinder(dir):
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
	

