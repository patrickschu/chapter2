# -*- coding: utf-8 -*-


import codecs
import json
import os
from collections import defaultdict
import clustertools as ct
import re
import nltk

#moving parts

#we copy these items from the word2vecmaker
stopregex=re.compile(r"([\.|\?|\!|\-|,]+)(\w)")


#the script counts the occurence of specific words within certain clusters from word2vec.
#these clusters are contained in /Users/ps22344/Downloads/chapter2/current/clusterskmeans_54_19_10_07_30.json
#we need to look at clusters [50, 6, 22, 39, 24, 48, 1]
#for each cluster, we need a dict that counts occureence of a word in the files in /Users/ps22344/Downloads/craig_0208
#if needed, these should be broken down by category

def folderreader(directory):
	"""
	folderreader takes a directory containing subfolders. 
	then iterates over files contained in the subfolder.
	"""
	output=[]
	directory=os.path.expanduser(directory)
	subfolds=[i for i in os.listdir(directory) if not i.startswith (".")]
	for fold in subfolds:
		filis=[os.path.join(directory, fold, i) for i in os.listdir(os.path.join(directory, fold)) if not i.startswith (".")]
		output=output+filis
		if len(output) != len (set(output)):
			print "Alarm \n --- duplicates in filelist --- \n"
	return (set(output))
	
#folderreader('~/Downloads/craig_0208')

def wordcounter (list_of_clusters):
	with codecs.open('/Users/ps22344/Downloads/chapter2/current/clusterskmeans_54_19_10_07_30.json', 'r', 'utf-8') as jsoninput:
		wordtovecclusters=json.load(jsoninput)
	wordtovecclusters={int(k):v['words'] for k,v in wordtovecclusters.items() if int(k) in list_of_clusters}
	for key in wordtovecclusters:
		wordcount={i:0 for i in wordtovecclusters[key]}
		filis=folderreader('~/Downloads/craig_0208')
		print "we have {} files to work with".format(len(filis))
		for fili in filis:
			with codecs.open(fili, "r", "utf-8") as inputfile:
				inputad=ct.adtextextractor(inputfile.read(), fili)
			addspace=stopregex.sub(r"\g<1> \g<2>", inputad)
			splittext=nltk.word_tokenize(addspace)
			#splittext=[s for s in splittext if s not in exclude]
			splittextlo=[s.lower() for s in splittext if s]
			for w in wordcount.keys():
				wordcount[w]=wordcount[w] + splittextlo.count(w)
		print "\n", key
		print [(k,wordcount[k]) for k in sorted(wordcount, key=wordcount.get, reverse=True)]
	
wordcounter([1,2,3])