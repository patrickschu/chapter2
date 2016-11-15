
import numpy as np
import os
import json
import codecs

filelist=[
#"/Users/ps22344/Downloads/chapter2/current/shorteningdict_2_1115.json",
#"/Users/ps22344/Downloads/chapter2/current/shorteningdict_3_1115.json",
#"/Users/ps22344/Downloads/chapter2/current/shorteningdict_4_1115.json",
#"/Users/ps22344/Downloads/chapter2/current/shorteningdict_5_1115.json",
"/Users/ps22344/Downloads/chapter2/current/shorteningdict_6_1115.json"
]

search_terms = []

for fili in filelist:
	with codecs.open(fili, "r", "utf-8") as inputfile:
		acronym_dict=json.load(inputfile)
		for key in [i for i in acronym_dict.keys() if i not in ["blend", "abbreviation", "clipping", "delete"]]:
			for cat in ['X', 'location']:
				print "adding", acronym_dict[key][cat]
				search_terms = search_terms + acronym_dict[key][cat]

print search_terms
			
		
print "we have {} search terms".format(len(search_terms))


#for key in acronym_dict


def acronymcounter(acronym_list, input_dir):
		acronym_list=set(acronym_list)
		for fili in [i for i in os.listdir(input_dir) if not i.startswith(".")]:
			#lower and pluralize
			[text.count(i) for i in acronym_list] 
			


acronymcounter(search_terms, "/Users/ps22344/Downloads/craig_0208")
		
	
	
