import numpy as np
import re
import clustertools as ct
import time
import os
import codecs
from collections import defaultdict
import json 


def dictbuilder(input_path, output_file):
	"""
	reads files in input_path	
	input_path needs to have subfolders. 
	if "remove_numbers", does not count numbers (as in "\d+").
	This was used for IDing leetspeak.
	"""
	worddict=defaultdict(int)
	for pati in [i for i in os.listdir(input_path) if not i.startswith(".")]:
		print pati
		for fil in [i for i in os.listdir(os.path.join(input_path, pati)) if not i.startswith(".")]:
			fili=codecs.open(os.path.join(input_path, pati, fil), "r", "utf-8")
			inputad=ct.adtextextractor(fili.read(), fil)
			inputad=inputad.lower()
			tokenized=ct.tokenizer(inputad)
			tokenized=[re.sub("\W","", i) for i in tokenized]
			if remove_numbers:
				tokenized=[i for i in tokenized if not re.match("\d+", i)]
			for token in [i for i in tokenized if i]:
				worddict[token]=worddict[token]+1
	print ("\n".join([":".join((k, unicode(worddict[k]))) for k in sorted(worddict, key=worddict.get, reverse=True) if worddict[k] > 50]))
	print "We created a dictionary of {} total words with {} types".format(sum(worddict.values()), len(worddict.keys()))		
	if output_file:
		with codecs.open(output_file, "w", "utf-8") as outputfile:
			json.dump(worddict, outputfile)	
			print "Dict written to ", outputfile