#!/Users/ps22344/Downloads/virtualenv/chapter2_env/bin/python
from nltk.stem import porter
from gensim.models import Word2Vec
import gzip
import sklearn
from sklearn.cluster import KMeans, MiniBatchKMeans, AgglomerativeClustering
import clustertools as ct
from collections import defaultdict
import json
import codecs
import time
import os
header="\n\n----\n\n"
newmod=Word2Vec.load("model_1")

nclusters=[16,32, 54]


def word2vecclustermaker(model, no_clusters, distance_metric):
	"""
	This takes 
	a word2vec model created by gensim.Word2Vec, 
	a list of cluster numbers to compute, 
	and a distance metric to use.
	The resulting clusters are output as json files formatted {cluster X: {indexes:[], words:[], vectors:[], cluster Y:{}}.
	It prints the silhouette score and the distribution of words over clusters. 
	"""
	
	for k in no_clusters:
		print "clustering"
		#clustering=AgglomerativeClustering(n_clusters=k, affinity=distance_metric, linkage='average')
		clustering=KMeans(n_clusters=k, max_iter=1000, n_init=100)
		result=clustering.fit(newmod.syn0)
		clusteringstats=ct.Clusteringstats(newmod.syn0, newmod.syn0, result, result.labels_)
		print clustering
		print clusteringstats.size_of_clusters()
		print "silhouette", clusteringstats.cluster_silhouette(distance_metric)
		clusterdict=defaultdict(dict)
		for item in range(0, k):
			#print item
			clusterdict[item]['indexes']= [i for i, x in enumerate(result.labels_) if x == item]
		
			clusterdict[item]['words']=[e for e in newmod.vocab.keys() for i in clusterdict[item]['indexes'] if newmod.vocab[e].__dict__['index']==i]
			#clusterdict[item]['vectors']=[newmod[e].tolist() for e in clusterdict[item]['words']]
		with codecs.open(os.path.join("outputfiles","clusters_"+str(k)+"_"+time.strftime("%H_%M_%m_%d")+".json"), "w", "utf-8") as outputfile:
			json.dump(clusterdict, outputfile)
		print "output to ", "clusters_"+str(k)+"_"+time.strftime("%H_%M_%m_%d")+".json"

word2vecclustermaker(newmod, nclusters, 'euclidean')

# for k in nclusters:
# 	print "clustering"
#  	clustering=AgglomerativeClustering(n_clusters=k, affinity='euclidean', linkage='average')
#  	#clustering=KMeans(n_clusters=k, max_iter=1000, n_init=100)
#  	result=clustering.fit(newmod.syn0)
#  	clusteringstats=ct.Clusteringstats(newmod.syn0, newmod.syn0, result, result.labels_)
#  	print clustering
#  	print clusteringstats.size_of_clusters()
#  	print "silhouette", clusteringstats.cluster_silhouette('cosine')
# 	clusterdict=defaultdict(dict)
# 	for item in range(0, k):
# 		#print item
# 		clusterdict[item]['indexes']= [i for i, x in enumerate(result.labels_) if x == item]
# 		
# 		clusterdict[item]['words']=[e for e in newmod.vocab.keys() for i in clusterdict[item]['indexes'] if newmod.vocab[e].__dict__['index']==i]
# 		#clusterdict[item]['vectors']=[newmod[e].tolist() for e in clusterdict[item]['words']]
# 	with codecs.open(os.path.join("outputfiles","clusters_"+str(k)+"_"+time.strftime("%H_%M_%m_%d")+".json"), "w", "utf-8") as outputfile:
# 		json.dump(clusterdict, outputfile)
# 	print "output to ", "clusters_"+str(k)+"_"+time.strftime("%H_%M_%m_%d")+".json"
	#matrix_with_cats, matrix_without_cats, name, labels , centroids=None





# t= clusterdict[0]['words'].index('girl')
# print t
# print clusterdict[0]['words'][t]
# print clusterdict[0]['indexes'][t]
# print clusterdict[0]['vectors'][t]
# print newmod['girl']
# print newmod['girl'] == clusterdict[0]['vectors'][t]


#newi= newmod.syn0[0]

#tt=json.load('/Users/ps22344/Downloads/chapter2/current/outputfiles/clusters_2_15_38_07_29.json')
#this checks on words



# ii= newmod['i']
# 
# print newi, header
# 
# print ii, header
# 
# 
# print newi == ii 
#print newmod.vocab[key].__dict__
# print "sex", newmod.most_similar(positive=['sex'])
# print 'woman', newmod.most_similar(positive=['woman'])
# print 'girl',newmod.most_similar(positive=['girl'])
# 
# print 'man',newmod.most_similar(positive=['man'])
# print 'guy',newmod.most_similar(positive=['guy'])
# 
# print 'gay',newmod.most_similar(positive=['gay'])
#print [k for k in newmod.vocab.keys() for i in range(0,newmod.syn0.shape[0]) if newmod.vocab[k].__dict__['index']==i]
#print newmod.vocab.__dict__
