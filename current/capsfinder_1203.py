import clustertools as ct
import tokenfinder_1004 as tk
import re
import codecs
from collections import defaultdict
import os

abbreviations=["LTR"]


capsdict={
re.compile("([A-Z]{3,})"):0
}

print {i.pattern for i,v in capsdict.items()}

def capsfinder(input_dir, input_dict):
	results=[]
	dicti=defaultdict(float)
	matchesdicti=defaultdict(list)
	search_terms=[i for i in input_dict.keys()]
	print "search terms",  [i.pattern for i in search_terms]
	for dir in [i for i in os.listdir(input_dir) if not i.startswith(".")]:
		print dir
		for fili in [i for i in os.listdir(os.path.join(input_dir, dir)) if not i.startswith(".")]:
			with codecs.open(os.path.join(input_dir, dir, fili), "r", "utf-8") as inputtext:
				inputad=ct.adtextextractor(inputtext.read(), fili)
			#we exclude anything we have in our abbreviations dict
			result=[([t for t in i.findall(inputad) if not t in abbreviations], i.pattern) for i in search_terms] 
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
	for entry in {k:v for k,v in matchesdicti.items()}:
		print "\n", entry, matchesdicti[entry]
	for entry in dicti:
		print entry, dicti[entry]
	for entry in matchesdicti:
		tk.tokenfinder(["(.{,20})(?<![A-Z] [A-Z]|Ave| MA)\s+(N)\s+(?!Houston|Ballard|word|Royaton|Wilmot|Tucson|Dallas|Warren|side|Avalon|St Pete|Scottsdale|Tampa|C[Oo][Uu][Nn][Tt][Yy]|[Rr][Oo][Ll][Ll]|Arl\.|Royaltown|Golden Isles|Oeleans|Ballard Rd|Broward|Ward|angola|Oracle|[Hubert|1st] Ave|European|Tryon|Hill\w+ |Wil\w+|[Ss][Uu][Bb][Jj][Ee][Cc][Tt]|state line|for now|with a dick|OT |of (\s+Dayton|Talla\w+)|THE INSIDE|THE SURROUNDING|TIME|AUGHTY|[A-Z] [A-Z] |&amp; 5th)(.{,20})"], "/Users/ps22344/Downloads/craig_0208", length= 50, lower_case=False)
	return results 


capsfinder("/Users/ps22344/Downloads/craig_0208", capsdict)