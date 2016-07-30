import re
from string import punctuation
import os
import codecs 
import clustertools as ct
from nltk import word_tokenize

exclude=["<br>", "<br/>", "\n", " "]+list(punctuation)
excluderegex=re.compile("^["+"|\\".join(exclude)+"]+$") #we use this to identify tokens of punctuation only
punctuationregex=re.compile("["+"|\\".join(list(punctuation))+"|\d+]+") #we use this to find punctuation
stopregex=re.compile(r"([\.|\?|\!|\-|,]+)(\w)") #we use this to add whitespace after punct

htmlregex=re.compile(r"<.*?>")
linebreakregex=re.compile(r"(<br>|<br\/>)")


#remove after test
pathi=os.path.expanduser(os.path.join("~/", "Downloads", "craig_0208"))
folderlist=[i for i in os.listdir(pathi) if not i.startswith(".")]
print folderlist


ad="i LOVE YOu honeybaer.i want to be your firend???? </br>"
print "original", ad
def adcleaner(text, replace_linebreak=False, remove_html=False):
	"""
	The adcleaner processes ads to get them ready for sentence or word tokenization. 
	In this order:
	It adds whitespace after punctuation right before a word. 
	If replace_linebreak, it replaces every <br/> with a full stop, which is good for the sentence tokenizer. 
	If remove_html is True, removes everything "<>".
	It does not remove punctuation cause the word_tokenizer likes it.  
	It does not lowercase because the word_tokenizer likes that. 
	"""
	if replace_linebreak:
		text=linebreakregex.sub(".", text)
	text=stopregex.sub(r"\g<1> \g<2>", text)
	if remove_html:
		text=htmlregex.sub(" ", text)
	return text
	
for folder in folderlist:
	filis=[i for i in os.listdir(os.path.join(pathi,folder)) if not i.startswith(".")]
	print "Building vocab: we have {} files in folder {}".format(len(filis), folder)
	#collect a dictionary with all words
	#lowercase them    
	for fili in filis[:10]:
		inputfile=codecs.open(os.path.join(pathi, folder, fili), "r", "utf-8").read()
		inputtext=ct.adtextextractor(inputfile, fili)
		print "\n\n\npre",inputtext
		#pre-processing here
		inputtext=adcleaner(inputtext ,replace_linebreak=True, remove_html=False)
		splittext=word_tokenize(inputtext)
		splittextlo=[i.lower() for i in splittext]	
 		print "\n past", splittextlo
 		finaltext=[punctuationregex.sub("",i) for i in splittextlo]
 		finaltext=[i for i in finaltext if i and i not in ['br']]	
 		print finaltext
		



# def sentencefeeder(text):
# 	sents=sent_tokenize(text)
# 	#print sents
# 		sents=[s for s in sents if s not in exclude]
# 	#print sents
# 		sents=[re.split(r"(<br/>|\n|\.\.+)", s) for s in sents]
# 	#print sents
# 	#flatten sents
# 		sents=[s for longsent in sents for s in longsent]
# 	#print sents
# 		sents=[s.lower() for s in sents if s and not excluderegex.match(s)]
# 	#print sents
# 		for sent in sents:
# 			sent=[punctuationregex.sub("",s) for s in sent.split()]
# 		print sents
# 		return sents
	