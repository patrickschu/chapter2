import clustertools as ct
import tokenfinder_1004 as tk
import re
import codecs
from collections import defaultdict
import os

abbreviations=["LTR"]


capsdict={
#re.compile("(\W+[A-Z]{3,})\W+"):"all caps",
#re.compile("\W+([a-z]+[A-Z]+(?:[a-z]+)?(?:[A-Z]+)?)\W"):"PascalCase",
re.compile("\W+([A-Z]+[a-z]+[A-Z]+(?:[a-z]+)?)\W"):"CamelCase",


}

print {i.pattern for i,v in capsdict.items()}

def capsfinder(input_dir, input_dict):
	results=[]
	#dicti is results by word/item
	dicti=defaultdict(float)
	#matchesdicti is results by Regexpattern
	matchesdicti=defaultdict(list)
	search_terms=[i for i in input_dict.keys()]
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
			if len(result) > 1:
				print "result", len(result), result
			#this is the count we returs
			results.append([len(matches) for matches, pattern in result])
			#here we inspect findings. note resultS vs result
			for matches, pattern in result:
				if len(matches) > 100:
					print "matches", len(matches), os.path.join(input_dir, dir, fili)
					#the dicti is {pattern:count, pattern: count, ...}
				for res in matches:
					dicti[res]=dicti[res]+1
					#print len(matches[0]), 'total', len(matches)
					#matchesdicti collects the matches per regex, dicti per feature
					matchesdicti[pattern]=matchesdicti[pattern]+matches
	print "\n".join([":".join((i, str(dicti[i]), "|".join(set(matchesdicti[i])))) for i in sorted(dicti, key=dicti.get, reverse=True)])	
	# for entry in {k:v for k,v in matchesdicti.items()}:
# 		print "\n", entry, matchesdicti[entry]
# 	for entry in dicti:
# 		print entry, dicti[entry]
	return results 


capsfinder("/Users/ps22344/Downloads/craig_0208", capsdict)