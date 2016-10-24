import numpy as np
from string import punctuation
import re
import clustertools as ct
import time
import os
import codecs
from collections import defaultdict
import json 


#dataset
#dir='/Users/ps22344/Downloads/craig_0208/'
#search terms
#search_terms=[r'sling 2']



def tokenfinder(input_list, input_path):
	"""
	the tokenfinder looks over the items in an input_list.
	the regex pattern is ".{,40}ITEM.{,40}".	
	it outputs findings in the corpus given in "dir".
	filename and total number of matches are printed. 
	dir needs to have subfolders. 
	"""
	starttime=time.time()
	print "search term is ", input_list
	#construct the regexes
	typedict={}
	for item in input_list:
		typedict[re.compile(r".{,40}"+unicode(item)+".{,40}")]=0
	for typi in typedict:
		print typi.pattern	
	totalhits=[]
	#iterate over files
	for pati in [i for i in os.listdir(input_path) if not i.startswith(".")]:
		#print pati
		for fil in [i for i in os.listdir(os.path.join(input_path, pati)) if not i.startswith(".")]:
			fili=codecs.open(os.path.join(input_path, pati, fil), "r", "utf-8")
			inputad=ct.adtextextractor(fili.read(), fili)
			inputad=inputad.lower()
			matches=[k.findall(inputad) for k in typedict.keys()]
			if sum([len(i) for i in matches]) > 0:
				print "{} hits in file {}".format(sum([len(i) for i in matches]), os.path.join(input_path, pati, fil))
				print matches, "\n\n"
				totalhits.append(sum([len(i) for i in matches]))
	if sum(totalhits) == 0:
		print "\nNO MATCHES IN TOKENFINDER\n---\n"
	else:
		print "{} matches total".format(sum(totalhits))
	endtime=time.time()
	#print "This took us {} minutes".format((endtime-starttime)/60)	


#tokenfinder(search_terms, dir)






