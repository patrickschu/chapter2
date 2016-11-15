
import numpy as np
import os
import json
import codecs
import re
import clustertools as ct

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
			for cat in ['X', 'location']:
				print "adding", acronym_dict[key][cat]
				search_terms = search_terms + acronym_dict[key][cat]

print search_terms
			
		
print "we have {} search terms".format(len(search_terms))


#for key in acronym_dict


def acronymcounter(acronym_list, input_dir):
		#regex, lower and pluralize
		acronym_list=[re.compile("((?:"+i+"|"+i.lower()+")[sS]?)") for i in acronym_list]
		acronym_list=set(acronym_list)
		print [i.pattern for i in acronym_list]
		for dir in [i for i in os.listdir(input_dir) if not i.startswith(".")]:
			print dir
			for fili in [i for i in os.listdir(os.path.join(input_dir, dir)) if not i.startswith(".")]:
				#print os.path.join(input_dir, dir, fili)
				with codecs.open(os.path.join(input_dir, dir, fili), "r", "utf-8") as inputtext:
					inputad=ct.adtextextractor(inputtext.read(), fili)
				result=[i.findall(inputad) for i in acronym_list] 
				result= [(i, len(i)) for i in result if len(i) > 1] 
				if result:
					print result
					


acronymcounter(search_terms, "/Users/ps22344/Downloads/craig_0208")
		
	
	
