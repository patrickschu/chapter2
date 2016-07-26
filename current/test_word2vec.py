#!/Users/ps22344/Downloads/testenv/my_env/bin/python

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

print "mein freund"


documents = ["Human machine interface for lab abc computer applications",
             "A survey of user opinion of computer system response time",
             "The EPS user interface management system",
             "System and human system engineering testing of EPS",
             "Relation of user perceived response time to error measurement",
             "The generation of random binary unordered trees",
             "The intersection graph of paths in trees",
             "Graph minors IV Widths of trees and well quasi ordering",
             "Graph minors A survey"]

# 
# pprint.pprint(documents)
# 
# docs=[[w.lower() for w in doc.split() if len(w) > 1]for doc in documents]
# 
# pprint.pprint(docs)
# 
# dict = corpora.Dictionary(docs)
# print dict.token2id
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
# print model.syn0.shape
# 
# #Note that there is a gensim.models.phrases module
# 
# end=time.time()
# print "this took us freaking {} minutes!".format((end-now)/60)


featureVec=np.array([[1.,2,3,4],[22.,33,11,0], [1.,2,3,4]])
print featureVec
featureVec = np.divide(featureVec,2)
print featureVec
