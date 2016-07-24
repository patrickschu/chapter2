import clustertools as ct
import os, re, shutil,string,numpy,nltk,codecs, scipy, scipy.cluster, scipy.spatial, time, sklearn, itertools
import numpy as np 
from sklearn import cluster, mixture, metrics
from scipy import spatial, sparse
from collections import defaultdict
from nltk.tokenize import word_tokenize
# read the clustering documentation here: 
# http://docs.scipy.org/doc/scipy-0.14.0/reference/generated/scipy.cluster.vq.kmeans2.html

metriclist=[['cityblock', 'cosine', 'euclidean', 'l1', 'l2', 'manhattan'],['braycurtis', 'canberra', 'chebyshev', 'correlation', 'dice', 'hamming', 'jaccard', 'kulsinski', 'mahalanobis', 'matching', 'minkowski', 'rogerstanimoto', 'russellrao', 'seuclidean', 'sokalmichener', 'sokalsneath', 'sqeuclidean', 'yule']]


print "start"
print "\n---------------\nSome public service announcements"
#moving parts
pathi=os.path.join("/Users/ps22344/Downloads","craig_0208")


# heres what sklearn ppl do
# Estimated number of clusters: 3
# Homogeneity: 0.953
# Completeness: 0.883
# V-measure: 0.917
# Adjusted Rand Index: 0.952
# Adjusted Mutual Information: 0.883
# Silhouette Coefficient: 0.626

	##	
	###BUILDING VOCAB
	#
	#threshold sets how many times a word needs to occur to be included in the featuredict
def dictmaker(folderlist, threshold=1000):
	#this is our general vocab
	vocab={}
	#collecting words
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
	
	##
	###FINDING CATEGORIES
	#this just extracts the categories from our files
def categorymachine(folderlist):
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

	#
	###BUILDING MATRICES
	#
	

def matrixmachine(folderlist, featuredict, external_category): 
	#matrixmachine takes a list of folders	and of external categories to be included, note that it calls on the category machine 
	print "Starting the matrixmachine"
	wordmatrix=np.empty(shape=(1,len(featuredict)+1))
	print "Matrix initial shape: ", np.shape(wordmatrix)
	# making a dictionary for the categories
	# we need the zero cause the machine returns 2 items
	catdicti=categorymachine(folderlist)[0]
	for folder in folderlist:
		filis=[i for i in os.listdir(os.path.join(pathi, folder)) if not i.startswith(".")]
		print "Building matrices: we have {} files in folder {}".format(len(filis), folder)
		for fili in filis:
			inputfile=codecs.open(os.path.join(pathi, folder, fili), "r", "utf-8").read()
			#establish category
			cat=catdicti[ct.tagextractor(inputfile, external_category, fili)]
			#collect a dictionary with all lowercased words
			#note that punctuation is still in here
			splittext=nltk.word_tokenize(inputfile)
			# we lowercase
			splittextlo=[i.lower() for i in splittext]
			#number of "words"
			wordcount=float(len(splittextlo))
			# we make the vector for this file
			# this is a per word frequency
			wordvector=np.array([float(cat)]+[float(splittextlo.count(i))/wordcount for i in featuredict])
			#print wordvector
			#we append it to the matrix
			wordmatrix=np.append(wordmatrix, [wordvector], axis=0)
	print "Features of word matrix: shape {}, dtype {}".format(np.shape(wordmatrix), wordmatrix.dtype)
	print "---------------\nEnd of public service announcements\n\n"
	#"In 2D, the first dimension corresponds to rows, the second to columns."
	# we don't look at the first row cause that was just for initialization
	# the one without cats we put into the clustering algorithm
	wordmatrix_without_cat=wordmatrix[1:wordmatrix.shape[0],1:wordmatrix.shape[1]]
	wordmatrix_with_cat=wordmatrix[1:wordmatrix.shape[0],]
	return (wordmatrix_without_cat, wordmatrix_with_cat, catdicti)
	
	
	#
	###CREATING CLUSTERS
	#
	#this makes clusters; takes the dataset (matrix) and the algorithm
	
def clustermachine(matrix, clusters=4):
	#we need a similarity matrix to feed into some of the algos
	similarity_matrix=metrics.pairwise.euclidean_distances(matrix)	
	#meanshift and kmeans take features, others need distance matrixes
	no_of_clusters=range(clusters)	
	result=[]
	t=time.time()
	
	## # 1: kmeans
	model=sklearn.cluster.KMeans(clusters,tol=0)
	clustering=model.fit(matrix)
	centroids=clustering.cluster_centers_
	labels=clustering.labels_
	inertia=clustering.inertia_
	kmeans=ct.Clustering(model, clustering.labels_, clustering.cluster_centers_)
	result.append(kmeans)
	print [i.name for i in result][len(result)-1]
	u=time.time()
	print (u-t)/60
	
# 	## #2: MeanShift, takes forever @  12600, 42
# 	model=sklearn.cluster.MeanShift()
#  	clustering=model.fit(matrix)
#  	centroids=clustering.cluster_centers_
#  	labels=clustering.labels_
#  	meanshift=ct.Clustering(model, clustering.labels_, clustering.cluster_centers_)
#  	result.append(meanshift)
#  	u=time.time()
#  	print [i.name for i in result][len(result)-1]
# 	print (u-t)/60
#  	
#  	# 3: Affinity Propagation, breaks @ 12600, 42
#  	model=sklearn.cluster.AffinityPropagation()
# 	clustering=model.fit(matrix)
# 	centroid_index=model.cluster_centers_indices_
# 	centroids=clustering.cluster_centers_
#  	labels=clustering.labels_
#  	aff_matrix=clustering.affinity_matrix_
#  	its= clustering.n_iter_
#  	affinity=ct.Clustering(model, clustering.labels_, clustering.cluster_centers_)
#  	result.append(affinity)
# 	u=time.time()
#  	print [i.name for i in result][len(result)-1]
# 	print (u-t)/60
# 	
# 	## #4: Spectral clustering
# 	model=sklearn.cluster.SpectralClustering()
# 	clustering=model.fit(matrix)
# 	labels=clustering.labels_
#  	aff_matrix=clustering.affinity_matrix_
#  	spectral= ct.Clustering(model, clustering.labels_)
# 	result.append(spectral)
#  	u=time.time()
#  	print [i.name for i in result][len(result)-1]
# 	print (u-t)/60
#  	
#  	
#  	
# #  	##watch out --------- centroids are indices!!!!!	
# # 	## # 5: DBCASN, eanShift, takes forever @  12600, 42
# 	model=sklearn.cluster.DBSCAN()
# 	clustering=model.fit(matrix)
# 	core_samples=clustering.core_sample_indices_
# 	components=clustering.components_
# 	labels=clustering.labels_
# 	dbscan= ct.Clustering(model, clustering.labels_, clustering.core_sample_indices_)
# 	result.append(dbscan)
# 	u=time.time()
#  	print [i.name for i in result][len(result)-1]
# 	print (u-t)/60
# 	
# 	##GUASSIN DOEs NOT FIT OUR SCHEMA AT THIS POINT
# 	## 6: GAUSSIAN MIXTURE. eh this does not really fit in here
# 	model=sklearn.mixture.GMM()
# 	clustering=model.fit(matrix)
# 	weights=model.weights_
#  	means=model.means_
#  	covars=model.covars_
#  	converged=clustering.converged_	
#  	u=time.time()
#  	result.append(dbscan)
#  	print [i.name for i in result][len(result)-1]
# 	print (u-t)/60
# 	
# 
# 	#These are essentially trees; maybe need a different approach. They are kinda predictive
# 	
# # 	## #7: Agglomerative // Ward Hierarchical 
# 	model=sklearn.cluster.AgglomerativeClustering()
# 	clustering=model.fit(matrix)
# 	labels=clustering.labels_
# 	leaves=clustering.n_leaves_
# 	components=clustering.n_components_
# 	ward= ct.Clustering(model, clustering.labels_)
# 	result.append(ward)
# 	u=time.time()
#  	print [i.name for i in result][len(result)-1]
# 	print (u-t)/60
# 
# 	## #8: Birch Hierarchical 	
# 	model=sklearn.cluster.Birch(threshold=0.025)
# 	clustering=model.fit(matrix)
# 	labels=clustering.labels_
# 	root=clustering.root_
# 	subcluster_labels=clustering.subcluster_labels_
# 	birch= ct.Clustering(model, clustering.labels_)
# 	result.append(birch)
# 	u=time.time()
#  	print [i.name for i in result][len(result)-1]
# 	print (u-t)/60
	
	return(result)
	
	
	#######MAIN#########


	 
def main():
	starttime=time.time()
	folders=[i for i in os.listdir(pathi) if not i.startswith(".")]
	print ", ".join(folders)
	print ", ".join([str(len(os.listdir(os.path.join(pathi,f)))) for f in folders])
	folders=['files9_output_0102']#, 'files9_output_0102', 'files9_output_0102', 'files9_output_0102','files9_output_0102', 'files9_output_0102','files9_output_0102', 'files9_output_0102', 'files9_output_0102'] 
	print "We have {} folders".format(len(folders))
	featuredict=dictmaker(folders, 5000)
	wordmatrix_without_cat, wordmatrix_with_cat, catdicti = matrixmachine(folders, featuredict, "category1")
	#self.matrix_with_cats=matrix_with_cats  #data frame including "gold labels"
	#self.matrix_without_cats=matrix_with_cats[:,1:] #data frame without "gold labels"
	x=clustermachine(wordmatrix_without_cat,2)
	print [(i.name, i.no_of_clusters) for i in x]
	#print [i.name for i in x]
	excludelist=['total','no_of_categories', 'no_of_clusters', 'no_of_cats']
	for clustering in x:
		cati=ct.Categorystats(wordmatrix_with_cat, clustering.name, clustering.labels)
		sili=ct.Clusteringstats(wordmatrix_with_cat, clustering.name, clustering.labels).cluster_silhouette()
	# 	print cati.size_of_categories()
		
	
	 	print "\n\n-----------\n\nClustering called {} has {} clusters". format(clustering.getname()[0], clustering.no_of_clusters)
 		print "Its silhouette score is {}".format(str(sili))
		stats=ct.Clusteringstats(wordmatrix_with_cat, clustering.name, clustering.labels).size_of_clusters()
		catstats=ct.Clusteringstats(wordmatrix_with_cat, clustering.name, clustering.labels).cats_per_cluster()
		for cluster in stats:
			print "\nCluster {} contains {} items, {} % of the total".format(cluster, stats[cluster], round(float(stats[cluster])/len(wordmatrix_without_cat)*100))
			for cat in [i for i in catstats[cluster] if not i in excludelist]:
				print "{} items of category {} make up {} % of this cluster".format(catstats[cluster][cat], "".join([i[0] for i in catdicti.items() if i[1] == int(cat)]), round(catstats[cluster][cat]/catstats[cluster]['total']*100))
		cats=ct.Categorystats(wordmatrix_with_cat, clustering.name, clustering.labels).size_of_categories()
		print "\n\n-----------\n\nStatistics per category"
		for cat in [i for i in cats if not i in excludelist]:
			print "\nCategory {} has {} items".format("".join([i[0] for i in catdicti.items() if i[1] == int(cat)]), cats[cat]['total'])
			for entry in [i for i in cats[cat]['cat_per_cluster'] if not i in excludelist]:
				print "{} items or {} percent in cluster {}".format(cats[cat]['cat_per_cluster'][entry], round(float(cats[cat]['cat_per_cluster'][entry])/float(cats[cat]['total'])*100), entry)

		print "\n\n-----------\n\nStronly predictive features are"
		cents=ct.Centroidstats(clustering.name, clustering.labels, clustering.centroids).cluster_predictors(featuredict)
		for diff in cents:
			print "\n Raw Scores"
			print "{} differentiate {} and {}\n".format(", ".join([" : ".join(map(str, i[::-1])) for i in cents[diff]['raw_diff']]), diff[0], diff[1]) 
			print "Zscores"
			print "{} differentiate {} and {}".format(", ".join([" : ".join(map(str, i[::-1])) for i in cents[diff]['zscores_diff']]), diff[0], diff[1])
		"We can also add equivalent features if we want"
		"And stems and whatnot"
		
		
		print "\n\n-----------\n\nHere is a typical document for each cluster"
	endtime=time.time()
	process=endtime-starttime
	print "This took us {} minutes".format(process/60)
		#or do we want to do predictive features and typical document per cluster as well????
		
		
#	print "\n\n-----------\n\nComparing clusterings"
# 		
# 	input=[(str(type(i.name)).split(".")[3].rstrip("'>"), i) for i in x]
# 	simi=ct.Clusteringsimilarity(wordmatrix_with_cat, input)
# 	options=['adjustedrand_sim', 'adjustedmutualinfo_sim', 'jaccard_sim', 'v_sim', 'completeness_sim', 'homogeneity_sim', 'silhouette_score_sim']
# 	for o in options:
# 		print "\n---\n"
# 		ct.Clusteringsimilarity(wordmatrix_with_cat, input).similarity_matrix(o)
# 	endtime=time.time()
# 	print "This took us {} minutes".format((endtime-starttime)/60)
# 	#t=str(type(i.name)).split("."))[3].rstrip("'>")
# 	
	
	
main()



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
		
			
# 	

# 		
# #

# 		
# 		
# 		
# 		
# 		
# 		
# 		
# 		
# 		
# #
# ###DISPERSION
# #
# # How good are our clusters?
# # maybe just calculate the square of the distance to the centroid, then sum
# # ??
# # then average out per data point
# # look at real outliers (more than 2 stdevs)
# 
# #in this distancedict, we collect the indexes for each cluster 
# #that way we can access the actual data points
# distancedict=defaultdict(list)
# for item in labellist_enum:
# 	#establish index numbers for each cluster
# 	#items are (index, value). thus: item[0] - index, item[1]-cluster
# 	distancedict[item[1]].append(item[0])
# 
# print "\n---------------\nThe dispersion of clusters:\n"
# 
# # print distancedict[1]
# for c in clusters:
# 	print "CLUSTER ",c, ":"
# 	centroid_by_cluster=centroids[c]
# 	wordmatrix_by_cluster=[wordmatrix_without_cat[i] for i in distancedict[c]]
# 	difference=[pow((np.array(centroid_by_cluster) - np.array(i)),2) for i in wordmatrix_by_cluster]
# 	# print wordmatrix_by_cluster[0][:3]
# # 	print centroid_by_cluster[:3]
# # 	print difference[0][:3]
# 	totaldifference=sum([sum(i) for i in difference])
# 	meantotaldifference= totaldifference/len(wordmatrix_by_cluster)
# 	print "Total difference is {} for {} data points, mean difference: {}".format(
# 	round(totaldifference), 
# 	len(wordmatrix_by_cluster),
# 	round(meantotaldifference*1000))
# 	print "\n---\n"
# 	
# 	
# #
# ###PREDICTORS
# #
# #which words drive our clusters?
# # we have a number of centroids == len(clusters)
# #centroids=[x,y,z]
# # for each x,y,z we calculate the range
# # note that we would have to scale them if we dont have per word counts
# # then we have to relate the centroids to the value in the vocab
# # they should have the same index but vocab is a dict
# # but it is fixed; if we do an items(). ?
# #ranges=[range() for c in centroids
# range=np.ptp(centroids, axis=0)	
# #range_with_words=[(i, 
# #note that this was stolen from 
# # http://stackoverflow.com/questions/26984414/efficiently-sorting-a-numpy-array-in-descending-order
# # http://stackoverflow.com/questions/14875248/python-numpy-sort-array
# sorted_range= np.sort(range)[::-1]
# sorted_range_index=np.argsort(range)[::-1]
# print "range", range
# print "sorted range", sorted_range
# print "indexes", sorted_range_index
# print "original keys", featuredict.keys()
# print "original items", featuredict.items()
# sorted_range_keys=[featuredict.keys()[i] for i in sorted_range_index]
# sorted_range_values=[float(featuredict.values()[i]) for i in sorted_range_index]
# sorted_range_ranges=[range[i] for i in sorted_range_index]
# sorted_range_centroids=[centroids[:,i].tolist() for i in sorted_range_index]
# #flattened = [val for sublist in list_of_lists for val in sublist]
# 
# 
# #t=[i[0] for i in sorted_range_centroids for i in [l] ]	
# # t=[entry[0] for entry in i for l in sorted_range_centroids]
# 		
# # print "the keys", sorted_range_keys
# # print "the values", sorted_range_values
# # print "the ranges", sorted_range_ranges
# print "the original range", sorted_range_centroids
# 
# #now that were doing it this way, we could have sorted on the list in the first place
# #but its whatevs at this point
# result=zip(sorted_range_ranges, sorted_range_centroids, sorted_range_keys, sorted_range_values)
# print "result", result
# 
# endtime=time.time()
# print "Finished. the threshold was {}, this took us {} minutes".format(threshold, (endtime - starttime)/60)
# 
# #exclude too low categories
# #express as: percentage of category, percentage of cluster, distance from centroid