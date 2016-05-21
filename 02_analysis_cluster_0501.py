import clustertools as ct
import os
import re 
import shutil
import string
import nltk
import codecs 
import scipy, scipy.cluster, scipy.spatial
import time
import sklearn
import itertools
import numpy as np 
from sklearn import cluster, mixture, metrics
from scipy import spatial, sparse
from collections import defaultdict
from nltk.tokenize import word_tokenize


metriclist=[['cityblock', 'cosine', 'euclidean', 'l1', 'l2', 'manhattan'],['braycurtis', 'canberra', 'chebyshev', 'correlation', 'dice', 'hamming', 'jaccard', 'kulsinski', 'mahalanobis', 'matching', 'minkowski', 'rogerstanimoto', 'russellrao', 'seuclidean', 'sokalmichener', 'sokalsneath', 'sqeuclidean', 'yule']]
scipy_distances=['euclidean', 'minkowski', 'cityblock', 'seuclidean', 'sqeuclidean', 'cosine', 'correlation','hamming', 'jaccard', 'chebyshev', 'canberra', 'braycurtis', 'mahalanobis', 'yule', 'matching', 'dice', 'kulsinski', 'rogerstanimoto', 'russellrao', 'sokalmichener', 'sokalsneath', 'wminkowski']

print "start"
print "\n---------------\nSome public service announcements"

#moving parts
pathi=os.path.join("craig_0208")

def dictmaker(folderlist, threshold):
	##	
	###BUILDING VOCAB
	#threshold sets how many times a word needs to occur to be included in the featuredict
	vocab={}
	for folder in folderlist:
		filis=[i for i in os.listdir(os.path.join(pathi,folder)) if not i.startswith(".")]
		print "Building vocab: we have {} files in folder {}".format(len(filis), folder)
		#collect a dictionary with all words
		#lowercase them    
		for fili in filis:
			inputfile=codecs.open(os.path.join(pathi, folder, fili), "r", "utf-8").read()
			inputtext=ct.adtextextractor(inputfile, fili)
			splittext=nltk.word_tokenize(inputtext)
			splittextlo=[i.lower() for i in splittext]
			#do we want to lemmatize or things like that
			for word in splittextlo:
				if word not in vocab:
					vocab[word]=1
				else:
					vocab[word]=vocab[word]+1
	print "Our vocab dictionary has {} entries".format(len(vocab))
	#here we set the threshold
	featuredict= {key:value for key, value in vocab.items() if value > float(threshold) }
	print "Our feature dictionary has {} entries\n---------------\n".format(len(featuredict))
	return featuredict
	

def categorymachine(folderlist):
	##
	###FINDING CATEGORIES
	#this just extracts the categories from our files
	print "starting category machine"
	catdicti={}
	catnumber=0
	for folder in folderlist:
		filis=[i for i in os.listdir(os.path.join(pathi,folder)) if not i.startswith (".")]
		for fili in filis:
			inputfile=codecs.open(os.path.join(pathi, folder,fili), "r", "utf-8").read()
			inputtext=ct.adtextextractor(inputfile, fili)
			# lets establish the category
			# we need to make it numeric, so the numpy won't screw up
			category=ct.tagextractor(inputfile, "category1", fili)
			try: 
				cat=catdicti[category]
			except:
				print "We added {} to the category dictionary, coded as {}".format(category, catnumber)
				catdicti[ct.tagextractor(inputfile, "category1", fili)]=catnumber
				catnumber=catnumber+1
				cat=catdicti[ct.tagextractor(inputfile, "category1", fili)]
	return (catdicti, catnumber)



def matrixmachine(folderlist, featuredict, testmode, *args):
	#
	###BUILDING MATRICES
	#
	# args are external categories
	#matrixmachine takes a list of folders	and of external categories to be included, note that it calls on the category machine 
	print "Starting the matrixmachine"
	print "external categories: ", len(args)
	print args
	#the plus one in here is for the file id
	wordmatrix=np.empty(shape=(1,(len(featuredict)+len(args)+1)))
	print "Matrix initial shape: ", np.shape(wordmatrix)
	# making a dictionary for the categories
	# we need the zero cause the machine returns 2 items
	count=0
	catdicti=categorymachine(folderlist)[0]
	filedict={}
	for folder in folderlist:
		filis=[i for i in os.listdir(os.path.join(pathi, folder)) if not i.startswith(".")]
		if testmode == True:
			print "\n\nRUNNING\nIN\nTEST\nMODE\n"
			filis=filis[:30]
		print "Building matrices: we have {} files in folder {}".format(len(filis), folder)
		for fili in filis:
			inputfile=codecs.open(os.path.join(pathi, folder, fili), "r", "utf-8").read()
			#establish category
			for external_cat in args:
				cat=catdicti[ct.tagextractor(inputfile, external_cat, fili)]
			count=count+1
			filedict[count]=os.path.join(pathi, folder, fili)
			#note that punctuation is still in here
			splittext=nltk.word_tokenize(inputfile)
			splittextlo=[i.lower() for i in splittext]
			wordcount=float(len(splittextlo))
			# this is a per word frequency
			wordvector=np.array([float(cat)]+[float(count)]+[float(splittextlo.count(i))/wordcount for i in featuredict])
			#print wordvector
			#we append it to the matrix
			wordmatrix=np.append(wordmatrix, [wordvector], axis=0)
	print "Features of word matrix: shape {}, dtype {}".format(np.shape(wordmatrix), wordmatrix.dtype)
	print "---------------\nEnd of public service announcements\n\n"
	#"In 2D, the first dimension corresponds to rows, the second to columns."
	# we don't look at the first row cause that was just for initialization
	# the one without cats we put into the clustering algorithm
	wordmatrix_without_cat=wordmatrix[1:wordmatrix.shape[0],len(args)+1:wordmatrix.shape[1]]
	print "without", np.shape(wordmatrix_without_cat)
	wordmatrix_with_cat=wordmatrix[1:wordmatrix.shape[0],]
	print "with", np.shape(wordmatrix_with_cat)
	return (wordmatrix_without_cat, wordmatrix_with_cat, catdicti, filedict)
	
	

def clustermachine(matrix, distance_metric, clusters=4):
	#we need a similarity matrix to feed into some of the algos
	similarity_matrix=metrics.pairwise.euclidean_distances(matrix)	
	#meanshift and kmeans take features, others need distance matrixes
	no_of_clusters=range(clusters)	
	result=[]
	t=time.time()
	
	## # 1: kmeans
# 	model=sklearn.cluster.KMeans(clusters,tol=0)
# 	clustering=model.fit(matrix)
# 	centroids=clustering.cluster_centers_
# 	labels=clustering.labels_
# 	inertia=clustering.inertia_
# 	kmeans=ct.Clustering(model, clustering.labels_, clustering.cluster_centers_)
# 	result.append(kmeans)
# 	print [i.name for i in result][len(result)-1], [i.no_of_clusters for i in result][len(result)-1]
# 	u=time.time()
# 	print (u-t)/60
		#
	###CREATING CLUSTERS
	#
	#this makes clusters; takes the dataset (matrix) and the algorithm

#	## #2: MeanShift, takes forever @  12600, 42
#	model=sklearn.cluster.MeanShift()
#	clustering=model.fit(matrix)
#	centroids=clustering.cluster_centers_
#	labels=clustering.labels_
#	meanshift=ct.Clustering(model, clustering.labels_, clustering.cluster_centers_)
#	result.append(meanshift)
#	u=time.time()
#	print [i.name for i in result][len(result)-1]
#	print (u-t)/60
#	
	# 3: Affinity Propagation, breaks @ 12600, 42
# 	model=sklearn.cluster.AffinityPropagation()
# 	clustering=model.fit(matrix)
# 	centroid_index=model.cluster_centers_indices_
# 	centroids=clustering.cluster_centers_
# 	labels=clustering.labels_
# 	aff_matrix=clustering.affinity_matrix_
# 	its= clustering.n_iter_
# 	affinity=ct.Clustering(model, clustering.labels_, clustering.cluster_centers_)
# 	result.append(affinity)
# 	u=time.time()
# 	print [i.name for i in result][len(result)-1], [i.no_of_clusters for i in result][len(result)-1]
# 	print (u-t)/60
	
# 	## #4: Spectral clustering
# 	model=sklearn.cluster.SpectralClustering()
# 	clustering=model.fit(matrix)
# 	labels=clustering.labels_
# 	aff_matrix=clustering.affinity_matrix_
# 	spectral= ct.Clustering(model, clustering.labels_)
# 	result.append(spectral)
# 	u=time.time()
# 	print [i.name for i in result][len(result)-1], [i.no_of_clusters for i in result][len(result)-1]
# 	print (u-t)/60


##watch out --------- centroids are indices!!!!!

	
# 	## # 5: DBCASN, eanShift, takes forever @  12600, 42
# 	for x in [0.025,0.05, 0.075, 0.1, 0.25, 0.5, 0.75, 1, 1.25, 1.5, 1.75, 2, 2.25]:
# 		model=sklearn.cluster.DBSCAN(eps=x, metric=distance_metric, algorithm='brute')
# 		clustering=model.fit(matrix)
# 		core_samples=clustering.core_sample_indices_
# 		components=clustering.components_
# 		labels=clustering.labels_
# 		print labels
# 		dbscan= ct.Clustering(model, clustering.labels_, clustering.core_sample_indices_)
# 		result.append(dbscan)
# 		u=time.time()
# 		print [i.name for i in result][len(result)-1], [i.no_of_clusters for i in result][len(result)-1]
# 		print (u-t)/60
#	
#	##GUASSIN DOEs NOT FIT OUR SCHEMA AT THIS POINT
#	## 6: GAUSSIAN MIXTURE. eh this does not really fit in here
	for x in range(2,44):
		model=sklearn.mixture.DPGMM(x)
		clustering=model.fit(matrix)
		labels=model.fit_predict(matrix)
		weights=model.weights_
		means=clustering.means_
		print "bic", model.bic(matrix)
		print "aic", model.aic(matrix)
		print "components", clustering.n_components
		centroids=clustering.means_
		converged=clustering.converged_	
		print "converged?", converged
		gauss= ct.Clustering(model, model.fit_predict(matrix), clustering.means_)
		u=time.time()
		result.append(gauss)
		#print [i.name for i in result][len(result)-1]
		#print (u-t)/60
#	
#
	#These are essentially trees; maybe need a different approach. They are kinda predictive
	
# 	## #7: Agglomerative 

# 	for x in range(2,6):
# 		model=sklearn.cluster.AgglomerativeClustering(affinity=distance_metric, n_clusters=x, linkage='complete')
# 		clustering=model.fit(matrix)
# 		labels=clustering.labels_
# 		leaves=clustering.n_leaves_
# 		children=clustering.children_
# 		components=clustering.n_components_
# 		ward= ct.Clustering(model, clustering.labels_)
# 		result.append(ward)
# 		u=time.time()
# 		print [i.name for i in result][len(result)-1], [i.no_of_clusters for i in result][len(result)-1]
# 		print (u-t)/60
# # 	
# 
# 	print [i.name for i in result][len(result)-1], [i.no_of_clusters for i in result][len(result)-1]
# 	print (u-t)/60

	
	
	
# 	model=sklearn.cluster.AgglomerativeClustering(affinity='cosine', linkage='complete')
# 	clustering=model.fit(matrix)
# 	labels=clustering.labels_
# 	leaves=clustering.n_leaves_
# 	components=clustering.n_components_
# 	ward= ct.Clustering(model, clustering.labels_)
# 	result.append(ward)
# 	u=time.time()
# 	print [i.name for i in result][len(result)-1], [i.no_of_clusters for i in result][len(result)-1]
# 	print (u-t)/60

# 	## #8: Birch Hierarchical 	
# 	model=sklearn.cluster.Birch(threshold=0.025)
# 	clustering=model.fit(matrix)
# 	labels=clustering.labels_
# 	root=clustering.root_
# 	subcluster_labels=clustering.subcluster_labels_
# 	birch= ct.Clustering(model, clustering.labels_)
# 	result.append(birch)
# 	u=time.time()
# 	print [i.name for i in result][len(result)-1], [i.no_of_clusters for i in result][len(result)-1]
# 	print (u-t)/60
	
	return(result)
	
	
	#######MAIN#########


	 
def main(distance_metric):
	starttime=time.time()
	folders=[i for i in os.listdir(pathi) if not i.startswith(".")]
	print ", ".join(folders)
	print ", ".join([str(len(os.listdir(os.path.join(pathi,f)))) for f in folders])
	#folders=['files9_output_0102']#, 'files9_output_0102', 'files9_output_0102', 'files9_output_0102','files9_output_0102', 'files9_output_0102','files9_output_0102', 'files9_output_0102', 'files9_output_0102'] 
	print "We have {} folders".format(len(folders))
	featuredict=dictmaker(folders, 10000)
	wordmatrix_without_cat, wordmatrix_with_cat, catdicti, filedicti = matrixmachine(folders, featuredict, True, "category1")
	x=clustermachine(wordmatrix_without_cat,distance_metric,4)
	#print [(i.name, i.no_of_clusters) for i in x]
	excludelist=['total','no_of_categories', 'no_of_clusters', 'no_of_cats']
	print "These clusterings have less than 2 clusters\n{}\n\n".format("\n".join([str(c.name) for c in x if c.no_of_clusters < 2]))
	#PRINTING STUFF
	headline="\n\n-----------\n\n"
	print "Working with {} distance metric".format(distance_metric)
	for clustering in [c for c in x if c.no_of_clusters > 1]:
		cati=ct.Categorystats(wordmatrix_with_cat, clustering.name, clustering.labels)
		sili=ct.Clusteringstats(wordmatrix_with_cat, wordmatrix_without_cat, clustering.name, clustering.labels).cluster_silhouette(distance_metric)
	
		#GENERAL STATS
	 	print headline, headline, "CLUSTERING CALLED {} HAS {} CLUSTERS". format(clustering.getname()[0], clustering.no_of_clusters)
		print "Its silhouette score is {}".format(str(sili))
		stats=ct.Clusteringstats(wordmatrix_with_cat, wordmatrix_without_cat, clustering.name, clustering.labels).size_of_clusters()
		catstats=ct.Clusteringstats(wordmatrix_with_cat, wordmatrix_without_cat, clustering.name, clustering.labels).cats_per_cluster()
		for cluster in stats:
			print "\nCluster {} contains {} items, {} % of the total".format(cluster, stats[cluster], round(float(stats[cluster])/len(wordmatrix_without_cat)*100))
			for cat in [i for i in catstats[cluster] if not i in excludelist]:
				print "{} items of category {} make up {} % of this cluster".format(catstats[cluster][cat], "".join([i[0] for i in catdicti.items() if i[1] == int(cat)]), round(catstats[cluster][cat]/catstats[cluster]['total']*100))
		cats=ct.Categorystats(wordmatrix_with_cat, clustering.name, clustering.labels).size_of_categories()
		
		#STATS PER CAT
		print headline,"Statistics per category"
		for cat in [i for i in cats if not i in excludelist]:
			print "\nCategory {} has {} items".format("".join([i[0] for i in catdicti.items() if i[1] == int(cat)]), cats[cat]['total'])
			for entry in [i for i in cats[cat]['cat_per_cluster'] if not i in excludelist]:
				print "{} items or {} percent in cluster {}".format(cats[cat]['cat_per_cluster'][entry], round(float(cats[cat]['cat_per_cluster'][entry])/float(cats[cat]['total'])*100), entry)

		#PREDICTIVE FEATURES
		###NOTE THAT THIS IS A BREAK POINT IF WE HAVE REALLY SMALL CLUSTERS
		print headline, "Strongly predictive features are"
		#centroids=ct.Centroidstats(wordmatrix_without_cat, clustering.name, clustering.labels, clustering.centroids)
		cents=ct.Centroidstats(wordmatrix_without_cat, clustering.name, clustering.labels, clustering.centroids).cluster_predictors(featuredict)
		if cents:
			for diff in cents:
				print "\nRaw Scores"
				print "Cluster {} and cluster {} are differentiated by \n{}\n\n\n".format(diff[0], diff[1], ", ".join([" : ".join(map(str, i[::-1])) for i in cents[diff]['raw_diff']][:10])) 
				print "Zscores"
				print "Cluster {} and cluster {} are differentiated by \n{}\n\n\n".format(diff[0], diff[1], ", ".join([" : ".join(map(str, i[::-1])) for i in cents[diff]['zscores_diff']][:10]))	
			
		
		#PROTOTYPES
		print headline, "Here is a typical document for each cluster"
		distance=distance_metric
		print "We set the distance metric to {}".format(distance)
		docs=ct.Centroidstats(wordmatrix_without_cat, clustering.name, clustering.labels, clustering.centroids).central_documents(wordmatrix_with_cat, filedicti)
		if docs:
			for cluster in docs:
				print "\nCLUSTER {} \n".format(cluster)
				with open(docs[cluster][distance][0]) as f:
					print f.read()
				if len(docs[cluster][distance]) > 8:
					print "\nOther files close by in cluster {}:\n".format(cluster)
					print ("{}\n"*8).format(*docs[cluster][distance][1:9])
	
	#CROSS CLUSTERING COMPARISON
	print headline, "Comparing clusterings"
	for clustering in [c for c in x if c.no_of_clusters > 1]:
		print headline, "CLUSTERING CALLED {} HAS {} CLUSTERS". format(clustering.getname()[0], clustering.no_of_clusters)
		print "Its silhouette score is {}".format(str(ct.Clusteringstats(wordmatrix_with_cat, wordmatrix_without_cat, clustering.name, clustering.labels).cluster_silhouette(distance_metric)))
	#all input does it just concatenate name + cluster # and supply clustering object to similarity measurement
	input=[(str(type(i.name)).split(".")[3].rstrip("'>")+"--"+str(i.no_of_clusters), i) for i in x]
	simi=ct.Clusteringsimilarity(wordmatrix_with_cat, wordmatrix_without_cat ,input)
	options=['adjustedrand_sim', 'adjustedmutualinfo_sim', 'jaccard_sim', 'v_sim', 'completeness_sim', 'homogeneity_sim', 'silhouette_score_sim']
	for o in options:
		print "\n---\n"
		ct.Clusteringsimilarity(wordmatrix_with_cat, wordmatrix_without_cat ,input).similarity_matrix(o)
	
	
	print "\n---\n"
	endtime=time.time()
	process=endtime-starttime
	print headline, "This took us {} minutes".format(process/60)
		#or do we want to do predictive features and typical document per cluster as well????	
	
main('cosine')

# Valid values for metric are:
# From scikit-learn: ['cityblock', 'cosine', 'euclidean', 'l1', 'l2', 'manhattan']. These metrics support sparse matrix inputs.
# From scipy.spatial.distance: ['braycurtis', 'canberra', 'chebyshev', 'correlation', 'dice', 'hamming', 'jaccard', 'kulsinski', 'mahalanobis', 'matching', 'minkowski', 'rogerstanimoto', 'russellrao', 'seuclidean', 'sokalmichener', 'sokalsneath', 'sqeuclidean', 'yule'] See the documentation for scipy.spatial.distance for details on these metrics. 
# These metrics do not support sparse matrix inputs.

##
####NOTES
##

# def categorystats
# def globalstats

## for each, give stats :
# -per cluster: (class Clusterstats)
# 		1. size (len per label)
# 		# 		
# 		2. split up btw categories how? (number, percentage)
#  				
# 		3. feature distinctive of cluster
# 				get centroids/prototypes per cluster
# 				find biggest difference between clusters
# 				[w,e,r,i,s,t]
# 				[w,e,r,i,s,t]
# 				[w,e,r,i,s,t]
# 				[w,e,r,i,s,t]
# 				...
# 				maybe:
# 				sort
# 				
# 				calculate distance first to last, while at it: also variance, means <--- feature description
# 				
# 				w=range:(x:y), mean: x, var: u, ... 
# 				[can we somehow calculate the importance / weight of one feature to each cluster?
# 				[in z scores???? normalized some kind of way
# 				biggest distnace is the difference maker
# 				
# 		
# 		4. homogeneity/tightness of cluster (distance btw poitns)
# 				same thing for points in each cluster
# 				maybe we do point product for each row
# 				
# 		
# 		
# - general
# 		5. distance btw clusters (centroids)
# 		6. homgeneity of clusters (cf 4)
# 		consistency of runs
# 		consistency of labeling / grouping certain data points together (??)
# 			consitstency btw clusters in one algo
# 			consistency btw different runs of one method
# 		
# - per category
# 		7. how split up btw clusters: how many n, what percentage is in each cluster? (dict of category: clusters per item)
# 		8. relate feature to category --> 3
# 		
# - think
# 		# label-independent quality
# # 		
# 		
# 		label-dependent quality:
# 		silhouette
		# V-measure: 0.917
		# Adjusted Rand Index: 0.952
		# Adjusted Mutual Information: 0.883
		# Silhouette Coefficient: 0.626
		
		
		
		
		
# heres what sklearn ppl do
# Estimated number of clusters: 3
# Homogeneity: 0.953
# Completeness: 0.883
# V-measure: 0.917
# Adjusted Rand Index: 0.952
# Adjusted Mutual Information: 0.883
# Silhouette Coefficient: 0.626

