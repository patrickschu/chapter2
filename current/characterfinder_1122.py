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

alphabet = {k:0 for k in list(string.ascii_letters)}
print alphabet
excludelist=[]


def characterfinder(input_dir, input_dict):
	results=[]
	dicti=defaultdict(float)
	matchesdicti=defaultdict(list)
	for entry in input_dict:
		print entry
	characterlist=set([re.compile("\W"+i+"\W") for i in input_dict.keys()])
	print [i.pattern for i in characterlist]
	for dir in [i for i in os.listdir(input_dir) if not i.startswith(".")]:
		print dir
		for fili in [i for i in os.listdir(os.path.join(input_dir, dir)) if not i.startswith(".")]:
			with codecs.open(os.path.join(input_dir, dir, fili), "r", "utf-8") as inputtext:
				inputad=ct.adtextextractor(inputtext.read(), fili).lower()
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
		tk.tokenfinder([re.sub("[\(\)]", "", entry)], "/Users/ps22344/Downloads/craig_0208")
	return results 
		
characterfinder( "/Users/ps22344/Downloads/craig_0208", alphabet)
