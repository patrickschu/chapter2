import clustertools as ct
from collections import defaultdict
import json
import os
import codecs
import string

def dictbuilder(input_dir, output_name, lowercase=False, print_dict=False):
	"""
	The dictbuilder puts all words in the corpus (input_dir) into a dictionary and outputs as json. 
	Name of output file determined by output_name.
	If print_dict is set to True, prints our sorted dictionary.
	Format of the dict returned: {word:count, word:count, }
	"""
	dicti=defaultdict(float)
	for dir in [i for i in os.listdir(input_dir) if not i.startswith(".")]:
			print dir
			for fili in [i for i in os.listdir(os.path.join(input_dir, dir)) if not i.startswith(".")]:
				with codecs.open(os.path.join(input_dir, dir, fili), "r", "utf-8") as inputtext:
					inputad=ct.adtextextractor(inputtext.read(), fili)
				inputad=[w.rstrip(string.punctuation).lstrip(string.punctuation) for w in ct.tokenizer(inputad)]
				inputad=[w for w in inputad if w]
				if lowercase:
					for word in inputad:
						dicti[word.lower()]=dicti[word.lower()]+1
				else:
					for word in inputad:
						dicti[word]=dicti[word]+1
	if print_dict:
		print  "\n".join([":".join((i, str(dicti[i]))) for i in sorted(dicti, key=dicti.get, reverse=True)])
	with codecs.open(output_name+".json", "w", "utf-8") as outputi:
		json.dump(dicti, outputi, encoding="utf8")
	print "Written dictionary with {} items to ".format(len(dicti)), output_name
	return dicti
	
dictbuilder('/Users/ps22344/Downloads/craig_0208', "fulldict_0116", lowercase=True, print_dict=False)