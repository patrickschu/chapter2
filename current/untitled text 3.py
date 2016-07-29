#!/Users/ps22344/Downloads/virtualenv/chapter2_env/bin/python
from nltk.stem import porter
from gensim.models import Word2Vec
import gzip
import sklearn
from sklearn.cluster import KMeans, MiniBatchKMeans, AgglomerativeClustering
import clustertools as ct

header="\n\n----\n\n"
newmod=Word2Vec.load("model_1")
#newmod=Word2Vec.load_word2vec_format('/Users/ps22344/Downloads/GoogleNews-vectors-negative300.bin.gz', binary=True)
print header, "working with ", newmod.syn0.shape, header
#print newmod.syn0
for key  in newmod.vocab:
	print key, newmod.vocab[key].__dict__['index']


# print "sex", newmod.most_similar(positive=['sex'])
# print 'woman', newmod.most_similar(positive=['woman'])
# print 'girl',newmod.most_similar(positive=['girl'])
# 
# print 'man',newmod.most_similar(positive=['man'])
# print 'guy',newmod.most_similar(positive=['guy'])
# 
# print 'gay',newmod.most_similar(positive=['gay'])


# for k in [2, 4,8,16,32]:
# 	print "clustering"
# 	#clustering=AgglomerativeClustering(n_clusters=k, affinity='cosine', linkage='complete')
# 	clustering=KMeans(n_clusters=k, max_iter=1000, n_init=100)
# 	result=clustering.fit(newmod.syn0)
# 	clusteringstats=ct.Clusteringstats(newmod.syn0, newmod.syn0, result, result.labels_)
# 	print header, k
# 	print clustering
# 	print clusteringstats.size_of_clusters()
# 	print clusteringstats.cluster_silhouette('cosine')
# 	#link label to word, group by clusters
# 	#matrix_with_cats, matrix_without_cats, name, labels , centroids=None




