#!/Users/ps22344/Downloads/virtualenv/chapter2/bin/python

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


print np.prod([ 0.09915783, -0.03299134, -0.01437753,  0.00536732,  0.06406488])
print np.prod([ 0.08549197, -0.075089,   -0.01246947, -0.04792206, -0.00101304])
print np.prod([ 0.03188382,  0.0699484,  -0.0095439,  -0.04693603, -0.07593358])

documents = ["Human machine interface for lab abc computer applications",
             "A survey the of the user opinion of computer the system the response time",
             "The EPS user interface management system",
             "the System the and human system engineering testing of EPS",
             "Relation the of the user perceived response time to error measurement",
             "The generation the of the random binary unordered trees",
             "The intersection graph the of the paths in trees",
             "Graph minors IV Widths the of the trees and well quasi ordering",
             "Graph minors A survey"]

pprint.pprint(documents)
# 
docs=[[w.lower() for w in doc.split() if len(w) > 1]for doc in documents]

model = Word2Vec()
print model.scan_vocab(docs)#.raw_vocab

model.build_vocab([i for i in docs])
print "dict length", len(model.vocab), "\n"
for entry in model.vocab:
	print "entry '", entry, "'", model.vocab[entry]
print model.syn0
model.train(['the','the','the','the','of'])
print "dict length", len(model.vocab), "\n"
#print model.vocab['trees']
for entry in model.vocab:
	print "entry '", entry, "'", model.vocab[entry]


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
from nltk.tokenize import word_tokenize
with codecs.open("positive.txt", "r", "latin-1") as inputfile:
	text=inputfile.read()
	
short_pos_words = word_tokenize(text)	
print type(short_pos_words)
