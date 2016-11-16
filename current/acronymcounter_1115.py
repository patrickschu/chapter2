
import numpy as np
import os
import json
import codecs
import re
import clustertools as ct
from collections import defaultdict


filelist=[
#"/Users/ps22344/Downloads/chapter2/current/shorteningdict_2_1115.json",
"/Users/ps22344/Downloads/chapter2/current/shorteningdict_3_1115.json",
#"/Users/ps22344/Downloads/chapter2/current/shorteningdict_4_1115.json",
#"/Users/ps22344/Downloads/chapter2/current/shorteningdict_5_1115.json",
"/Users/ps22344/Downloads/chapter2/current/shorteningdict_6_1115.json"
]

search_terms = ["MILF"]

for fili in filelist:
	with codecs.open(fili, "r", "utf-8") as inputfile:
		acronym_dict=json.load(inputfile)
		for key in [i for i in acronym_dict.keys() if i not in ["blend", "abbreviation", "clipping", "delete", "other"]]:
			for cat in ['X', 'location', 'other']:
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
		"""
		dicti=defaultdict(float)
		#regex, lower and pluralize
		acronym_list=[re.compile("\W((?:"+i+"|"+i.lower()+")[sS]?)\W") for i in acronym_list]
		acronym_list=set(acronym_list)
		print [i.pattern for i in acronym_list]
		for dir in [i for i in os.listdir(input_dir) if not i.startswith(".")]:
			print dir
			for fili in [i for i in os.listdir(os.path.join(input_dir, dir)) if not i.startswith(".")]:
				#print os.path.join(input_dir, dir, fili)
				with codecs.open(os.path.join(input_dir, dir, fili), "r", "utf-8") as inputtext:
					inputad=ct.adtextextractor(inputtext.read(), fili)
				result=[i.findall(inputad) for i in acronym_list] 
				result= [(i, len(i)) for i in result if len(i) > 0] 
				if result:
					for res in result:
						dicti[res]=dicti[res]+len(res)
					print result
		print dicti			


acronymcounter(search_terms, "/Users/ps22344/Downloads/craig_0208")
		
	
	
