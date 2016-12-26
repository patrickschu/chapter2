"""
This compiles all the tools needed for extraction of e-grammar features as defined by Herring.
"""
# BE FLEXIBLE WITH INPUT DATA SET SO WE CAN USE FULL OR BALANCED
# BE SOMEWHAT FLEXIBLE IN HOW WE AGGRAGATE OVER FEATURES
# So we need dir as input
# do we want corpus counts as result or featurelists
# maybe: dict={feature:count, feature_2: count, ...}
# we make lists to be glued together in numpy column_stack
# the returns consist of lists, each representing a file. 
# the file list consists of a tuple for each feature that contains (raw count, frequency per word). 


import numpy as np
from string import punctuation
import re
import clustertools as ct
import time
import os
import codecs
from collections import defaultdict
import json
from nltk.tag import pos_tag

#helper funcs
def anyoftheseregex(regexstring):
	"""
	The anyofthesregex iterates over all instances with "+" in a regex to construct a new pattern.
	THe new pattern replaces one instance of + with a {2,}. 
	Thus, this will get us a string to match Hhello, Heeeeello but not Hheello.
	"""
	print "we run the anyoftheseregex on", regexstring
	#print regexstring.split("+")
	result=[i for i in regexstring.split("+") if i]
	outputregex=[]
	for number, item in enumerate(result):
		temp=[i for i in regexstring.split("+") if i]
		temp[number]=item+"{2,}"
		outputregex.append(temp)
		
	anyregex=")|(?:".join(["".join(i) for i in outputregex])
	print "((?:"+anyregex+"))"
	return "((?:"+anyregex+"))"


###SECTION 1
###TYPOGRAPHY


def emoticonfinder(dir):
	"""
	THIS STILL NEEDS THE OUTPUT FUNCTION OF PUNCTFINDER
	The emoticonfinder takes a directory with corpus files as input. 
	It returns a list of lists with counts of each emoticon in each file in dir.
	Emoticons are read from file.
	list=[[x1feature1, x1feature2, ...], [x2feature1, x2feature2, ...]]
	We might consider making the file with emoticons an argument as well. 
	--- Original Source file is /Users/ps22344/Downloads/chapter2/current/emoticoncounter.py ---
	"""
	print "RUNNING EMOTICONFINDER"
	starttime=time.time()
	#creating a featuredict from file
	featuredict={}
	search_terms=[]
	results=[]
	resultdict=defaultdict(float)
	
	with codecs.open('/home/ps22344/Downloads/chapter2/textfiles/emolist_final_2.txt', "r", "utf-8") as inputtext:
		for line in inputtext.readlines():
			#print line.rstrip("\n")
			search_terms.append(re.compile("\W("+re.escape(line.rstrip("\n"))+")(?: |<)"))
		
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
			# if 11 > sum([len(i) for i in result]) > 6:
				# for n, i in enumerate(result):
					# if len(i) > 0:
						# print search_terms[n].pattern, n,i
				# print os.path.join(dir, pati, fili), "\n"
				# os.system("cygstart "+os.path.join(dir, pati, fili))
			
	endtime=time.time()
	print "This took us {} minutes".format((endtime-starttime)/60)
	print "\n\n"
	resultdict={search_terms[k].pattern:v for k,v in resultdict.items() if v > 0}
	for k in sorted(resultdict, key=resultdict.get, reverse=True):
		print k, resultdict[k]
	print "shape of results, number of lists:", len(results),  "-- length of lists", set([len(i) for i in results])
	#1st list is absolute counts, 2nd div by word count
	return ([[x[0] for x in i] for i in results], [[x[1] for x in i] for i in results])

def repeatedpunctuationfinder(dir):
	"""
	The repeatedpunctuationfinder uses string.punctuation to create a dictionary of regexes.
	These are used to identify non-Standard usage of punctuation. 
	Note how we hardcoded the ?!? variants into the punctuationdict from the start. 
	Iterates over files contained in dir.
	Returns two lists; first is absolute counts, the second relative counts	
	-- Source file is /Users/ps22344/Downloads/chapter2/current/punctuationcounter_0927.py ---
	"""
	print "RUNNING REPEATEDPUNCTUATIONFINDER"
	starttime=time.time()
	#creating a featuredict from file
	results=[]
	resultdict=defaultdict(float)
	punctuationdict={
	re.compile(r"(?:\s|\w)(!\?|\?!)(?:\s|\w)"):0
	}

	for stringi in punctuation:
		#print stringi, "-->", re.escape(stringi)
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
			if sum([len(i) for i in result]) > 80:
				for n, i in enumerate(result):
					 if len(i) > 0:
						 print search_terms[n].pattern, n,i, "len", len(i)
				print os.path.join(dir, pati, fili), "\n"
				#os.system("cygstart "+os.path.join(dir, pati, fili))
			
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
	return ([[x[0] for x in i] for i in results], [[x[1] for x in i] for i in results])


def leetcounter(dir):
	"""
	The leetcounter identifies any words that exhibit leet features, e.g. name --> nam3 
	The list this is based on was made in /Users/ps22344/Downloads/chapter2/current/identifying_leetspeak_1008.py
	Iterates over files contained in dir.
	Returns two lists; first is absolute counts, the second relative counts	 
	Inspired by  http://www.gamehouse.com/blog/leet-speak-cheat-sheet/
	"""
	print "\nRUNNING LEETCOUNTER"
	starttime=time.time()
	featuredict={}
	search_terms=[]
	results=[]
	resultdict=defaultdict(float)
	
	with codecs.open('/home/ps22344/Downloads/chapter2/textfiles/leetwords_1216.txt', "r", "utf-8") as inputtext:
		for line in inputtext.readlines():
			#print line.rstrip("\n")
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
				#os.system("cygstart "+os.path.join(dir, pati, fili))
	endtime=time.time()
	print len(results), "files processed"
	print "\n\n"
	resultdict={search_terms[k].pattern:v for k,v in resultdict.items() if v > 0}
	for k in sorted(resultdict, key=resultdict.get, reverse=True):
		print k, resultdict[k]
	print "shape of results, number of lists:", len(results),  "-- length of lists", set([len(i) for i in results])
	print "This took us {} minutes".format((endtime-starttime)/60)
	#1st list is absolute counts, 2nd div by word count
	return ([[x[0] for x in i] for i in results], [[x[1] for x in i] for i in results])


#the rebusfinder needs to be here; it finds instances of "4" for "for". 
def rebusfinder_for(input_path):
	"""
 	This finds words that are represented as numbers. 
 	All combinations \W([a-z]+)\s+("+unicode(number)+")\s+([a-z]+)\W for the number put in are identified.
 	The lists exclude_pre and exclude_post word for negative contexts in 4.
 	Returns two lists; first is absolute counts, the second relative counts	. 
	"""
	print "\nRUNNING REBUSFINDER FOR"
	
	writtennumberdict={}
	#these are exclude and include contexts we need
	writtennumbers=["zero", "one","two","three","four","five","six","seven","eight","nine","ten","eleven","twelve","thirteen","fourteen", "twenty", "thirty", "fourty", "fifty", "sixty"]	

	for writtennumber in writtennumbers:
		writtennumberdict[writtennumber]=0

	exclude_post_context=["fingers","nights", "weeling","wheel",  "s", "am", "a.m.", "figures", "pm", "p.m.","dogs","tattoos", "emails", "foot", "feet", "ft", "children", "guy", "just", "of", "to", "i", "year", "years", "yr", "yrs", "days", "wheeler", "wheelers", "wheeling", "times", "or", "and", "months", "in", "kids", "weeks", "day", "days"]
	exclude_pre_context= ["battlefield", "minimum", "but", "from", "got", "be", "this", "n", "first","only", "these", "has", "all", "are", "and", "feb", "april", "july", "number", "about", "playstation", "our", "on", "sleep","thanks","bedroom", "fine","before","had","except", "acres", "no", "in", "b", "with", "size", "a", "to","have", "of", "or", "the", "for", "feet", "foot", "ft", "my", "your"]+["young","incredable","friendly","very","eiight","every","servicing","like","quick","sev","our","giving","stage","last","son","speak","use","top","least","until","survived","than","those","is","buffy","im","at","after","know"]+[u'holding', u'ad', u'oh', u'gta', u'dogs', u'her', u'look', u'eyes', u'mind', u'make', u'figured', u'nearly', u'lodging', u'marred', u'start', u'taken', u'plus', u'truck', u'own', u'prefers', u'favorite', u'doorsopened', u'weather', u'other', u'gym', u'tandem', u'tongue', u'past', u'who', u'female', u'round', u'as', u'put', u'decent', u'raised', u'fairs', u'driving', u'that', u'beach', u'beach', u'just', u'country', u'carry', u'she', u'shine', u'seen', u'sober', u'dogs', u'same', u'friend', u'hmu', u'time', u'nice', u'guy', u'guy', u's', u'almost', u'o', u'unforgettable', u'zro', u'zro', u'hace', u'hoping', u'other', u'horny', u'regularly', u'nice', u'harts', u'now', u'beg', u'same', u'offing', u'answer', u'host', u'married', u'head', u'befor', u'thick', u'gym', u'f', u'drive', u'hair', u'owned', u're', u'park', u'smash', u'into', u'phase', u'havin', u'wednesday', u'large', u'finding', u'over', u'within', u'run', u'owned', u'answer', u'she', u'sitter', u'apr', u'apr', u'random', u'us', u'taking', u'hotel', u'fishing', u'were', u'interested', u'evil', u'events', u'supported', u'lvl', u'literally', u'may', u's', u'extinct', u'sending', u'hp', u'hp', u'suffered', u'waiting', u'pay', u'extinct', u'til', u'done', u'play', u'beautiful', u'then', u'plus', u'approx', u'lives', u'literally', u'get', u'found', u'someone', u'insert']

	include_pre_context=["pay", "m", "w", "up", "swf","love", "here", "not", "there", "ready","lkng","me", "ask", "live", "cheer", "grateful", "thanks", "partner", "men", "man", "male", "woman", "women","looking", "lookin", "pic", "pix", "lookn", "pics", "picture", "photo"]
	include_post_context=["swf","yu","who", "dead", "reading", "over", "help", "life", "your", "the", "a", "my", "our", "an", "real", "you", "u", "me", "ltr", "play", "same", "whatever", "sex", "someone", "fun"]
	
	results=[]
	for number in [4]:
		numberregex=re.compile("\W([a-z]+)\s+("+unicode(number)+")\s+([a-z]+)\W")
		#just for now
		h0dict=defaultdict(int)
		h2dict=defaultdict(int)
		print numberregex.pattern
		for pati in [i for i in os.listdir(input_path) if not i.startswith(".")]:
			print pati
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
		print "\n".join([": ".join([k, unicode(h0dict[k])]) for k in sorted(h0dict, key=h0dict.get, reverse=True)])
		print "\n".join([": ".join([k, unicode(h2dict[k])]) for k in sorted(h2dict, key=h2dict.get, reverse=True)])

		print "We have {} post items with a token count of {}".format(len(h2dict.keys()), sum(h2dict.values()))
		print "We have {} pre items with a token count of {}".format(len(h0dict.keys()), sum(h0dict.values()))
		return [np.array([[x[0] for x in i] for i in results]), np.array([[x[1] for x in i] for i in results])]

# the rebusfinder 2 needs to be here; it finds instances of "2" for "to".

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
	Based on /Users/ps22344/Downloads/chapter2/current/identifying_rebus_2_1012.py
	Returns a list of lists where each list contains raw and per word counts. 
	"""
	print "RUNNING REBUSFINDER TO"
	#written numbers for quality control
	writtennumberdict={}
	
	writtennumbers=["zero", "one","two","three","four","five","six","seven","eight","nine","ten","eleven","twelve","thirteen","fourteen", "twenty", "thirty", "fourty", "fifty", "sixty", "fivefivefive"]	

	for writtennumber in writtennumbers:
		writtennumberdict[writtennumber]=0
	
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
			print pati
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
		return [np.array([[x[0] for x in i] for i in results]), np.array([[x[1] for x in i] for i in results])]


def rebusfinder_too(input_path):
	"""
	The rebus_too finder.
	It uses a list of expressions, pre-established thru "identifying_rebus_too_1022.py", to count 
	instances where a writer uses "2" instead of "too". 
	Based on rebusfinder_too_1108.
	Returns a list of lists where each list contains raw and per word counts. 
	"""
	print "RUNNING REBUSFINDER TOO"
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
			print pati
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
						#print h
						#if result[0] > 10: 
						#	print "result for file", len(result), result, #os.path.join(input_path, pati, fil)
				results.append([(len(result), len(result)/wordcount)])
				if sum(result) > 1:
					print "result for file", len(result), result, os.path.join(input_path, pati, fil)
					#print results
					
				#print "len results", len(results)
		
		print "original result list is", len(results)
		print "PRE CONTEXT"
		print "\n".join([": ".join([k, unicode(predict[k])]) for k in sorted(predict, key=predict.get, reverse=True)])
		print "POST CONTEXT"
		print "\n".join([": ".join([k, unicode(postdict[k])]) for k in sorted(postdict, key=postdict.get, reverse=True)])
		print "shape of results, number of lists:", len(results),  "-- length of lists", set([len(i) for i in results])
		#for u in [[x[1] for x in i] for i in results]:
		#	print u
		return [np.array([[x[0] for x in i] for i in results]), np.array([[x[1] for x in i] for i in results])]

		
def capsfinder(input_dir, limit):
	"""
	The capsfinder finds instances of non-Standard capitalization. 
	Items such as iPhone or ReTro as well as straightforward THINGS. 
	input_dir is the folder with corpus files to iterate over.
	limit sets the ratio of words that can be capitalized at the most, supposed to address the files that are all caps. This is a 0 to 1 ratio, i.e. 0.5 is half of all words capitalized, camelcased, etc. 
	do we want switch over at this point and count the lowercase ones?
	Based on capsfinder_1203.py.
	Returns a list of lists where each list contains raw and per word counts.
	"""
	print "RUNNING CAPSFINDER"
	capsdict={
	re.compile("\W+([A-Z]{3,})\W+"):"all caps",
	re.compile("\W+([a-z]+[A-Z]+(?:[a-z]+)?(?:[A-Z]+)?)\W"):"PascalCase",
	re.compile("\W+([A-Z]+[a-z]+[A-Z]+(?:[a-z]+)?)\W"):"CamelCase"
	}
	print {i.pattern for i,v in capsdict.items()}
	
	abbreviations=["LTR"]
	results=[]
	#dicti is results by word/item
	dicti=defaultdict(float)
	#matchesdicti is results by Regexpattern
	matchesdicti=defaultdict(list)
	search_terms=[i for i in capsdict.keys()]
	print "search terms",  [i.pattern for i in search_terms]
	for dir in [i for i in os.listdir(input_dir) if not i.startswith(".")]:
		print dir
		for fili in [i for i in os.listdir(os.path.join(input_dir, dir)) if not i.startswith(".")]:
			with codecs.open(os.path.join(input_dir, dir, fili), "r", "utf-8") as inputtext:
				inputad=ct.adtextextractor(inputtext.read(), fili)
			#we exclude anything we have in our abbreviations dict
			#no, we cover this by subtracting the results later
			result=[([t for t in i.findall(inputad) if not t in abbreviations], i.pattern) for i in search_terms] 
			#print result
			wordcount=float(len(ct.tokenizer(inputad)))
			#this is the count we returs
			results.append([(len(matches), (len(matches))/wordcount) for matches, pattern in result])
			#print "\n\n\n-----\n", results, wordcount
			#here we inspect findings. note resultS vs result
			for matches, pattern in result:
				if len(matches)/wordcount > limit:
					print "WARNING: matches higher than limit: matches {}, wordcount {}, in {}".format(len(matches), wordcount, os.path.join(input_dir, dir, fili))
					#the dicti is {pattern:count, pattern: count, ...}
				for res in matches:
					dicti[res]=dicti[res]+1
					#print len(matches[0]), 'total', len(matches)
					#matchesdicti collects the matches per regex, dicti per feature
					matchesdicti[pattern]=matchesdicti[pattern]+matches
	#print "\n".join([":".join((i, str(dicti[i]))) for i in sorted(dicti, key=dicti.get, reverse=True) if dicti[i] > 100])	
	for entry in {k:v for k,v in matchesdicti.items()}:
 		print "\n", entry, len(set([i for i in matchesdicti[entry]]))
	print "shape of results, number of lists:", len(results),  "-- length of lists", set([len(i) for i in results])
	return [np.array([[x[0] for x in i] for i in results]), np.array([[x[1] for x in i] for i in results])]


def singleletterfinder(input_dir):
	"""
	Finds individual characters representing an entire word.
	Example: C U for see you. 
	Based on charactercounter_1129.py.
	Returns a list of lists where each list contains raw and per word counts.
	"""
	print "RUNNING SINGLELETTERFINDER"
	start=time.time()
	#helper funcs
	def capitalizer(input_list):
		"""
		returns a list with inputword|inputword.upper() to feed into regex
		"""
		return [i.upper()+"|"+i for i in input_list]
	#where (?<!x) means "only if it doesn't have "x" before this point"
	capitalrprewords=[]
	capitalrpostwords=[]
	
	#finished
	xpostwords=["army", "navy", "wife", "husband", "gf", "girlfriends?", "drug", "baggage", "drama", "user", "boy", "of low", "anything", " hockey", "slaves", "relationship"]
	xprewords=["[Mm]y", "[Ii]'m", "[Yy]our"]
	cpostwords=["where","when","how (?:things|we)", "[Yy][Aa]"]
	cprewords=[" 2", "[^ f] u", "U", "[Tt][Oo]","[Ll][Ee][Tt]'?s?", "[Cc]ould","can","will", "up", "I'll"]
	upostwords=["(?!of )"]

	counterdict={
	"xX":["(?:"+"|".join(capitalizer(xprewords))+")\W+([Xx])\W+" , "\W+([Xx])\W+(?:"+"|".join(capitalizer(xpostwords))+")"],
	"cC":["(?:"+"|".join(cprewords)+")\s+([Cc])\s+" , "\s+([Cc])\s+(?:"+"|".join(cpostwords)+")"],
	"u":["\s+(u)\s+"],
	"U":["\s+(U)\s+"+"".join(upostwords)],
	"r":["(?<!(e|g|t))\s+(r)\s+(?!and b |\&amp;)"],
	"R":["(?<!rated|Cocks| [Tt]oys|Girls|[A-Z] [A-Z] [A-Z])\s+(R)\s+(?![A-Z] [A-Z]|R |B |AND [R|B]|&amp;)"],
	"b":["(?<! size|r and)\s+(b)\s+(?!day |cups?|tits|e |or larger)"],
	"B": ["(?<![A|R] AND| Part|. F W|&amp;)\s+(B)\s+(?!cups?|tits|level|average|horror|rated|movie|in the world|S |Q |and W |B? ?W)"],
	"N": ["(?<![A-Z] [A-Z]|Ave| MA)\s+(N)\s+(?!Houston|Ballard|word|Royaton|Wilmot|Tucson|Dallas|Warren|side|Avalon|St Pete|Scottsdale|Tampa|C[Oo][Uu][Nn][Tt][Yy]|[Rr][Oo][Ll][Ll]|Arl\.|Royaltown|Golden Isles|Oeleans|Ballard Rd|Broward|Ward|angola|Oracle|[Hubert|1st] Ave|European|Tryon|Hill\w+ |Wil\w+|[Ss][Uu][Bb][Jj][Ee][Cc][Tt]|state line|for now|with a dick|OT |of (\s+Dayton|Talla\w+)|THE INSIDE|THE SURROUNDING|TIME|AUGHTY|[A-Z] [A-Z] |&amp; 5th)"],
	"n": ["(?<!I'm| im|ver|sia)\s+(n)\s+(?!shape|city|town|Bismarck|[Rr]oses| b |subject|[Nn]orth|the subject|[Rr][Oo][Ll][Ll]|[0-9] [0-9])"]
	}
		
	results=[]
	dicti=defaultdict(float)
	matchesdicti=defaultdict(list)
	search_terms=[re.compile("|".join(i)) for i in counterdict.values()]
	print "search terms",  len([i.pattern for i in search_terms])
	for dir in [i for i in os.listdir(input_dir) if not i.startswith(".")]:
		print dir
		for fili in [i for i in os.listdir(os.path.join(input_dir, dir)) if not i.startswith(".")]:
			with codecs.open(os.path.join(input_dir, dir, fili), "r", "utf-8") as inputtext:
				inputad=ct.adtextextractor(inputtext.read(), fili)
			#result is a list of lists which contain matches for each regex/acronym
			#the list incomprehension just deletes empty search results from the "|" search
			wordcount=float(len(ct.tokenizer(inputad)))
			result=[([t for m in i.findall(inputad) for t in m if t], i.pattern) for i in search_terms] 
			#print result
			results.append([(len(matches), len(matches)/wordcount) for matches, pattern in result])
			for matches, pattern in result:
				if len(matches) > 0:
				#	print "multiple matches", matches, os.path.join(input_dir, dir, fili)
					#the dicti is {pattern:count, pattern: count, ...}
					for res in matches[0]:
						dicti[res]=dicti[res]+1
						#matchesdicti collects the matches per regex, dicti per feature
						matchesdicti[pattern]=matchesdicti[pattern]+matches
	for entry in {k:v for k,v in matchesdicti.items()}:
		print "\n", entry, set(matchesdicti[entry])
	for entry in sorted(dicti, key=dicti.get, reverse=True):
		print entry, dicti[entry]
	print "shape of results, number of lists:", len(results),  "-- length of lists", set([len(i) for i in results])
	end=time.time()
	print "This took us {} minutes".format((end-start)/60)
	#for u in [[x[1] for x in i] for i in results]:
	#	print u
	return [[x[0] for x in i] for i in results], [[x[1] for x in i] for i in results]  

###SECTION 2
###ORTHOGRAPHY

#spelling correctness?
def spellingcounter(input_dir):
    """
    The spellingcounter counts the number of mis-spelled words.
    It uses the PyEnchange library for spellchecking.
    It iterates over the files in input_dir.
    It returns a lists of lists with (raw count, relative count) tuples.
	Based on spellingcounter_1216
    """
    print "RUNNING SPELLINGCOUNTER"
    start=time.time()
    americandict = enchant.Dict("en_US")
    goodwords=set(["wo", "'ve", "'m", "n't", "'s", "'ll", "'re", "'d", "non-"]+list(string.punctuation))
    htmlregex=re.compile("<.*?>")
    results=[]
    for pati in [i for i in os.listdir(input_dir) if not i.startswith(".")]:
        print pati
        for fili in [i for i in os.listdir(os.path.join(input_dir, pati)) if not i.startswith(".")]:
            #print fili
            result=[]
            fili=codecs.open(os.path.join(input_dir, pati, fili), "r", "utf-8")
            inputad=ct.adtextextractor(fili.read(), fili)
            inputad=htmlregex.sub(" ", inputad)
            words=ct.tokenizer(inputad)
            #print "\n\n\n", words
            wordcount=float(len(words))
            mistakes=[w for w in words if not americandict.check(w) and w not in goodwords]
            #print mistakes
            if wordcount-len(mistakes) < 0:
                 print "WARNING: negative count-mistakes", wordcount, len(correct), os.path.join(input_dir, pati, fili)
            results.append([(len(mistakes), len(mistakes)/wordcount)])
            #print "\n".join([":".join([i, str(dict[i])]) for i in sorted(dict, key=dict.get, reverse=True)])
    end=time.time()
    print "len results", len(results)
    print "this took us {} minutes".format((end-start)/60)
    print "shape of results, number of lists:", len(results),  "-- length of lists", set([len(i) for i in results])
    #for u in [[x[1] for x in i] for i in results]:
    #    print u
    #print [[x[0] for x in i] for i in results], [[x[1] for x in i] for i in results]
    return [[x[0] for x in i] for i in results], [[x[1] for x in i] for i in results]

#clippings
def clippingcounter(input_dir):
	"""
	The clipping uses the clipping_list to count instances	of the clippings listed in there. 
	Here, we make that list out of the shorteningdict jsons created earlier. 
	The regex is designed to find lowercase and uppercase versions of each, plus plurals.
	The input_dir contains the text files to be iterated over. 
	Returns a list of lists where each list contains raw and per word counts.
	Based on /chapter2/current/clippingcounter_1120.py
	"""
	print "RUNNING CLIPPINGCOUNTER"
	start=time.time()
	#creating the search terms
	filelist=[
	'clippingfiles/clippingdict_catsfinal_post_3chars_1121.json',
	'clippingfiles/clippingdict_catsfinal_post_4chars_1121.json',
	'clippingfiles/clippingdict_catsfinal_post_5chars_1121.json',
	'clippingfiles/clippingdict_catsfinal_post_6chars_1121.json',
	'clippingfiles/clippingdict_catsfinal_yes_2chars_1121.json',
	'clippingfiles/clippingdict_catsfinal_yes_3chars_1121.json',
	'clippingfiles/clippingdict_catsfinal_yes_4chars_1121.json',
	'clippingfiles/clippingdict_catsfinal_yes_5chars_1121.json',
	'clippingfiles/clippingdict_catsfinal_yes_6chars_1121.json',
	'clippingfiles/clippingdict_catsfinal_yes_7chars_1121.json'
	]

	search_terms = []

	for fili in filelist:
		with codecs.open(fili, "r", "utf-8") as inputfile:
			acronym_dict=json.load(inputfile)
			for key in [i for i in acronym_dict.keys() if i not in ["delete", "other"]]:
				for cat in ['X']:
					#print "adding", acronym_dict[key][cat]
					search_terms = search_terms + acronym_dict[key][cat]
				for cat in ['noun']:
	 				#special treatment for nouns to accept plurals
					print "adding", acronym_dict[key][cat]
					search_terms = search_terms + [i if i in ["loc", "les", "sis"] else i + "s?" for i in acronym_dict[key][cat]]
	print "we have {} search terms".format(len(search_terms))
	print "we have {} set search terms".format(len(set(search_terms)))
	
	clipping_list=search_terms
	#start actual counting		
	excludelist=[]
	
	#dicts to store results
	dicti=defaultdict(float)
	matchesdicti=defaultdict(list)
	results=[]
	
	clipping_list=[re.compile("[^web|i]\W("+i+")\W") if i in ["cams?", "sites?"] else re.compile("\W("+i+")\W") for i in clipping_list]
	#clipping_list=[re.compile("\W("+i+")\W") for i in clipping_list]
	clipping_list=set(clipping_list)
	#print [i.pattern for i in clipping_list]
	#iterate and match
	for dir in [i for i in os.listdir(input_dir) if not i.startswith(".")]:
		print dir
		for fili in [i for i in os.listdir(os.path.join(input_dir, dir)) if not i.startswith(".")]:
			with codecs.open(os.path.join(input_dir, dir, fili), "r", "utf-8") as inputtext:
				inputad=ct.adtextextractor(inputtext.read(), fili).lower()
			#result is a list of lists which contain matches for each regex/acronym
			wordcount=float(len(ct.tokenizer(inputad)))
			result=[([m for m in i.findall(inputad) if not m in 
			excludelist], i.pattern) for i in clipping_list] 
			# o=[(r,os.path.join(input_dir, dir, fili)) for r in result if len(r[0]) > 2]
# 				if o:
# 					print o
			results.append([(len(matches), len(matches)/wordcount) for matches, pattern in result])
			for matches, pattern in result:
				#the dicti is {pattern:count, pattern: count, ...}
				dicti[pattern]=dicti[pattern]+len(matches)
				matchesdicti[pattern]=matchesdicti[pattern]+matches
	print "\n".join([":".join((i, str(dicti[i]), "|".join(set(matchesdicti[i])))) for i in sorted(dicti, key=dicti.get, reverse=True)])	
	#for entry in {k:v for k,v in matchesdicti.items() if v > 10}:
	#	print entry

	end=time.time()
	print "This took us {} minutes".format((end-start)/60)
	#for u in [[x[1] for x in i] for i in results]:
	#	print u
	print "shape of results, number of lists:", len(results),  "-- length of lists", set([len(i) for i in results])
	#for u in [[x[1] for x in i] for i in results]:
	#	print u
	return [[x[0] for x in i] for i in results], [[x[1] for x in i] for i in results] 


#abbreviations
def acronymcounter(input_dir):
	"""
	The acronymcounter counts acronyms and abbreviations. 
	I.e. things such as LOL, lol and LTR, ltr. 
	The input_dir contains the text files to be iterated over. 
	It relies on a&a previously IDd in the acronymfinder. 
	Here, we make that list out of the shorteningdict jsons created earlier. 
	The regex is designed to find lowercase and uppercase versions of each, plus plurals.
	Undesired plurals are in the exclude_list. 
	Returns a list of lists where each list contains raw and per word counts.
	This is based on chapter2/current/acronymcounter_1115.py.
	NOTE:we can consider running location and schools over a different regex that does not include plural s.
	"""
	print "RUNNING ACRONYMCOUNTER"
	start=time.time()
	filelist=[
	"abbreviationfiles/shorteningdict_2_1115.json",
	"abbreviationfiles/shorteningdict_3_1115.json",
	"abbreviationfiles/shorteningdict_4_1115.json",
	"abbreviationfiles/shorteningdict_5_1115.json",
	"abbreviationfiles/shorteningdict_6_1115.json"
	]

	search_terms = []

	for fili in filelist:
		with codecs.open(fili, "r", "utf-8") as inputfile:
			acronym_dict=json.load(inputfile)
		for key in [i for i in acronym_dict.keys() if i not in ["blend", "abbreviation", "clipping", "delete", "other"]]:
			for cat in ['X', 'location']:
				print "adding", acronym_dict[key][cat]
				search_terms = search_terms + acronym_dict[key][cat]

	#print search_terms
			
	print "we have {} search terms".format(len(search_terms))
		
	excludelist=set(["oks", "fbs", "PSS", "VAS", "vas", "BCS", "bcs", "NES", "nes", "SMS", "sms", "SAS", "SSS", "sss", "nsas", "mias"])
	
	#dicts to store results
	dicti=defaultdict(float)
	matchesdicti=defaultdict(list)
	results=[]
	
	#regex, lower and pluralize
	acronym_list=[re.compile("\W((?:"+i+"|"+i.lower()+")[sS]?)\W") for i in search_terms]
	acronym_list=set(acronym_list)
	#print [i.pattern for i in acronym_list]
	#iterate and match
	for dir in [i for i in os.listdir(input_dir) if not i.startswith(".")]:
		print dir
		for fili in [i for i in os.listdir(os.path.join(input_dir, dir)) if not i.startswith(".")]:
			with codecs.open(os.path.join(input_dir, dir, fili), "r", "utf-8") as inputtext:
				inputad=ct.adtextextractor(inputtext.read(), fili)
			#result is a list of lists which contain matches for each regex/acronym
			wordcount=float(len(ct.tokenizer(inputad)))
			result=[([m for m in i.findall(inputad) if not m in excludelist], i.pattern) for i in acronym_list] 
			results.append([(len(matches), len(matches)/wordcount) for matches, pattern in result])
			for matches, pattern in result:
				#the dicti is {pattern:count, pattern: count, ...}
				dicti[pattern]=dicti[pattern]+len(matches)
				matchesdicti[pattern]=matchesdicti[pattern]+matches
	print "\n".join([":".join((i, str(dicti[i]), "|".join(set(matchesdicti[i])))) for i in sorted(dicti, key=dicti.get, reverse=True) if dicti[i] > 10])
	end=time.time()
	print "This took us {} minutes".format((end-start)/60)
	#for u in [[x[1] for x in i] for i in results]:
	#	print u
	print "shape of results, number of lists:", len(results),  "-- length of lists", set([len(i) for i in results])
	#for u in [[x[1] for x in i] for i in results]:
	#	print u
	return [[x[0] for x in i] for i in results], [[x[1] for x in i] for i in results] 


#phonetically motivated letter substitution


#eye dialect


#spellings representing prosody or non-linguistic sounds such as laughter 

	"""
	The anyofthesregex iterates over all instances with "+" in a regex to construct a new pattern.
	THe new pattern replaces one instance of + with a {2,}. 
	Thus, this will get us a string to match Hhello, Heeeeello but not Hheello.
	"""
	print "we run the anyoftheseregex on", regexstring
	#print regexstring.split("+")
	result=[i for i in regexstring.split("+") if i]
	outputregex=[]
	for number, item in enumerate(result):
		temp=[i for i in regexstring.split("+") if i]
		temp[number]=item+"{2,}"
		outputregex.append(temp)
		
	anyregex=")|(?:".join(["".join(i) for i in outputregex])
	print "((?:"+anyregex+"))"
	return "((?:"+anyregex+"))"
	

def prosodycounter(input_dir):
	"""
	This finds representations of prosody and non-linguistic sounds.  
	The list of features is from non-Standard words in the corpus. 
	Returns a list of lists where each list contains raw and per word counts.
	Based on prosodycounter_1219.
	Returns a list of lists where each list contains raw and per word counts.
	"""
	print "RUNNING PROSODYCOUNTER"
	start=time.time()
	#creating the search terms
	prosodyitems=[
	"\s(\*(?:laugh|cough|smack|giggle)\*)\s",
	"\W([Ee][Rr])\W",
	"\W((?:[Hh][Aa]){1,}[Hh]?)\W",
	"\W((?:[Hh][Uu]){1,}[Hh]?)\W",
	"\W((?:[Hh][Ee]){2,}[Hh]?)\W",
	"\W([Hh][Oo]{2,})\W",
	"\W([Hh][Mm]{1,})\W",
	"\W([Hh]e+y{2,})\W",
	"\W([Hh]e{2,}[Yy]+)\W",
	"\W"+anyoftheseregex("[Hh]+[Ee]+[Ll][Ll]+[Oo]+")+"\W",
	"\W([Mm]{2,}[Hh]?)\W",
	"\W((?:[Mm][Hh]){1,})\W",
	"\W([Ss][Oo]{2,})\W",
	"\W([Uu][Hh]+)\W",
	"\W([Uu][Mm]+)\W",
	"\W([Yy][Aa]+[Yy]+)\W",
	"\W([Yy]+[Aa]+[Hh]?)\W"
	]
	excludelist=[]
	
	#dicts to store results
	dicti=defaultdict(float)
	matchesdicti=defaultdict(list)
	results=[]
	
	prosody_list=[re.compile(i) for i in prosodyitems]
	print "{} items in the prosody_list, {} unique".format(len(prosody_list), len(set(prosody_list)))
	print [i.pattern for i in prosody_list]
	#iterate and match
	for dir in [i for i in os.listdir(input_dir) if not i.startswith(".")]:
		print dir
		for fili in [i for i in os.listdir(os.path.join(input_dir, dir)) if not i.startswith(".")]:
			with codecs.open(os.path.join(input_dir, dir, fili), "r", "utf-8") as inputtext:
				inputad=ct.adtextextractor(inputtext.read(), fili).lower()
			#result is a list of lists which contain matches for each regex/acronym
			wordcount=float(len(ct.tokenizer(inputad)))
			result=[([m for m in i.findall(inputad) if not m in excludelist], i.pattern) for i in prosody_list] 
			#print result
			results.append([(len(matches), len(matches)/wordcount) for matches, pattern in result])
			for matches, pattern in result:
				#print pattern
				#the dicti is {pattern:count, pattern: count, ...}
				dicti[pattern]=dicti[pattern]+len(matches)
				matchesdicti[pattern]=matchesdicti[pattern]+matches
	print "\n".join([":".join((i, str(dicti[i]), "|".join(set(matchesdicti[i])))) for i in sorted(dicti, key=dicti.get, reverse=True)])
	end=time.time()
	print "This took us {} minutes".format((end-start)/60)
	# for u in [[x[0] for x in i] for i in results]:
		# print u
	print "shape of results, number of lists:", len(results),  "-- length of lists", set([len(i) for i in results])
	return [[x[0] for x in i] for i in results], [[x[1] for x in i] for i in results] 



###SECTION 3
###WORD LEVEL




###SECTION 4
###UTTERANCE LEVEL

