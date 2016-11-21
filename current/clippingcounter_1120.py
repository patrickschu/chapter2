#this is based on the acronymcounter. 
# files have been exchanged
# - check out all variatns
#  -- exclude some contexts cf notes
#  - investigate plurals
#  - remove duplicates 

import numpy as np
import os
import json
import codecs
import re
import clustertools as ct
from collections import defaultdict


filelist=[

'/Users/ps22344/Downloads/chapter2/current/clippingdict_catsfinal_yes_2chars_1121.json',
'/Users/ps22344/Downloads/chapter2/current/clippingdict_catsfinal_yes_5chars_1121.json',
'/Users/ps22344/Downloads/chapter2/current/clippingdict_catsfinal_yes_4chars_1121.json',
'/Users/ps22344/Downloads/chapter2/current/clippingdict_catsfinal_post_4chars_1121.json',
'/Users/ps22344/Downloads/chapter2/current/clippingdict_catsfinal_yes_3chars_1121.json',
'/Users/ps22344/Downloads/chapter2/current/clippingdict_catsfinal_post_3chars_1121.json',
'/Users/ps22344/Downloads/chapter2/current/clippingdict_catsfinal_yes_7chars_1121.json',
'/Users/ps22344/Downloads/chapter2/current/clippingdict_catsfinal_yes_6chars_1121.json',
'/Users/ps22344/Downloads/chapter2/current/clippingdict_catsfinal_post_6chars_1121.json',
'/Users/ps22344/Downloads/chapter2/current/clippingdict_catsfinal_post_5chars_1121.json'
]

search_terms = []


for fili in filelist:
	with codecs.open(fili, "r", "utf-8") as inputfile:
		acronym_dict=json.load(inputfile)
		for key in [i for i in acronym_dict.keys() if i not in ["delete", "other"]]:
			for cat in ['X', 'noun', ]:
				print "adding", acronym_dict[key][cat]
				search_terms = search_terms + acronym_dict[key][cat]

print search_terms

for i in search_terms:
	print i
			
		
print "we have {} search terms".format(len(search_terms))




def clippingcounter(clipping_list, input_dir):
		"""
		The clipping uses the clipping_list to count instances	of the clippings listed in there. 
		Here, we make that list out of the shorteningdict jsons created earlier. 
		The regex is designed to find lowercase and uppercase versions of each, plus plurals.
		The input_dir contains the text files to be iterated over. 
		It returns a list of match counts.
		e.g.
		clipping_list=['LOL', 'ROFL', 'ASL', 'BRB']
		result=[0,0,2,0] 
		"""
		excludelist=set(["oks", "fbs", "PSS", "VAS", "vas", "BCS", "bcs", "NES", "nes", "SMS", "sms", "SAS", "SSS", "sss", "nsas", "mias"])
		
		#dicts to store results
		dicti=defaultdict(float)
		matchesdicti=defaultdict(list)
		results=[]
		
		#regex, lower and pluralize
		for i in clipping_list:
			print i, "\n"
		clipping_list=[re.compile("\W((?:"+i+"|"+i.lower()+")[sS]?)\W") for i in clipping_list]
		clipping_list=set(clipping_list)
		print [i.pattern for i in clipping_list]
		#iterate and match
		for dir in [i for i in os.listdir(input_dir) if not i.startswith(".")]:
			print dir
			for fili in [i for i in os.listdir(os.path.join(input_dir, dir)) if not i.startswith(".")][:100]:
				with codecs.open(os.path.join(input_dir, dir, fili), "r", "utf-8") as inputtext:
					inputad=ct.adtextextractor(inputtext.read(), fili)
				#result is a list of lists which contain matches for each regex/acronym
				result=[([m for m in i.findall(inputad) if not m in excludelist], i.pattern) for i in acronym_list] 
				results.append([len(matches) for matches, pattern in result])
				for matches, pattern in result:
 					#the dicti is {pattern:count, pattern: count, ...}
 					dicti[pattern]=dicti[pattern]+len(matches)
 					matchesdicti[pattern]=matchesdicti[pattern]+matches
		print "\n".join([":".join((i, str(dicti[i]), "|".join(set(matchesdicti[i])))) for i in sorted(dicti, key=dicti.get, reverse=True)])	
		return results 


#x=clippingcounter(search_terms, "/Users/ps22344/Downloads/craig_0208")