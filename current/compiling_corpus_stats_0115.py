import os
import codecs
import clustertools as ct
from collections import defaultdict
import time
import json

timestamp = time.strftime("%Y%m%d-%H%M%S")

"""Compiling corpus stats"""

input_dir="/Users/ps22344/Downloads/craig_0208/plat"


def wordcounter(input_dir, tag, output_json=False):
	"""
	count words 
	"""
	catdicti=defaultdict(float)
	worddicti=defaultdict(float)
	for dir in [i for i in os.listdir(input_dir) if not i.startswith(".")]:
		print dir
		for fili in [i for i in os.listdir(os.path.join(input_dir, dir)) if not i.startswith(".")]:
			inputad=ct.Ad(os.path.join(input_dir, dir, fili))
			catdicti[inputad.meta[tag]]=catdicti[inputad.meta[tag]]+1
			worddicti[inputad.meta[tag]]=worddicti[inputad.meta[tag]]+inputad.wordcount
	if output_json:
		with codecs.open(tag+"_categorydict_plat"+timestamp+".txt", "w", "utf-8") as categoryout:
			json.dump(catdicti, categoryout)
		with codecs.open(tag+"_wordcountdict_plat"+timestamp+".txt", "w", "utf-8") as wordout:
			json.dump(worddicti, wordout)
	for dict in [worddicti, catdicti]:
		sorteddict=sorted(dict, key=lambda x:dict[x], reverse=True)
		print "\n".join([",".join([i, unicode(dict[i])]) for i in sorteddict])
		print "\ntotal count", sum([v for k,v in dict.items()])
	
			
			
		
wordcounter(input_dir, "category1", output_json=True)


def dictprinter(file_name):
	"""
	put in json, get out csv print
	"""
	with codecs.open(file_name, "r", "utf-8") as inputjson:
		dict=json.load(inputjson)
	sorteddict=sorted(dict, key=lambda x:dict[x], reverse=True)
	print "\n".join([",".join([i, unicode(dict[i])]) for i in sorteddict])
	print "\ntotal count", sum([v for k,v in dict.items()])
	
#dictprinter('categorydict20170116-124503.txt')