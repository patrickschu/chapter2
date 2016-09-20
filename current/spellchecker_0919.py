#!/Users/ps22344/Downloads/virtualenv/chapter2_env/bin/python


##Doing a spellchecker
## With pyenchant
##This needs to run in virtual env

import time
import enchant
from string import punctuation
import codecs
import re
import os
import clustertools as ct
import nltk
from collections import defaultdict
import json


exclude=["<br>", "<br/>", "\n", " "]+list(punctuation)
excluderegex=re.compile("^["+"|\\".join(exclude)+"]+$")
punctuationregex=re.compile("["+"|\\".join(list(punctuation))+"|\d+]+")
stopregex=re.compile(r"([\.|\?|\!|\-|,]+)(\w)")

pathi='/Users/ps22344/Downloads/craigbalanced_0601'



spelldicti=enchant.Dict("en_US")

#for personal word list, do this:
#d2 = enchant.DictWithPWL("en_US","mywords.txt")


#it comes with a tokenizer
#from enchant.tokenize import get_tokenizer
#tknzr = get_tokenizer("en_US")

#compute frequency of non-standard words
#check on capitalization
#the filelist needs to include the subfolder



def nonstandardcounter(filelist):
	count=0
	filedict={}
	typodict=defaultdict(float)
	for fili in filelist:
		#print fili
		#print os.path.join(pathi,  fili)
		inputfile=codecs.open(os.path.join(pathi,  fili), "r", "utf-8").read()
		inputad=ct.adtextextractor(inputfile, fili)
		count=count+1
		filedict[count]=os.path.join(pathi,  fili)
		addspace=stopregex.sub(r"\g<1> \g<2>", inputad)
		splittext=nltk.word_tokenize(addspace)
		#splittext=[s for s in splittext if s not in exclude]
		splittextlo=[s for s in splittext if s]
		for word in [w for w in splittextlo if not spelldicti.check(w) and w not in list(punctuation)]:
			typodict[word]=typodict[word]+1
	return (typodict)

filis=[[os.path.join(i, x) for x in os.listdir(os.path.join(pathi,i)) if not x.startswith(".")] for i in os.listdir(pathi) if not i.startswith(".")]
print len(filis)
#the miracle of flattening
#for each item in sublist, replace the sublist with this item
filis=[fili for fililist in filis for fili in fililist]
print "We have {} files".format(len(filis))

dicti=nonstandardcounter(filis)


sorti=[(k,dicti[k]) for k in sorted(dicti, key=dicti.get, reverse=True)]
with codecs.open("typodict_"+time.strftime("%Y%m%d")+".json", "w", "utf-8") as outputfile:
	json.dump(dicti, outputfile)
	
for entry in sorti:
	print entry
