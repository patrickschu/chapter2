import numpy as np
import codecs
import time
import os
import clustertools as ct

t=np.array([[1,1], [2,2]])


print t, "\n---"

print np.column_stack((t, [[1000,1000,0], [2000,2000,0]]))


def emoticonfinder(dir):
	"""
	The emoticonfinder takes a directory with corpus files as input. 
	We might consider making the file with emoticons an argument as well. 
	The emoticonfinder creates a list of relevant emoticons from a text file. 
	Then counts how often they occur in files in dir.
	--- Source file is /Users/ps22344/Downloads/chapter2/current/emoticoncounter.py ---
	"""
	starttime=time.time()
	#creating a featuredict from file
	featuredict={}
	with codecs.open('/home/ps22344/Downloads/chapter2/textfiles/emolist_final.txt', "r", "utf-8") as inputtext:
		for line in inputtext.readlines():
			featuredict[line.rstrip("\n")]=0
	#test formatting
	for k in featuredict:
		if k.startswith(" "):
			print k, "starts with whitespace"
	for pati in [i for i in os.listdir(dir) if not i.startswith(".")]:
		print pati
		for fili in [i for i in os.listdir(os.path.join(dir, pati)) if not i.startswith(".")]:
			fili=codecs.open(os.path.join(dir, pati, fili), "r", "utf-8")
			inputad=ct.adtextextractor(fili.read(), fili)
			words=ct.tokenizer(inputad)
			for item in words:
				if item in featuredict:
					featuredict[item] = featuredict[item]+1
	print featuredict
	endtime=time.time()
	print "This took us {} minutes".format((endtime-starttime)/60)

emoticonfinder ("/home/ps22344/Downloads/craig_0208")
