import numpy as np
from string import punctuation
import re
import clustertools as ct
import time
import os
import codecs
from collections import defaultdict
import json 


def tokenfinder(input_list, input_path, length=40, lower_case=True):
	"""
	the tokenfinder looks over the items in an input_list.
	the regex pattern is ".{,40}ITEM.{,40}".	
	it outputs findings in the corpus given in "dir".
	filename and total number of matches are printed. 
	dir needs to have subfolders. 
	"""
	starttime=time.time()
	allhits=[]
	print "search term is ", input_list
	#construct the regexes
	typedict={}
	for item in input_list:
		typedict[re.compile(r".{,"+str(length)+"}"+unicode(item)+".{,"+str(length)+"}")]=0
	for typi in typedict:
		print "***", typi.pattern	
	totalhits=[]
	#iterate over files
	for pati in [i for i in os.listdir(input_path) if not i.startswith(".")]:
		#print pati
		for fil in [i for i in os.listdir(os.path.join(input_path, pati)) if not i.startswith(".")]:
			fili=codecs.open(os.path.join(input_path, pati, fil), "r", "utf-8")
			inputad=ct.adtextextractor(fili.read(), fili)
			if lower_case:
				#print "were lowercasing"
				inputad=inputad.lower()
			matches=[k.findall(inputad) for k in typedict.keys()]
			if sum([len(i) for i in matches]) > 0:
				print "{} hits in file {}".format(sum([len(i) for i in matches]), os.path.join(input_path, pati, fil))
				print matches, "\n"
				totalhits.append(sum([len(i) for i in matches]))
				allhits.append(matches)
	if sum(totalhits) == 0:
		print "\n---\nNO MATCHES IN TOKENFINDER\n---\n"
	else:
		print "{} matches total".format(sum(totalhits))
	endtime=time.time()
	return allhits
	#print "This took us {} minutes".format((endtime-starttime)/60)	








