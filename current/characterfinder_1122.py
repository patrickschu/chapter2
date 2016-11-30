import codecs
import re
import json
import string
import os 
import clustertools as ct
import tokenfinder_1004 as tk
from collections import defaultdict


print string.ascii_letters

# iding letters for words
# what comes to mind? c = see, u = you, 
#in herring this is the same as numbers
# or find one letter words in corpus


# with codecs.open("/Users/ps22344/Downloads/chapter2/current/typodict_20160926.json", "r", "utf-8") as jsonin:
# 	typodict=json.load(jsonin)
# 	
# print "len of typodict", len(typodict)

	
	
#u2 uR ub UC ru  2b c ya

alphabet = {k:0 for k in [i for i in list(string.ascii_letters) if not i in [
"D", "d", "F", "f", "G", "J", "Q", "q", "P", "p",  "I", "i", "M", "m", "O", "o", "L", "l", "g", "j", "V", "v", "s", "S", "t", "h", "H", "K", "k", "A", "a", "E", "e", "Z", "z"
]]}
# print "these are our search terms", alphabet
excludelist=[]


def characterfinder(input_dir, input_dict):
	results=[]
	dicti=defaultdict(float)
	matchesdicti=defaultdict(list)
	for entry in input_dict:
		print entry
	characterlist=set([re.compile(" "+i+" ") for i in input_dict.keys()])
	print [i.pattern for i in characterlist]
	for dir in [i for i in os.listdir(input_dir) if not i.startswith(".")]:
		print dir
		for fili in [i for i in os.listdir(os.path.join(input_dir, dir)) if not i.startswith(".")]:
			with codecs.open(os.path.join(input_dir, dir, fili), "r", "utf-8") as inputtext:
				inputad=ct.adtextextractor(inputtext.read(), fili)
			#result is a list of lists which contain matches for each regex/acronym
			result=[([m for m in i.findall(inputad) if not m in excludelist], i.pattern) for i in characterlist] 
			results.append([len(matches) for matches, pattern in result])
			for matches, pattern in result:
				#the dicti is {pattern:count, pattern: count, ...}
				dicti[pattern]=dicti[pattern]+len(matches)
				matchesdicti[pattern]=matchesdicti[pattern]+matches
	print "\n".join([":".join((i, str(dicti[i]), "|".join(set(matchesdicti[i])))) for i in sorted(dicti, key=dicti.get, reverse=True)])	
	for entry in {k:v for k,v in matchesdicti.items() if v > 10}:
		print entry
		tk.tokenfinder([re.sub("[\(\)]", "", entry)], "/Users/ps22344/Downloads/craig_0208", lower_case=False)
	return results 
		
characterfinder( "/Users/ps22344/Downloads/craig_0208", {'c':0})

######
#helper funcs
def capitalizer(input_list):
	"""
	returns a list with inputword|inputword.upper() to feed into regex
	"""
	return [i.upper()+"|"+i for i in input_list]


xpostwords=["army", "navy", "wife", "husband", "gf", "girlfriends?", "drug", "baggage", "drama", "user", "boy", "of low", "anything", " hockey", "slaves", "relationship"]
xprewords=["[Mm]y", "[Ii]'m", "[Yy]our"]


counterdict={
"xX":["(?:"+"|".join(capitalizer(xprewords))+")\W+([Xx])\W+" , "\W+([Xx])\W+(?:"+"|".join(capitalizer(xpostwords))+")"]
}


def charactercounter(input_dir, input_dict):
	results=[]
	dicti=defaultdict(float)
	matchesdicti=defaultdict(list)
	#search_terms=set([t for i in input_dict.values() for t in i])
	search_terms=[re.compile("|".join(i)) for i in input_dict.values()]
	print "search terms",  [i.pattern for i in search_terms]
	for dir in [i for i in os.listdir(input_dir) if not i.startswith(".")]:
		print dir
		for fili in [i for i in os.listdir(os.path.join(input_dir, dir)) if not i.startswith(".")]:
			with codecs.open(os.path.join(input_dir, dir, fili), "r", "utf-8") as inputtext:
				inputad=ct.adtextextractor(inputtext.read(), fili)
			#result is a list of lists which contain matches for each regex/acronym
			#the list incomprehension just deletes empty search results from the "|" search
			result=[([t for m in i.findall(inputad) for t in m if t], i.pattern) for i in search_terms] 
			#print result
			results.append([len(matches) for matches, pattern in result])
			for matches, pattern in result:
				if len(matches) > 1:
					print "multiple matches", matches, os.path.join(input_dir, dir, fili)
				if len(matches) > 0:
					print len(matches)
					#the dicti is {pattern:count, pattern: count, ...}
					for res in matches[0]:
						dicti[res]=dicti[res]+1
					#print len(matches[0]), 'total', len(matches)
					#print inputad[inputad.index(matches[0])-20:inputad.index(matches[0])+20]
					#matchesdicti collects the matches per regex, dicti per feature
						matchesdicti[pattern]=matchesdicti[pattern]+matches
	#print "\n".join([":".join((i, str(dicti[i]), "|".join(set(matchesdicti[i])))) for i in sorted(dicti, key=dicti.get, reverse=True)])	
	for entry in {k:v for k,v in matchesdicti.items()}:
		print "\n", entry, matchesdicti[entry]
	for entry in dicti:
		print entry, dicti[entry]
	#	tk.tokenfinder([re.sub("[\(\)]", "", entry)], "/Users/ps22344/Downloads/craig_0208", lower_case=False)
	return results 


#charactercounter("/Users/ps22344/Downloads/craig_0208", counterdict)
