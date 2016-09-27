import re
import nltk
import codecs
import os
import clustertools as ct
import time

#create the featuredict from a text file
featuredict={}
with codecs.open('/Users/ps22344/Downloads/chapter2/textfiles/emolist_final.txt', "r", "utf-8") as inputtext:
	for line in inputtext.readlines():
		featuredict[line.rstrip("\n")]=0




#test formatting
for k in featuredict:
	if k.startswith(" "):
		print k



#dataset
dir='/Users/ps22344/Downloads/craig_0208/'#adfiles_output_0116'


#check if we find items
starttime=time.time()

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
	

# inputad="I have been home for days now.what else is     there to do ?! Give me the icecream..."
# 
# 
# #this is used to add spaces between stops and the following word
# stopregex=re.compile(r"([\.|\?|\!|\-|,]+)(\w)")
# 
# def tokenizer(input_string):
# 	"""
# 	The tokenizer takes a string of words.
# 	It fixes quirky punctuation that trips us the NLTK Word Tokenizer. 
# 	Then it runs nltk.word_tokenize() to return a list of words>
# 	"""
# 	addspace=stopregex.sub(r"\g<1> \g<2>", input_string)
# 	splittext=nltk.word_tokenize(addspace)
# 	return splittext

#splittext=[s for s in splittext if s not in exclude]
#splittextlo=[s.lower() for s in splittext if s and not excluderegex.match(s)]