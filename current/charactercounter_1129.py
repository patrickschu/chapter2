import codecs
import re
import os
from collections import defaultdict
import clustertools as ct
import tokenfinder_1004 as tk

######
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
#"xX":["(?:"+"|".join(capitalizer(xprewords))+")\W+([Xx])\W+" , "\W+([Xx])\W+(?:"+"|".join(capitalizer(xpostwords))+")"]
#"cC":["(?:"+"|".join(cprewords)+")\s+([Cc])\s+" , "\s+([Cc])\s+(?:"+"|".join(cpostwords)+")"]
#"u":["\s+(u)\s+"],
#"U":["\s+(U)\s+"+"".join(upostwords)]
#"r":["(?<!(e|g|t))\s+(r)\s+(?!and b |\&amp;)"]
#"R":["(?<!rated|Cocks| [Tt]oys|Girls|[A-Z] [A-Z] [A-Z])\s+(R)\s+(?![A-Z] [A-Z]|R |B |AND [R|B]|&amp;)"]
#"b":["(?<! size|r and)\s+(b)\s+(?!day |cups?|tits|e |or larger)"]
#"B": ["(?<![A|R] AND| Part|. F W|&amp;)\s+(B)\s+(?!cups?|tits|level|average|horror|rated|movie|in the world|S |Q |and W |B? ?W)"]
"N": ["(?<![A-Z] [A-Z]|Ave) N (?!Houston|Wilmot|Tucson|Dallas|Warren|side|Avalon|St Pete|Scottsdale|Tampa|C[Oo][Uu][Nn][Tt][Yy]|Arl\.|Royaltown|Golden Isles|Oeleans|Ballard Rd|Broward|Ward|angola|Oracle|Hubert Ave|European|Tryon|Hill\w+ |Wil\w+ |[Ss][Uu][Bb][Jj][Ee][Cc][Tt]|state line|for now|of Dayton| AUGHTY|[A-Z] [A-Z] )"]
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
				if len(matches) > 0:
					print "multiple matches", matches, os.path.join(input_dir, dir, fili)
				if len(matches) > 0:
					#print len(matches)
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
	for entry in matchesdicti:
		tk.tokenfinder(["(.{,20})(?<![A|R] AND| Part|. F W|&amp;)\s+(B)\s+(?!cups?|tits|level|average|horror|rated|movie|in the world|S |Q |and W |B? ?W)"], "/Users/ps22344/Downloads/craig_0208", length= 50, lower_case=False)
	return results 


charactercounter("/Users/ps22344/Downloads/craig_0208", counterdict)