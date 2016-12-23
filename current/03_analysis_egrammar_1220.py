import egrammartools as eg
import clustertools as ct
import numpy as np
import time
import sklearn
from sklearn import cluster
completestart=time.time()
listi=[]
dir="/home/ps22344/Downloads/craigbalanced_0601"

##prep
#add uniqs
uniqs, file_count=ct.uniqarraymachine(dir, 0) 	
print "So many files", file_count
listi.append(uniqs)

#add cats
categories_dict, no_of_categories = ct.categorymachine(dir, "category1")
category1=ct.categoryarraymachine(dir, "category1", categories_dict)
listi.append(category1)



##collect features
rep_raw, rep_freq= eg.repeatedpunctuationfinder(dir)
listi.append(np.array(rep_freq))


leet_raw, leet_freq= eg.leetcounter(dir)
listi.append(np.array(leet_freq))


rebfor_raw, rebfor_freq= eg.rebusfinder_for(dir)
listi.append(np.array(rebfor_freq))

rebto_raw, rebto_freq= eg.rebusfinder_to(dir)
listi.append(np.array(rebto_freq))

rebtoo_raw, rebtoo_freq= eg.rebusfinder_too(dir)
listi.append(np.array(rebtoo_freq))

caps_raw, caps_freq=eg.capsfinder(dir, 0.5)
listi.append(np.array(caps_freq))

single_raw, single_freq=eg.singleletterfinder(dir)
listi.append(np.array(single_freq))

clip_raw, clip_freq=eg.clippingcounter(dir)
listi.append(np.array(clip_freq))

acro_raw, acro_freq=eg.acronymcounter(dir)
listi.append(np.array(acro_freq))

emos_raw, emos_freq=eg.emoticonfinder(dir)
listi.append(np.array(emos_freq))
	
t=np.column_stack(listi)

print type(t), t.shape
completeend=time.time()

#this is the t w/out uniq and category
t_no_meta=t[2:]

print categories_dict

def clustermachine(matrix, distance_metric, clusters=4):
	"""
	The clustermachine takes a matrix with word freqs and clusters according to the distance_metric. 
	Clusters sets the input if algorithm needs a pre-determined number of clusters. 
	Last two inputs will not be used by all algorithms. 
	"""
	no_of_clusters=range(clusters)	
	result=[]
	t=time.time()
	
	## # 1: kmeans
	for x in [2,4,6]:
		model=sklearn.cluster.KMeans(x,tol=0)
		clustering=model.fit(matrix)
		centroids=clustering.cluster_centers_
		labels=clustering.labels_
		inertia=clustering.inertia_
		kmeans=ct.Clustering(model, clustering.labels_, clustering.cluster_centers_)
		result.append(kmeans)
		print [i.name for i in result][len(result)-1], [i.no_of_clusters for i in result][len(result)-1]
		u=time.time()
		print (u-t)/60
	return result

cc=clustermachine(t[2:], "euclidean")
print cc
print "This took us {} minutes. So slow!".format((completeend-completestart)/60)