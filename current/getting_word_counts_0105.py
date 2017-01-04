import os
import codecs
import clustertools as ct
import json

dir = "/home/ps22344/Downloads/craig_0208"

categorydict, catnumber = ct.categorymachine(dir, "category1")

print categorydict

def wordcounter(input_dir, category_tag, category_dict):
	"""
	counts the words per category in the files in input_dir.
	
	Parameters
	----------
	input_dir is the corpus directoty
	category_tag is the name of the tag to be extracted with tagextractor. 
	category_dict is a dictionary of categories to be computed over (category names as keys)
	e.g. <location="X"> would be input with "location" as the category_tag and a dict with {"Austin":0, "Dallas":0, ...}
	Returns
	-------
	something
	"""
	print "Running the wordcounter"
	resultdict=category_dict
	for pati in [i for i in os.listdir(input_dir) if not i.startswith(".")]:
		print pati
		for fili in [i for i in os.listdir(os.path.join(input_dir, pati)) if not i.startswith(".")]:
			with codecs.open(os.path.join(input_dir, pati, fili), "r", "utf-8") as inputfili:
				inputfili= inputfili.read()
			wordcount= len(ct.tokenizer(ct.adtextextractor(inputfili, fili), remove_punctuation=True))
			category= ct.tagextractor(inputfili, category_tag, fili)
			if category in resultdict:
				resultdict[category]= resultdict[category]+wordcount
			else:
				print "\n\nWARNING:\n{} is not in the category_dict. What do we do now?\n\n".format(category)
	print "Wordcounter done"

	with codecs.open("wordcounter_"+category_tag+".json", "w", "utf-8") as jsonout:
		json.dump(resultdict, jsonout)

		
wordcounter(dir, "category1", categorydict)	
	
	
