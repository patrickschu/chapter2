
import numpy as np
import os
import json
import codecs
import re
import clustertools as ct
from collections import defaultdict


filelist=[
"/Users/ps22344/Downloads/chapter2/current/shorteningdict_2_1115.json",
"/Users/ps22344/Downloads/chapter2/current/shorteningdict_3_1115.json",
"/Users/ps22344/Downloads/chapter2/current/shorteningdict_4_1115.json",
"/Users/ps22344/Downloads/chapter2/current/shorteningdict_5_1115.json",
"/Users/ps22344/Downloads/chapter2/current/shorteningdict_6_1115.json"
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


#for key in acronym_dict


def acronymcounter(acronym_list, input_dir):
		"""
		The acronymcounter uses the acronym_list to count instances	of the abbreviations listed in there. 
		Here, we make that list out of the shorteningdict jsons created earlier. 
		The regex is designed to find lowercase and uppercase versions of each, plus plurals.
		The input_dir contains the text files to be iterated over. 
		It returns a list of match counts.
		e.g.
		acronym_list=['LOL', 'ROFL', 'ASL', 'BRB']
		result=[0,0,2,0] 
		NOTE:we can consider running location and schools over a different regex that does not include plural s.
		"""
		excludelist=set(["oks", "fbs", "PSS", "VAS", "vas", "BCS", "bcs", "NES", "nes", "SMS", "sms", "SAS", "SSS", "sss", "nsas", "mias"])
		
		#dicts to store results
		dicti=defaultdict(float)
		matchesdicti=defaultdict(list)
		results=[]
		
		#regex, lower and pluralize
		acronym_list=[re.compile("\W((?:"+i+"|"+i.lower()+")[sS]?)\W") for i in acronym_list]
		acronym_list=set(acronym_list)
		print [i.pattern for i in acronym_list]
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
		return results 
# 					
# 					print result
		print "\n".join([":".join((i, str(dicti[i]), "|".join(set(matchesdicti[i])))) for i in sorted(dicti, key=dicti.get, reverse=True)])	


x=acronymcounter(search_terms, "/Users/ps22344/Downloads/craig_0208")
print x
		

	
