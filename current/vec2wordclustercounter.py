#counting clusters
import os
import re
import json
import codecs
from collections import defaultdict
import clustertools as ct
from nltk import word_tokenize
from string import punctuation
import time

pathi=os.path.expanduser(os.path.join("~/", "Downloads", "craigbalanced_0601"))
punctuationregex=re.compile("(["+"|\\".join(list(punctuation))+"|\d+]+)")
chapterdir=os.path.split(os.getcwd())

folders=[i for i in os.listdir(pathi) if not i.startswith(".")]
print folders

#go thru text: we get a list of items

#instead of counting word, add to cluster it occurs in



def vec2wordclustercounter(folderlist, cluster_dictionary):
	"""
	This is stolen from the cluster_analysis dictmaker. 
	The dictmaker counts the words / items contained in the files found in the folders of folderlist.
	remove_stopwords uses the stopword list defined above to ignore words. 
	remove_punct works with string.punctuation, cf above. 
	This was mainly used to test how well the counting in the word2vec analysis works.
	"""
	with codecs.open(cluster_dictionary, "r", "utf-8") as inputjson:
		clusterdict=json.load(inputjson)
	result=defaultdict(int)
	#this is just for qc
	misses=[]
	for folder in folderlist:
		filis=[i for i in os.listdir(os.path.join(pathi,folder)) if not i.startswith(".")]
		print "Building vocab: we have {} files in folder {}".format(len(filis), folder)
		for fili in filis:
			inputfile=codecs.open(os.path.join(pathi, folder, fili), "r", "utf-8").read()
			inputtext=ct.adtextextractor(inputfile, fili)
			#pre-processing here
			inputtext=ct.adcleaner(inputtext ,replace_linebreak=True, remove_html=False)
			splittext=word_tokenize(inputtext)
			splittextlo=[i.lower() for i in splittext]	
			finaltext=[punctuationregex.sub("",i) for i in splittextlo]
			finaltext=[i for i in finaltext if i and i not in ['br']]	
			#do we want to lemmatize or things like that
			for word in finaltext:
				cluster= [k for k,v in clusterdict.items() if word in v['words']]
				if len(cluster) > 1:
					print "Warning: The item {} was found in more than one clusters".format(word)
				if len(cluster) < 1:
					#print "Warning: The item could not be found in a cluster"
					misses.append(word)
				else:
					result[cluster[0]]=result[cluster[0]]+1
	print "Our vocab dictionary has {} entries".format(len(result))
	ct.dictwriter(os.path.join("~/", chapterdir[0], "outputfiles", "fulldict_"+time.strftime("%H_%M_%m_%d")), result)
# 	featuredict= {key:value for key, value in vocab.items() if value > float(threshold) }
# 	print "Our feature dictionary has {} entries\n---------------\n".format(len(featuredict))
# 	print "This is our featuredict", featuredict
# 	ct.dictwriter(os.path.join("~/", chapterdir[0], "outputfiles", "featuredict_"+time.strftime("%H_%M_%m_%d")), featuredict)
	print "misses", len(misses), set(misses)
	print result
	return result

	
vec2wordclustercounter(folders, '/Users/ps22344/Downloads/chapter2/current/clusters_54_19_45_07_30.json')