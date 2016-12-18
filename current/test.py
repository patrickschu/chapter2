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


import time
import codecs
import json
import re
import os
import clustertools as ct
import tokenfinder_1004 as tk
from collections import defaultdict
from nltk import pos_tag
from string import punctuation
print punctuation




def rebusfinder_too(input_path):
	"""
	The rebus_too finder.
	It uses a list of expressions, pre-established thru "identifying_rebus_too_1022.py", to count 
	instances where a writer uses "2" instead of "too". 
	"""
	#regexes and utilities
	exclude_post_context=["+",  "(", "%"]#re.compile(r"^"+i+"$") for i in exclude_post_context]
	punctuationregex="+|".join([re.escape(i) for i in [l for l in list(punctuation) if not l in exclude_post_context]])
	#written numbers for quality control
	writtennumberdict={}
	writtennumbers=["zero", "one","two","three","four","five","six","seven","eight","nine","ten","eleven","twelve","thirteen","fourteen", "twenty", "thirty", "fourty", "fifty", "sixty", "fivefivefive"]	
	for writtennumber in writtennumbers:
		writtennumberdict[writtennumber]=0

	postwords= ["pickey", "far", "late", "much", "many", "heavy", "old"]
	prewords_withpunct= ["ability", "head", "company", "cool", "full"]
	prewords= ["band", "ass" ,"groups", "ub", "join"]

	predict=defaultdict(int)
	postdict=defaultdict(int)
	
	for number in [2]:
		results=[]
		#this is the regular expression to identify instances of the number studied
		numberregex=re.compile("\W([a-z]+)\s*("+punctuationregex+")?\s*("+unicode(number)+")(?:\s+)?("+punctuationregex+")?(?:\s+)?([a-z]+)\W")
		print numberregex.pattern
		#dicts to store statistics about context of number
		h0dict=defaultdict(int)
		h2dict=defaultdict(int)
		#lists to store results and previous search patterns fed into tokenfinder to avoid duplicate output
		previous_patterns=[]
		results=[]
		for pati in [i for i in os.listdir(input_path) if not i.startswith(".")]:
			for fil in [i for i in os.listdir(os.path.join(input_path, pati)) if not i.startswith(".")]:
				result=[]
				fili=codecs.open(os.path.join(input_path, pati, fil), "r", "utf-8")
				inputad=ct.adtextextractor(fili.read(), fil)
				inputad=ct.adcleaner(inputad, replace_linebreak=True)
				inputad=inputad.lower()
				wordcount=float(len(ct.tokenizer(inputad)))
				hits=numberregex.findall(inputad)
				#this weeds out all the phonenumbers. 
				hits=[h for h in hits if h[0] not in writtennumberdict and h[2] not in writtennumberdict]
				#if len(hits) > 0:
				#	print "\n len hits", len(hits)
				for h in hits:
					#this is needed for instance where there is no punctuation
					h=[" " if i == "" else i for i in h]
					"""
					thus
					[(u'of', 'IN'), (u'2', 'CD'), (u',', ','), (u'single', 'JJ')]
					pre, "2", optional punctuation, post
					"""
					[pre, pre_punct, number, punct, post]=pos_tag(h)
					
					if (
									
					#unique items catcher
					(pre[0] in ["date"]) 
					or
					(pre[0] in ["it"] and post[0] in ["i"])
					or
					(pre[0] in ["cook"] and post[0] in ["im"])
					or
					(pre[0] in ["kids"] and post[0] in ["young"]) 
					or
					(pre[0] in ["life", "way"] and post[0] in ["short"])
					or
					(pre[0] in ["that"] and post[0] in ["hard"])
					or
					(pre[0] in ["real"] and post[0] in ["hope"])
					or
					(pre[0] in ["me"] and post[0] in ["if"])
					or
					(pre[0] in ["dogs"] and post[0] in ["if"])
					or
					(pre[0] in ["can"] and post[0] in ["but"])
					or
					(pre[0] in ["kool"] and not post[0] in ["even"])
					or
					(pre[0] in ["on"] and punct[0] not in [" "] and inputad.split()[inputad.split().index(pre[0])-1] == "later")# and (h[h.index(pre[0])] == "later"))
					or
					(pre[0] in ["love"] and punct[0] not in [" "] and post[0] in ["msg"])
					or
					(pre[0] in ["real"] and post[0] in ["have"])
					or
					#BIGGER NETS
					#you be too in front of punctuation catch
					(pre[0] in ["be", "b", "are", "r"] and punct[0] not in [" ", "-", ")"])
					or
					#this is if we know the pre-word and 2 is followed by punctuation
					# cf 'intellectualy ability 2. '
					(pre[0] in prewords_withpunct and punct[0] not in [" ", ")", ":"])
					or
					#this is if we know the word to follow
					# cf 'not 2 late.' collected in postwords
					(post[0] in postwords)
					or
					#this is if we know the word to precede
					(pre[0] in prewords)
					):
					
						#print "\n\n***", [pre, number, punct, post], "**\n", os.path.join(input_path, pati, fil)
						#results.append((pre, number, punct, post, os.path.join(input_path, pati, fil)))
						predict[pre[0]]=predict[pre[0]]+1
						postdict[post[0]]=postdict[post[0]]+1
						result.append(1)
						print h
						#if result[0] > 10: 
						#	print "result for file", len(result), result, #os.path.join(input_path, pati, fil)
				results.append([(len(result), len(result)/wordcount)])
				if sum(result) > 1:
					print "result for file", len(result), result, os.path.join(input_path, pati, fil)
					print results
					
				#print "len results", len(results)
		
		print "original result list is", len(results)
		print "PRE CONTEXT"
		print "\n".join([": ".join([k, unicode(predict[k])]) for k in sorted(predict, key=predict.get, reverse=True)])
		print "POST CONTEXT"
		print "\n".join([": ".join([k, unicode(postdict[k])]) for k in sorted(postdict, key=postdict.get, reverse=True)])
		print "shape of results, number of lists:", len(results),  "-- length of lists", set([len(i) for i in results])
		#for u in [[x[1] for x in i] for i in results]:
		#	print u
		return [[x[0] for x in i] for i in results], [[x[1] for x in i] for i in results]




rebusfinder_too("/home/ps22344/Downloads/craig_0208")
















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



def rebusfinder_to(input_dir):
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
	Returns a list of lists where each list contains raw and per word counts. 
	"""
	nounregex=re.compile("NN.?")
	exclude_post_context=["inche?s?", "wks?", "nd", "i", "sec", "stepping", "asap", "tattoos", "years?", "yrs", "months?", "weeks?", "days?", "hours?", "times?", "peoples?", "(boy|girl)?friends?", "(p|a)\.?m\.?", "to", "or", "full", "wana" ]
	exclude_post_context=[re.compile(r"^"+i+"$") for i in exclude_post_context]
	exclude_pre_context=["borderlands", "chicago", "c?ops?", "till?", "or", "and", "just", "f(oo|ee)?t", "last", "own", "hsv", "herpes"]
	exclude_pre_context=[re.compile(r"^"+i+"$") for i in exclude_pre_context]
	search_terms=[2]
	for number in search_terms:
		numberregex=re.compile("\W([a-z]+)\s+("+unicode(number)+")\s+([a-z]+)\W")
		#just for now
		h0dict=defaultdict(int)
		h2dict=defaultdict(int)
		print numberregex.pattern
		results=[]
		for pati in [i for i in os.listdir(input_dir) if not i.startswith(".")]:
			for fil in [i for i in os.listdir(os.path.join(input_dir, pati)) if not i.startswith(".")]:
				result=[]
				fili=codecs.open(os.path.join(input_dir, pati, fil), "r", "utf-8")
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
							#print fil, "len tagged", type(tagged)
							result.append(tagged)
							#print "len result", len(result)
							h0dict[h[0]]=h0dict[h[0]]+1
 							h2dict[h[2]]=h2dict[h[2]]+1
						else:
							pass
				results.append([(len(result), len(result)/wordcount)])
				#print [(len(result), len(result)/wordcount)]
		print "We have {} items with a token count of {}".format(len(h0dict.keys()), sum(h0dict.values()))
		h0dict={k:v for k,v in h0dict.items() if v > 3}
		h2dict={k:v for k,v in h2dict.items() if v > 3}
		print "\n\n", number, "\npretext here be the results\n\n"
		for entry in sorted(h0dict, key=h0dict.get, reverse=True):
			print entry, h0dict[entry]
		print "We have {} post items with a token count of {}".format(len(h2dict.keys()), sum(h2dict.values()))
		for entry in sorted(h2dict, key=h2dict.get, reverse=True):
			print entry, h2dict[entry]
		print "We have {} pre items with a token count of {}".format(len(h0dict.keys()), sum(h0dict.values()))
		#print [i for i in results if sum(i[0]) > 2]
		#print results
		print "shape of results, number of lists:", len(results),  "-- length of lists", set([len(i) for i in results])
		return [[x[0] for x in i] for i in results], [[x[1] for x in i] for i in results]


			



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
	

