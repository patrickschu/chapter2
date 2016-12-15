import numpy as np
import codecs
import time
import os
import clustertools as ct
import re

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
	search_terms=[]
	with codecs.open('/home/ps22344/Downloads/chapter2/textfiles/emolist_final_2.txt', "r", "utf-8") as inputtext:
		for line in inputtext.readlines():
			print line.rstrip("\n")
			#featuredict[re.compile(" ("+re.escape(line.rstrip("\n"))+")")]=0
			search_terms.append(re.compile(" ("+re.escape(line.rstrip("\n"))+")"))
		
	for pati in [i for i in os.listdir(dir) if not i.startswith(".")]:
		print pati
		for fili in [i for i in os.listdir(os.path.join(dir, pati)) if not i.startswith(".")]:
			with codecs.open(os.path.join(dir, pati, fili), "r", "utf-8") as inputfili:
				inputad=ct.adtextextractor(inputfili.read(), fili)
			result=[k.findall(inputad) for k in search_terms]
			if sum([len(i) for i in result]) > 6:
				for n, i in enumerate(result):
					print search_terms[n].pattern, n,i
				print os.path.join(dir, pati, fili), "\n"
			
	endtime=time.time()
	print "This took us {} minutes".format((endtime-starttime)/60)
	

emoticonfinder ("/home/ps22344/Downloads/craig_0208")
