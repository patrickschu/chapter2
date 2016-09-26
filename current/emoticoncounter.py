import re
import nltk
import codecs
import os
import clustertools as ct


featuredict={}

with codecs.open('/Users/ps22344/Downloads/chapter2/textfiles/emolist_final.txt', "r", "utf-8") as inputtext:
	for line in inputtext.readlines():
		featuredict[line.rstrip("\n")]=0





for k in featuredict:
	if k.startswith(" "):
		print k




def tokenizer(input_string):
	"""
	The tokenizer takes a string of words.
	It fixes quirky punctuation that trips us the NLTK Word Tokenizer. 
	Then it runs nltk.word_tokenize() to return a list of words>
	"""
	addspace=stopregex.sub(r"\g<1> \g<2>", input_string)
	splittext=nltk.word_tokenize(addspace)
	return splittext
	
	
pati='/Users/ps22344/Downloads/craig_0208/adfiles_output_0116'
for fili in [i for i in os.listdir(pati) if not i.startswith(".")]:
	fili=codecs.open(os.path.join(pati, fili), "r", "utf-8")
	inputad=ct.adtextextractor(fili.read(), fili)
	

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