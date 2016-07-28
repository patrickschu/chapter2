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
folderlist=[i for i in os.listdir(pathi) if not i.startswith(".")]
#folderlist=['3']
print folderlist


stemmer=porter.PorterStemmer()
#initialize model here

exclude=["<br>", "<br/>", "\n", " "]+list(punctuation)
print [type(i) for i in exclude]
#excluderegex=["("+e+")" for e in exclude]
excluderegex=re.compile("^["+"|\\".join(exclude)+"]+$")
punctuationregex=re.compile("["+"|\\".join(list(punctuation))+"|\d+]+")


	
def sentencefeeder(folder_list):
	for folder in folder_list:
		filis=[i for i in os.listdir(os.path.join(pathi, folder)) if not i.startswith(".")]
		for fili in filis:
			with codecs.open(os.path.join(pathi, folder,fili), "r", "utf-8") as inputfile:
				ad=adtextextractor(inputfile.read(), fili)
			sents=sent_tokenize(ad)
			#print sents, len(sents)
			#sents=[sent_tokenize(s) for s in sents]
			sents=[s for s in sents if s not in exclude]
			sents=[re.split(r"(<br/>|\n|\.\.+)", s) for s in sents]
			#flatten sents
			sents=[s for longsent in sents for s in longsent]
			sents=[s.lower() for s in sents if s and not excluderegex.match(s)]
			for sent in sents:
				#print [re.sub(punctuationregex, "assssiAAAA",s) for s in sent.split()]
				# print [re.sub(excluderegex, "ASSSI", s) for s in sent]
 				sent=[re.sub(punctuationregex, "",s) for s in sent.split()]
 				#yield [stemmer.stem(s) for s in sent if s]
 				yield [s for s in sent if s]

model = Word2Vec(size=1000, min_count=5, workers=4, sg=1)
			
model.build_vocab(sentencefeeder(folderlist))
model.train(sentencefeeder(folderlist))

#save it
model.save("model_1")
#look at it
print "model saved"




#class gensim.models.word2vec.Word2Vec(sentences=None, size=100, alpha=0.025, window=5, min_count=5, max_vocab_size=None, sample=0.001, seed=1, workers=3, min_alpha=0.0001, sg=0, hs=0, negative=5, cbow_mean=1, hashfxn=<built-in function hash>, iter=5, null_word=0, trim_rule=None, sorted_vocab=1, batch_words=10000





# 
# print np.prod([ 0.09915783, -0.03299134, -0.01437753,  0.00536732,  0.06406488])
# print np.prod([ 0.08549197, -0.075089,   -0.01246947, -0.04792206, -0.00101304])
# print np.prod([ 0.03188382,  0.0699484,  -0.0095439,  -0.04693603, -0.07593358])
# 
# documents = ["Human machine interface for lab abc computer applications",
#              "A survey the of the user opinion of computer the system the response time",
#              "The EPS user interface management system",
#              "the System the and human system engineering testing of EPS",
#              "Relation the of the user perceived response time to error measurement",
#              "The generation the of the random binary unordered trees",
#              "The intersection graph the of the paths in trees",
#              "Graph minors IV Widths the of the trees and well quasi ordering",
#              "Graph minors A survey"]
# 
# pprint.pprint(documents)
# # 
# docs=[[w.lower() for w in doc.split() if len(w) > 1]for doc in documents]
# 
# model = Word2Vec()
# print model.scan_vocab(docs)#.raw_vocab
# 
# model.build_vocab([i for i in docs])
# print "dict length", len(model.vocab), "\n"
# for entry in model.vocab:
# 	print "entry '", entry, "'", model.vocab[entry]
# print model.syn0
# model.train(['the','the','the','the','of'])
# print "dict length", len(model.vocab), "\n"
# #print model.vocab['trees']
# for entry in model.vocab:
# 	print "entry '", entry, "'", model.vocab[entry]


#print model.syn0
#for s in model.syn0:
#	print len(s)

#model.vocab stores the dictionary of word counts and word indexea


# from source code 
#         if sentences is not None:
#             if isinstance(sentences, GeneratorType):
#                 raise TypeError("You can't pass a generator as the sentences argument. Try an iterator.")
#             self.build_vocab(sentences, trim_rule=trim_rule)
#             self.train(sentences)


# 
# newsi=dict.doc2bow("Relation of user perceived response time to error measurement".split())
# #print newsi
# 
# 
# model = Word2Vec(docs, size=100, window=5, min_count=3, workers=4)
# print model.most_similar(positive=["relation"])
#print model['user']

# now=time.time()
# pathi=os.path.expanduser(os.path.join("~/", "Downloads", "craigbalanced_0601", "1"))
# 
# filis=[i for i in os.listdir(os.path.join(pathi)) if not i.startswith(".")]
# 
# model= Word2Vec(size=2000)
# 
# def getgo(filis):
# 	for f in filis:
# 		with open(os.path.join(pathi,f), "r") as inputfile:
# 		 	yield([i.lower() for i in inputfile.read().split()])
# 
# model.build_vocab(getgo([i for i in os.listdir(os.path.join(pathi)) if not i.startswith(".")]))
# #model.syn0 is the entire dictionary
# model.save("word2vecmodel")
# print model.syn0.shape
# 
# #Note that there is a gensim.models.phrases module
# 
# end=time.time()
# print "this took us freaking {} minutes!".format((end-now)/60)
# 
# 
# featureVec=np.array([[1.,2,3,4],[22.,33,11,0], [1.,2,3,4]])
# print featureVec
# featureVec = np.divide(featureVec,2)
# print featureVec


# gensim.models.phrases 
# 
# he methods accept an iterable of sentences