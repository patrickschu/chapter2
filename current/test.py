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



def acronymcounter(input_dir):
	"""
	The acronymcounter counts acronyms and abbreviations. 
	It relies on a&a previously IDd in the acronymfinder. 
	Here, we make that list out of the shorteningdict jsons created earlier. 
	The regex is designed to find lowercase and uppercase versions of each, plus plurals.
	The input_dir contains the text files to be iterated over. 
	Returns a list of lists where each list contains raw and per word counts.
	This is based on chapter2/current/acronymcounter_1115.py.
	NOTE:we can consider running location and schools over a different regex that does not include plural s.
	"""
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

	print search_terms
			
	print "we have {} search terms".format(len(search_terms))
		
	excludelist=set(["oks", "fbs", "PSS", "VAS", "vas", "BCS", "bcs", "NES", "nes", "SMS", "sms", "SAS", "SSS", "sss", "nsas", "mias"])
	
	#dicts to store results
	dicti=defaultdict(float)
	matchesdicti=defaultdict(list)
	results=[]
	
	#regex, lower and pluralize
	acronym_list=[re.compile("\W((?:"+i+"|"+i.lower()+")[sS]?)\W") for i in search_terms]
	acronym_list=set(acronym_list)
	print [i.pattern for i in acronym_list]
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
	

	
ff=np.array([[0],[1],[2],[0]])	
pp=np.array([[0],[1],[200],[100]])
gg=np.array([[0],[1],[2],[1000.5]])
print gg.shape

res=np.column_stack([ff,pp, gg])
print res
print res.shape
print res.sum(axis=1)
t=np.column_stack([res,res.sum(axis=1)])
print t
print res.shape
print res.shape[0]

	

#x=acronymcounter("/home/ps22344/Downloads/craig_0208")
 

def clippingcounter(input_dir):
	"""
	The clipping uses the clipping_list to count instances	of the clippings listed in there. 
	Here, we make that list out of the shorteningdict jsons created earlier. 
	The regex is designed to find lowercase and uppercase versions of each, plus plurals.
	The input_dir contains the text files to be iterated over. 
	Returns a list of lists where each list contains raw and per word counts.
	"""
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

	#for i in search_terms:
	#	print i, search_terms.count(i)
			
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
		for fili in [i for i in os.listdir(os.path.join(input_dir, dir)) if not i.startswith(".")][:5]:
			with codecs.open(os.path.join(input_dir, dir, fili), "r", "utf-8") as inputtext:
				inputad=ct.adtextextractor(inputtext.read(), fili).lower()
			#result is a list of lists which contain matches for each regex/acronym
			wordcount=float(len(ct.tokenizer(inputad)))
			result=[([m for m in i.findall(inputad) if not m in excludelist], i.pattern) for i in clipping_list] 
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

#clippingcounter("/home/ps22344/Downloads/craig_0208")

def charactercounter(input_dir):
	"""
	Finds individual characters representing an entire word.
	Example: C U for see you. 
	Based on charactercounter_1129.py.
	Returns a list of lists where each list contains raw and per word counts.
	"""
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
	print "search terms",  [i.pattern for i in search_terms]
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

#charactercounter("/home/ps22344/Downloads/craig_0208")

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
	start=time.time()
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
	print "\n".join([":".join((i, str(dicti[i]))) for i in sorted(dicti, key=dicti.get, reverse=True) if dicti[i] > 100])	
	#for entry in {k:v for k,v in matchesdicti.items()}:
 	#	print "\n", entry, set([i for i in matchesdicti[entry] if #matchesdicti[entry].count(i) > 50])
	print "shape of results, number of lists:", len(results),  "-- length of lists", set([len(i) for i in results])
	end=time.time()
	print "This took us {} minutes".format((end-start)/60)
	return [[x[0] for x in i] for i in results], [[x[1] for x in i] for i in results] 


#capsfinder("/home/ps22344/Downloads/craig_0208", 0.5)
















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
	

