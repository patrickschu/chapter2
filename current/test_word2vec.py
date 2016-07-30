#!/Users/ps22344/Downloads/virtualenv/chapter2_env/bin/python

#make a word2vec
#is this fun?
# who knows
import time
import os
import pprint
import gensim
from gensim import corpora
from gensim.models import Word2Vec
import numpy as np
import nltk
import codecs
import re
from nltk.tokenize import sent_tokenize
from string import punctuation
from nltk.stem import porter
import logging
#logging.basicConfig(format='%(asctime)s : (levelname)s : % (message)s', level=logging.INFO)
header="\n\n\n-------\n"

def adtextextractor(text, fili):
    regexstring="<text>(.*?)</text>"
    result=re.findall(regexstring, text, re.DOTALL)
    if len(result) != 1:
        print "alarm in adtextextractor", fili, result
    return result[0]

#build a w2v for my data
#separate into sentences
now=time.time()
pathi=os.path.expanduser(os.path.join("~/", "Downloads", "craigbalanced_0601"))

pathi=os.path.expanduser(os.path.join("~/", "Downloads", "craig_0208"))
folderlist=[i for i in os.listdir(pathi) if not i.startswith(".")]

print "folders", folderlist


stemmer=porter.PorterStemmer()
#initialize model here

exclude=["<br>", "<br/>", "\n", " "]+list(punctuation)
#print [type(i) for i in exclude]
#excluderegex=["("+e+")" for e in exclude]
excluderegex=re.compile("^["+"|\\".join(exclude)+"]+$")
punctuationregex=re.compile("["+"|\\".join(list(punctuation))+"|\d+]+")
stopregex=re.compile(r"([\.|\?|\!|\-|,]+)(\w)")

	
def sentencefeeder(folder_list):
	for folder in folder_list:
		filis=[i for i in os.listdir(os.path.join(pathi, folder)) if not i.startswith(".")]
		for fili in filis :
			with codecs.open(os.path.join(pathi, folder,fili), "r", "utf-8") as inputfile:
				ad=adtextextractor(inputfile.read(), fili)
			#print ad
			#ad a space after punctiation between words
			sents=r=stopregex.sub(r"\g<1> \g<2>", ad)
			#print sents
			sents=sent_tokenize(sents)
			#print sents
			sents=[s for s in sents if s not in exclude]
			#print sents
			sents=[re.split(r"(<br/>|\n|\.\.+)", s) for s in sents]
			#print sents
			#flatten sents
			sents=[s for longsent in sents for s in longsent]
			#print sents
			sents=[s.lower() for s in sents if s and not excluderegex.match(s)]
			#print sents
			for sent in sents:
				sent=[punctuationregex.sub("",s) for s in sent.split()]
				#print sent
				#print [s for s in sent if s]
 				#yield [stemmer.stem(s) for s in sent if s]
 				yield [s for s in sent if s]



 
for s in [100, 200, 400, 800, 1000, 2000]:
	print header, s 
	model = Word2Vec(size=s, min_count=10, workers=4, sg=1)
			
	model.build_vocab(sentencefeeder(folderlist))
	model.train(sentencefeeder(folderlist))
	print model
	#save it
	model.save("model_1")
	#look at it
	print "model saved"

	newmod=model
	print "sex", newmod.most_similar(positive=['sex'])
	print 'woman', newmod.most_similar(positive=['woman'])
	print 'girl',newmod.most_similar(positive=['girl'])

	print 'man',newmod.most_similar(positive=['man'])
	print 'guy',newmod.most_similar(positive=['guy'])

	print 'gay',newmod.most_similar(positive=['gay'])

	print 'cute',newmod.most_similar(positive=['cute'])

	print 'love', newmod.most_similar(positive=['love'])
	print 'love neg', newmod.most_similar(negative=['love']), header

#class gensim.models.word2vec.Word2Vec(sentences=None, size=100, alpha=0.025, window=5, min_count=5, max_vocab_size=None, sample=0.001, seed=1, workers=3, min_alpha=0.0001, sg=0, hs=0, negative=5, cbow_mean=1, hashfxn=<built-in function hash>, iter=5, null_word=0, trim_rule=None, sorted_vocab=1, batch_words=10000



# from source code 
#         if sentences is not None:
#             if isinstance(sentences, GeneratorType):
#                 raise TypeError("You can't pass a generator as the sentences argument. Try an iterator.")
#             self.build_vocab(sentences, trim_rule=trim_rule)
#             self.train(sentences)




# 
# #Note that there is a gensim.models.phrases module
# 
end=time.time()
print "this took us freaking {} minutes!".format((end-now)/60)
