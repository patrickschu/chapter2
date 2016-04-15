import clustertools as ct 
import os, re, shutil,string,numpy,nltk,codecs, scipy, scipy.cluster, numpy as np, time, sklearn
from sklearn import cluster, mixture, metrics
from collections import defaultdict
from nltk.tokenize import word_tokenize
# read the clustering documentation here: 
# http://docs.scipy.org/doc/scipy-0.14.0/reference/generated/scipy.cluster.vq.kmeans2.html




print "start"
starttime=time.time()
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


#
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





#
##FINDING CATEGOIRES
#this just extracts the categories from our files
def categorymachine(folderlist):
	print folderlist
	catdicti={}
	catnumber=0
	for folder in folderlist:
		filis=os.listdir(os.path.join(pathi,folder))
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

# for c in clusters:
#     print "For cluster {} there are {} items".format(c, labellist.count(c))
    
#check out the groups within in each cluster



	#
	###BUILDING MATRICES
	#
#matrixmachine takes a list of folders	and of external categories to be included
#note that it calls on the category machine

def matrixmachine(folderlist, featuredict, external_category): 
	#constructing matrix
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
def clustermachine(matrix, algorithm, clusters=4):
	
	#we need a similarity matrix
	similarity_matrix=metrics.pairwise.euclidean_distances(matrix)	

	#meanshift and kmeans take features
	#others need distance matrixes
	no_of_clusters=range(clusters)
	
	result=[]
	
	## # 1: kmeans
	model=sklearn.cluster.KMeans(clusters)
	clustering=model.fit(matrix)
	centroids=clustering.cluster_centers_
	labels=clustering.labels_
	inertia=clustering.inertia_
	kmeans=ct.Cluster(matrix, model, clustering.labels_, clustering.cluster_centers_)
	result.append(kmeans)
	
# 	## #2: MeanShift
#  	model=sklearn.cluster.MeanShift()
#  	clustering=model.fit(matrix)
# 	centroids=clustering.cluster_centers_
#  	labels=clustering.labels_
#  	meanshift=ct.Cluster(matrix, model, clustering.labels_, clustering.cluster_centers_)
# 	result.append(meanshift)
# 	
# 	## #3: Affinity Propagation
# 	model=sklearn.cluster.AffinityPropagation()
# 	clustering=model.fit(similarity_matrix)
# 	centroid_index=model.cluster_centers_indices_
# 	centroids=clustering.cluster_centers_
#  	labels=clustering.labels_
#  	aff_matrix=clustering.affinity_matrix_
#  	its= clustering.n_iter_
#  	affinity=ct.Cluster(matrix, model, clustering.labels_, clustering.cluster_centers_)
#  	result.append(affinity)
	
# 	## #4: Spectral clustering
# 	model=sklearn.cluster.SpectralClustering()
# 	clustering=model.fit(similarity_matrix)
# 	labels=clustering.labels_
#  	aff_matrix=clustering.affinity_matrix_
#  	spectral= ct.Cluster(matrix, model, clustering.labels_)
# 	result.append(spectral)
#  	
#  	 ##watch out --------- centroids are indices!!!!!	
# 	## # 5: DBCASN
# 	model=sklearn.cluster.DBSCAN()
# 	clustering=model.fit(matrix)
# 	core_samples=clustering.core_sample_indices_
# 	components=clustering.components_
# 	labels=clustering.labels_
# 	dbscan= ct.Cluster(matrix, model, clustering.labels_, clustering.core_sample_indices_)
# 	result.append(dbscan)
# 	
	##GUASSIN DOEs NOT FIT OUR SCHEMA AT THIS POINT
	
	
	## 6: GAUSSIAN MIXTURE. eh this does not really fit in here
	model=sklearn.mixture.GMM()
	clustering=model.fit(matrix)
	weights=model.weights_
 	means=model.means_
 	covars=model.covars_
	converged=clustering.converged_	

	#These are essentially trees; maybe need a different approach. 
	#They are kinda predictive
	
	## #7: Agglomerative // Ward Hierarchical 
	model=sklearn.cluster.AgglomerativeClustering()
# 	clustering=model.fit(matrix)
# 	labels=clustering.labels_
# 	leaves=clustering.n_leaves_
# 	components=clustering.n_components_
# 	ward= ct.Cluster(matrix, model, clustering.labels_)
# 	result.append(ward)
# 
# 	## #8: Birch Hierarchical 	
# 	model=sklearn.cluster.Birch(threshold=0.025)
# 	clustering=model.fit(matrix)
# 	labels=clustering.labels_
# 	root=clustering.root_
# 	subcluster_labels=clustering.subcluster_labels_
# 	birch= ct.Cluster(matrix, model, clustering.labels_)
# 	result.append(birch)
	
	return(result)
	
	
	


	#
	###CALCULALTING CLUSTERSTATS
	#
#cat_threshold indicates how many times we need to see a category for it to be included in the stats
# def statsmachine(labellist, matrix_with_cat, catdict, cat_threshold=100):
# 
# 	#STATS PER CLUSTER FIRST
# 	print "\n---------------\nThe makeup of clusters:\n"
# 	# we connect labels to category of entry
# 	# remember that labellist consists of tuples where i[0] is the 
# 	# cluster label and i[1] the index, [2] the actual vector
# 
# 	#clustercounts collects a list with the items for each cluster
# 	clustercounts=defaultdict(list)
# 	#the lenght of the lists tells us the size of the cluster
# 	# later on, we can use the items to determine the makeup of the cluster
# 	# clustercounts looks like this {0:[1,1,1,1,2,1,1,2 ...], 1: [2,2,0,0,0,2...]}
# 	for i in labellist:
# 		clustercounts[i[0]].append(matrix_with_cat[i[1],0])
# 	#clusterstats contains the statistics of each cluster
# 	#is makes a sub dict for each cluster:
# 	#CLUSTER: {cat1: {count:x, alias:x}, cat2: {ibid}...}
# 	#e.g. 0 {u'w4w': {'count': 111, 'percentage': 32.080924855491325, 'code': 5}, u'm4w': {'count': 6 ...
# 		clusterstats=defaultdict()
# 	for i in clustercounts:
# 		print "Cluster {} contains {} items".format(i, len(clustercounts[i]))
# 		
# 		clusterstats[i]={c: {
# 		'code':catdict[c],
# 		'count':clustercounts[i].count(catdict[c]),
# 		'percentage':float(clustercounts[i].count(catdict[c]))/len(clustercounts[i])*100
# 		} 
# 		for c in catdict}
# 
# 	print "\n---------------\nThe stats of clusters:\n"
# 	for i in clusterstats:
# 		print "CLUSTER ",i, ":"
# 		for c in clusterstats[i]:
# 			if clusterstats[i][c]['count'] > cat_threshold:
# 				print "category {:>5}, coded as {:>3}: {:>4} items, or {:>4} percent of the cluster".format(
# 				c,
# 				clusterstats[i][c]['code'],
# 				clusterstats[i][c]['count'],
# 				round(clusterstats[i][c]['percentage'])
# 				)
# 		print "\n---\n"
# 	#	
# 	#NOW STATS PER CATEGORY	
# 	#
# 	catstats=defaultdict()
# 	#for each cat in the catdicti, we collect the total count
# 	for i in catdict:
# 		catstats[i]={str(c): clusterstats[c][i]['count'] for c in clusterstats}
# 		catstats[i]['total']=sum(catstats[i].values())
# 	print "\n---------------\nThe stats of categories:\n"
# 	for i in catstats:	
# 		if catstats[i]['total'] > cat_threshold:
# 			print "CATEGORY ",i.upper(), ":"
# 			for c in clusterstats:
# 				c=str(c)
# 				print "cluster {:>2} contains {:>5} out of {:>5} items in this category, or {:>4} percent of the total".format(
# 				c,
# 				catstats[i][c], 
# 				catstats[i]['total'],
# 				round(float(catstats[i][c])/catstats[i]['total']*100)
# 				)
# 			print "\n---\n"
	
	#######MAIN#########

class Clusterstats(object):#, matrix_with_cats, catdictionary):
	def __init__(self, model, matrix_with_cats): 
		self.name=model.name
		self.labels=model.labels
		self.matrix_with_cats=matrix_with_cats
		self.no_of_clusters=len(np.unique(model.labels))
		#self.cluster_dict=_dictmaker(self)
	#in this dicti, we collect for each cluster the indexes contained
	def _clusterdictmaker(self):
		iterator=range(self.no_of_clusters)
		clusterdicti=defaultdict()
		for cluster in iterator:
			print "cluster: " ,cluster
			#give me indexes of label array where cluster is true	
			#note that where returns a cluster that i always len 1
			# we are interested in l[0]
			clusterdicti[cluster]=np.where(self.labels==cluster)[0]
	
	def _clustercatdictmaker(self):
		iterator=range(self.no_of_clusters)
		clustercatdicti=defaultdict()
		for cluster in iterator:
			print "cluster: " ,cluster
			#structure: { cluster: {cat1: ...., cat2:..., cat3:....}, cluster2: {....}
			clustercatdicti[cluster]=defaultdict(list)
			#give me indexes of label array where cluster is true	
			#note that where returns a cluster that i always len 1
			# we are interested in l[0]
			# we look these indexes up in the wordmatrix to identify categories
			wordmatrix=[self.matrix_with_cats[i] for i in np.where(self.labels==cluster)[0]]
			for item in wordmatrix:
				clustercatdicti[cluster][item[0]].append(item)
		# for i in clustercatdicti:
# 			print "\n-------\nfirst level, entry:", i, "length", len(clustercatdicti[i])
# 			for t in clustercatdicti[i]:
# 				print  "2nd level entry", t, "length: ", len(clustercatdicti[i][t])
		return clustercatdicti
		
	def size_of_clusters(self):
		dict=self._dictmaker()
		return {k:len(dict[k]) for k in dict}
		
	def cats_per_cluster(self):
		dict=self._clusterdictmaker()
		#returning: how many of each cat in this cluster, percentage of this cluster
		


	
	
	



	
def main():
	folders=[i for i in os.listdir(pathi) if not i.startswith(".")]
	folders=['files9_output_0102']
	print "We have {} folders".format(len(folders))
	featuredict=dictmaker(folders)
	wordmatrix_without_cat, wordmatrix_with_cat, catdicti = matrixmachine(folders, featuredict, "category1")
	x=clustermachine(wordmatrix_without_cat, scipy.cluster.vq.kmeans2)
	f=[(i.name, i.no_of_clusters) for i in x]
	print f
	g=[(i.name, i.centroids) for i in x]
	h=[len(Clusterstats(i, wordmatrix_with_cat)._clustercatdictmaker()) for i in x]
	print "clusterstats says",  h
	# for i in x:
# 		print x.getClusterNumber()
	# #centroids, labels, labellist=clustermachine(wordmatrix_without_cat, scipy.cluster.vq.kmeans2)
# 	print "Centroids and labels established"
# 	stats=statsmachine(labellist, wordmatrix_with_cat, catdicti, 200)
# 	print "finito"



main()


#statsmachine
#clusterstats calculates stats by cluster
# we feed it the labels from the Cluster objects

	

# 			
# 		1. size (len per label)
# 		range(no_of_clusters) 
# 		for i in range(n_0_c) list.count(i)
# 		dicti[i]=list.count(i)
# 	def get_range(self):
# 		print "get range!!"
# 	
# 	def get_percentages(self):
# 		print "get percetnages!!"
	

# distancedict=defaultdict(list)
# 
# for item in labellist_enum:
# 	#establish index numbers for each cluster
# 	#items are (index, value). thus: item[0] - index, item[1]-cluster
# 	distancedict[item[1]].append(item[0])
# 
# print "\n---------------\nThe dispersion of clusters:\n"

##
####NOTES
##

# def categorystats
# def globalstats

## for each, give stats:
# -per cluster:
# 		1. size (len per label)
# 		range(no_of_clusters) 
# 		for i in range(n_0_c) list.count(i)
# 		dicti[i]=list.count(i)
# 		
# 		2. split up btw categories how? (number, percentage) (dict of clusters, len per label)
# 		for i in categories:
# 			get relevant index from matrix with cats, i.e. col 1 is cat
# 			find index in labels (might depend on algo how to do it)
# 			dict[i] cluster 1:
# 					cluster 2:
# 					sum(values) is total
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


