#!/Users/ps22344/Downloads/virtualenv/chapter2_env/bin/python

import string
import os
import codecs
import re
import time
from collections import defaultdict
import tokenfinder_1004 as tk
import spellchecker_1101 as spell
import clustertools as ct


def acronymfinder(dir):
	"""
	This finds acronyms. 
	"""
	start=time.time()
	capitals=re.compile("^[A-Z]+$")
	featuredict=defaultdict(int)
	#{
	#'lol':0
	#}
	
	for pati in [i for i in os.listdir(dir) if not i.startswith(".")]:
		print "working on", pati
		for fili in [i for i in os.listdir(os.path.join(dir, pati)) if not i.startswith(".")]:
			fili=codecs.open(os.path.join(dir, pati, fili), "r", "utf-8")
			inputad=ct.adtextextractor(fili.read(), fili)
			words=[w.rstrip(string.punctuation).lstrip(string.punctuation) for w in ct.tokenizer(inputad)]
			for item in words:
				if (capitals.match(item)) and (len(item) == 6):
					if not spell.spellchecker(item.lower()):
						featuredict[item] = featuredict[item]+1

	print sorted(featuredict.keys())
	print "SO many entries: ", len(featuredict)
	
	#sorted(d.items(), key=lambda x: x[1])
	#[":".join((i, str(y))) for i, y in sorted(featuredict, key=featuredict.get)]
	print  "\n".join([":".join((i, str(featuredict[i]))) for i in sorted(featuredict, key=featuredict.get, reverse=True)])
	mid=time.time()
	print "this took us {} minutes".format((mid-start)/60)
	for entry in sorted(featuredict):
		if featuredict[entry] > 5:
			print "\n\n\n***",entry,"\n\n"
			tk.tokenfinder([r"\s"+entry+"\s"], input_path='/Users/ps22344/Downloads/craig_0208/', length=20, lower_case=False)
	end=time.time()
	print "this took us {} minutes".format((end-start)/60)



acronymfinder('/Users/ps22344/Downloads/craig_0208')
#cool git update-index --assume-unchanged <file_to_ignore>