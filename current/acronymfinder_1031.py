import os
import codecs
import clustertools as ct
import re
from collections import defaultdict
iort tokenfinder_1004 as tk

def acronymfinder(dir):
	"""
	This finds acronyms. 
	"""
	featuredict=defaultdict(int)
	#{
	#'lol':0
	#}
	for pati in [i for i in os.listdir(dir) if not i.startswith(".")]:
		print pati
		for fili in [i for i in os.listdir(os.path.join(dir, pati)) if not i.startswith(".")]:
			fili=codecs.open(os.path.join(dir, pati, fili), "r", "utf-8")
			inputad=ct.adtextextractor(fili.read(), fili)
			words=ct.tokenizer(inputad)
			
			for item in words:
				if (re.match("^[A-Z]+$", item)) and (len(item) == 1):
					featuredict[item] = featuredict[item]+1
					#print item
		print featuredict
	for entry in featuredict:
		print "\n\n\n***",entry,"\n\n"
		tk.tokenfinder([r"\s"+entry+"\s"], input_path='/Users/ps22344/Downloads/craig_0208/', length=20, lower_case=False)

acronymfinder('/Users/ps22344/Downloads/craig_0208')
