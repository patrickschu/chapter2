import numpy as np
import codecs
import time
import os
import clustertools as ct
import re
from collections import defaultdict
from string import punctuation
import json
from nltk import pos_tag

starttime=time.time()
#check if we have this thing somewhere else and then delete from here. oops, this is included in our results
def word2vecwordfinder(search_terms, input_file):
	"""
	wordfinder looks up individual words in the clusters from word2vec.
	search_terms is list of strings, input_file the path to a JSON file of clusters.
	"""
	with codecs.open(input_file, 'r', 'utf-8') as inputfile:
		clusters=json.load(inputfile)
	
	results=[k for term in search_terms for k in clusters.keys() if term in clusters[k]['words']]
	return results
	


#number dictionary
numberdict={}

numbers=[2]#range(11,20)
for number in numbers:
	numberdict[number]=0


#written numbers for quality control
writtennumberdict={}

writtennumbers=["zero", "one","two","three","four","five","six","seven","eight","nine","ten","eleven","twelve","thirteen","fourteen", "twenty", "thirty", "fourty", "fifty", "sixty", "fivefivefive"]	

for writtennumber in writtennumbers:
	writtennumberdict[writtennumber]=0

print writtennumberdict
#dirs
dir='/Users/ps22344/Downloads/craig_0208/'
#dir='/Users/ps22344/Downloads/craigbalanced_0601'

nounregex=re.compile("NN.?")
#do we need the to, do ect in post_context
#exclude_post_context=["years?", "months?", "weeks?", "days?", "hours?", "times?", "peoples?", "daughters?", "(boy|girl)?friends?", "girls?", "kids?", "boys?", "children", "dogs?", "jobs?", "things?", "(p|a)\.?m\.?", "to", "or" ]
exclude_post_context=["inche?s?", "wks?", "nd", "i", "sec", "stepping", "asap", "tattoos", "years?", "yrs", "months?", "weeks?", "days?", "hours?", "times?", "peoples?", "(boy|girl)?friends?", "(p|a)\.?m\.?", "to", "or", "full", "wana" ]

exclude_post_context=[re.compile(r"^"+i+"$") for i in exclude_post_context]

exclude_pre_context=["borderlands", "chicago", "c?ops?", "till?", "or", "and", "just", "f(oo|ee)?t", "last", "own", "hsv", "herpes"]
exclude_pre_context=[re.compile(r"^"+i+"$") for i in exclude_pre_context]

def rebusfinder_to(input_path, word_dictionary, number_dictionary, excluded_words):
	"""
 	This finds the word "to"  that represented as the number 2. 
 	All combinations \W([a-z]+)\s+("+unicode(number)+")\s+([a-z]+)\W for the number put in are identified.
 	The lists exclude_pre_context and exclude_post_context exclude instances where a word follows (post) or precedes (pre) the "2" per regex. 
 	Procedure: 
 	Eliminate all pre and post contexts;
 	POS tag the remaining ones and eliminate certain combinations;
 	Find positives by POS tag and a word list;
 	Dismiss the remaining ones. 
 	It returns a list of positives. 
 	It print the results and give type and token counts. 
	
	"""
	search_terms=[2]
	for number in search_terms:
		numberregex=re.compile("\W([a-z]+)\s+("+unicode(number)+")\s+([a-z]+)\W")
		#just for now
		h0dict=defaultdict(int)
		h2dict=defaultdict(int)
		print numberregex.pattern
		results=[]
		for pati in [i for i in os.listdir(input_path) if not i.startswith(".")]:
			for fil in [i for i in os.listdir(os.path.join(input_path, pati)) if not i.startswith(".")]:
				fili=codecs.open(os.path.join(input_path, pati, fil), "r", "utf-8")
				inputad=ct.adtextextractor(fili.read(), fil)
				inputad=inputad.lower()
				wordcount=float(len(ct.tokenizer(inputad)))
				hits=numberregex.findall(inputad)
				#this weeds out all the phonenumbers. 
				hits=[h for h in hits if h[0] not in writtennumberdict and h[2] not in writtennumberdict]
				for h in hits:
					#print  h
					if not any (regex.match(h[2]) for regex in exclude_post_context) and not any (regex.match(h[0]) for regex in exclude_pre_context):
						tagged=pos_tag(h)
						#taking out trash
						if (
							(tagged[0][1] in ["DT", "JJS", "TO", "PRP$"]) 
							or
							(tagged[0][1]=="IN" and h[0] not in ["out", "like"])
							or
							(tagged[0][1] in ["VBG"] and h[0] not in ["talking", "responding", "waiting", "getting","looking", "going", "trying"])
							or
							(tagged[0][1] in ["VB", "VBD", "VBP", "VBZ"] and tagged[2][1] in ["JJ"])
							or
							#this is where we screw up
							(tagged[2][1] in ["NNS"] and h[2] not in ["chat", "kiss", "go", "know", "find", "do", "c", "knees"])
							or
							(tagged[2][1]=="IN")
							or
							(tagged[2][1]=="CC" and h[2] not in ["but"])
							or
							#we don't need this if we are to just ignore whatever goes thru all of it
							#TEMPTEMPTEMP
							(h[0] in ["be", "other", "s", "type", "was", "work", "im", "baths", "you", "maybe", "big", "day", "o", "round", "ride", "avengers", "kids", "had", "number", "have", "like", "here", "size", "got", "are", "send", "only", "have", "go", "is", "bedroom", "but", "beautiful", "nice"])
							or
							(h[2] in ["face", "new", "faced", "wonderful", "must", "min", "short", "si", "br", "step", "start", "so", "out", "story", "bdrm", "other", "out", "story", "yr", "looking", "more", "but", "hrs", "bedroom"])
							or 
							(tagged[2][1] in ["JJ", "VBD", "VBZ", "VBG"])
							):
							#print "killed",tagged, "\n"
							pass
						
						#finding the good
						elif (
							(tagged[2][1] in ["DT", "CD", "EX", "NNS", "VB"])
							or
							(tagged[2][1] in ["JJ"] and h[0] in ["opposed"])
							or
							(tagged[2][1] in ["PRP"] and not nounregex.match(tagged[0][1]))
							or
							(h[0] == "have" and h[2] in ["browse", "force", "go", "send", "talk"])
							or
							(h[0] == "like" and h[2] not in ["furry", "cuz", "straight"])
							or
							(h[0] in ["here"] and nounregex.match(tagged[2][1]))
							or
							#really what we are exluding here is anything non-Verb or Noun
							# we can consider replacing this with a regex
							(h[0] in ["need", "me", "pics"] and tagged[2][1] not in ["JJ", "JJR", "MD"])
							or 
							(h[0] in ["momma", "women", "delighted", "tryn", "respond", "travel", "veldkum", "happness", "pool", "lots", "bbw", "willin", "luvz", "place", "time", "married", "pixs", "boy", "pictures", "brickz", "somebody", "memphis", "cell", "fear", "hoop", "open", "goes", "afraid", "speak", "lady", "needs", "attracted", "doms", "bottom", "head", "apply", "drive", "pic", "newer", "pinned", "luvs", "sumbody", "face", "due", "tryin", "line", "has", "close", "interested", "alot", "oral", "talk", "new", "girl", "up", "scared", "willing", "cam", "loves", "cock", "out", "u", "nice", "how", "free", "hard", "hope", "able", "someone", "man", "woman", "male", "down", "love", "luv", "ready", "want", "wants"]+["talking", "responding", "waiting", "getting","looking", "lookin", "going", "trying"])
							or
							(h[2] in ["survive", "brag", "blow", "grab", "feel", "send", "connect", "hearing", "say", "read", "contact", "please", "run", "host","kno", "talk", "just", "add", "text", "chill", "hang", "date", "find", "chat", "show", "u", "meet", "her", "hear", "me", "my", "b", "know", "play", "do", "suck", "go", "get", "fuck"])
							):
							#print "hooked the plusloop", tagged
							print tagged
							results.append(tagged)
							h0dict[h[0]]=h0dict[h[0]]+1
 							h2dict[h[2]]=h2dict[h[2]]+1
						else:
							pass
									
		print "We have {} items with a token count of {}".format(len(h0dict.keys()), sum(h0dict.values()))
		h0dict={k:v for k,v in h0dict.items() if v > 0}
		print "\n\n", number, "\npretext here be the results\n\n"
		for entry in sorted(h0dict, key=h0dict.get, reverse=True):
			print entry, h0dict[entry]
		print "We have {} post items with a token count of {}".format(len(h2dict.keys()), sum(h2dict.values()))
		for entry in sorted(h2dict, key=h2dict.get, reverse=True):
			print entry, h2dict[entry]
		print "We have {} pre items with a token count of {}".format(len(h0dict.keys()), sum(h0dict.values()))
		return results


			
x=rebusfinder_to('/home/ps22344/Downloads/craig_0208', "worddict_full.json", numberdict, "b")


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
	

