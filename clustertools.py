import re, os, numpy as np, scipy, itertools, sklearn
from collections import defaultdict




class Clustering(object):
	"""collect basic features of a clustering"""

	def __init__(self, name, labels , centroids=None, actual_centroids=None):
		self.name=name #the clustering algorithm we are dealing with
		self.labels=labels #the array of labels: label for each data point
		self.centroids=centroids #the centroids or prototypes if applicable. WATCH:: INDEXES OR ACTUAL????
		self.actual_centroids=actual_centroids #what is this relevant for??
		self.no_of_clusters=len(np.unique(labels)) #how many clusters this algorithm came up with

	
	def getname(self):  
		return type(self.name), self.name  
		
	def _clusterdictmaker(self, matrix_without_cats):
		#in the clusterdicti, we collect for each cluster the data points contained
		# output is a dictionary with ACTUAL vectors
		iterator=range(self.no_of_clusters)
		clusterdicti=defaultdict()
		for cluster in iterator:
			#give me indexes of label array where cluster is true	
			#note that where returns a cluster that is always len 1
			# we are interested in l[0]
			clusterdicti[cluster]=np.array([matrix_without_cats[i] for i in np.where(self.labels==cluster)[0]])
		return clusterdicti

	def _clustercatdictmaker(self, matrix_with_cats):
		#in this dicti, we collect for each cluster the items per category
		# output is a dictionary of ACTUAL vectors
		#structure: { clustercatdicti: {cat1: ...., cat2:..., cat3:....}, cluster2: {....}
		# why don't we feed it the self.matrix?
		iterator=range(self.no_of_clusters)
		clustercatdicti=defaultdict()
		for cluster in iterator:
			clustercatdicti[cluster]=defaultdict(list)
			#note that where returns a cluster that is always len 1 --> two?
			# we are interested in l[0]
			wordmatrix=[matrix_with_cats[i] for i in np.where(self.labels==cluster)[0]]
			for item in wordmatrix:
				clustercatdicti[cluster][item[0]].append(item)
		return clustercatdicti



class Clusteringstats(Clustering):
	"""basic statistics of a clustering"""
	
	def __init__(self, matrix_with_cats, name, labels , centroids=None, actual_centroids=None): 
		Clustering.__init__(self, name, labels , centroids=None, actual_centroids=None)
		self.matrix_with_cats=matrix_with_cats
		self.matrix_without_cats=matrix_with_cats[:,1:]
			
	def size_of_clusters(self):
		#how many items in each cluster?
		# returns dictionary {cluster:size, cluster:size ...}	
		dict=self._clusterdictmaker(self.matrix_without_cats)
		return {k:len(dict[k]) for k in dict}

	def cats_per_cluster(self):
		#how many categories in each cluster?
		# output structure: {cluster: { categ x: N, cat y: N, total: x=y, no_of_categories: len[x,y]}	
		dict=self._clustercatdictmaker(self.matrix_with_cats)
		cluster_features=defaultdict()
		for i in dict:
			cluster_features[i]={k:float(len(v)) for k,v in dict[i].items()}
			cluster_features[i]['total']=sum(cluster_features[i].values())
			cluster_features[i]['no_of_categories']=len(dict[i])
		return cluster_features
		
	def cluster_features(self):
		#how spread out is each cluster? 
		# returns dictionary of basic stats
		featuredicti=defaultdict()
		dict=self._clusterdictmaker(self.matrix_without_cats)
		zscoredict={k:scipy.stats.mstats.zscore(dict[k], axis=0, ddof = 1) for k in dict.keys()} #setting  "ddof = 1" so we get the same output as in R
		silhouette=sklearn.metrics.silhouette_samples(self.matrix_without_cats, self.labels)
		# iterate over clusters
		for i in dict:
			featuredicti[i]={
			'mean':np.mean(dict[i], axis=0), #mean of column
			'median':np.median(dict[i], axis=0), #median of column
			'std':np.std(dict[i], axis=0,ddof = 1 ), #setting  "ddof = 1" so we get the same output as in R
			'var':np.var(dict[i], axis=0), #variance of column
			'range':np.ptp(dict[i], axis=0), #range of column, raw scores
			'zscore_range':np.ptp(zscoredict[i], axis=0), #range of column, zscores
			'silhouette_score': silhouette[np.where(self.labels==i)],
			#this is still very under development
			'feature_correlation':np.corrcoef(dict[i], rowvar=0) #feature correlation over rows
			} 
		return featuredicti

	def cluster_silhouette(self):
		silhouette=sklearn.metrics.silhouette_score(self.matrix_without_cats, self.labels)
		return silhouette


# remember that we could use z scores		
class Centroidstats(Clustering):

	"""statistics and calculations with centroids within a clustering"""
			
	def __init__(self, name, labels,centroids=None, actual_centroids=None):
		Clustering.__init__(self, name, labels, centroids, actual_centroids)
		#relevant here: centroids and actual centroids
		#centroid will be a vector of len (x)
		
	def _centroid_check(self):
		if self.centroids == None:
			print "Model {} has no centroids".format(self.name)
			return False
		else:
			pass
			
	def _centroiddictmaker(self):
		#returns a dictionary pairing clusters with centroids
		# structure: {cluster:vector_of_centorids, cluster2: ....}
		centroiddicti=defaultdict()
		#lets not get tripped up by models without centroids
		if self._centroid_check()==False:
			return None
		else:
			for i in range(self.no_of_clusters):
				centroiddicti[i]=self.centroids[i]
			return centroiddicti
	
	#do we want it here or its own thing
# 	def central_documents (self):
# 		#for actual vectors: find doc closest to the centroid
# 		
# 		# for indexes: just look it up in matrix, get row line
# 		# do we write the filename into the matrix with cats??
# 		# we should add a setting where we can set the length of external factors
# 		# external=3 --> 	self.matrix_without_cats=matrix_with_cats[:,external:]	
# 		# we should coordinate that with the catdicti maker
# 		for centroid in centroids:
# 			centroid - item = abs(difference)
# 				#apply to whole matrix_without_cats, should work in numpy
# 				#sum and smallest row wins
# 			# get the matching row in matrix_with_cats
# # 			open the file, print out 
				
				
			
	def distance_between_centroids(self):
		if self._centroid_check()==False:
			return None
		#calculate distance btw centroids
		#returns a dictionary pairing cluster pairs and distances in various measurement methods
		# structure: {cluster_to_cluster2:{hamming_dist:x, euclid_dist:y ....} (vector of dists??), cluster_to_cluster3: ....}	
		centroiddicti=self._centroiddictmaker()
		distdicti=defaultdict()
		for combo in itertools.combinations(centroiddicti.keys(), 2):
			distdicti[combo]={
			'raw_dist':sum(pow(centroiddicti[combo[0]]-centroiddicti[combo[1]], 2)),
			'manhattan_dist':scipy.spatial.distance.cityblock(centroiddicti[combo[0]],centroiddicti[combo[1]]),
			'euclid_dist':scipy.spatial.distance.euclidean(centroiddicti[combo[0]],centroiddicti[combo[1]]),
			#"[Cosine] is thus a judgement of orientation and not magnitude"
			'cosine_dist':scipy.spatial.distance.cosine(centroiddicti[combo[0]],centroiddicti[combo[1]]),
			'minkowski_dist':scipy.spatial.distance.minkowski(centroiddicti[combo[0]],centroiddicti[combo[1]], 3),
			'correlation_dist':scipy.spatial.distance.cosine(centroiddicti[combo[0]],centroiddicti[combo[1]])
			}
		return distdicti		
	
	def _differencemaker(self, dict_of_values):
		# takes a dictionary of what??, collects differences between all entries
		# returns tuple (entries compared, index of sorted vector)
		sorted=[]
		for combo in itertools.combinations(dict_of_values.keys(), 2):
			diff=dict_of_values[combo[0]]-dict_of_values[combo[1]]
			absolute_diff=abs(diff)
			#note that sorted is an index array
			# we return (comparison pair, differences, array of sorted indexes)
			sorted.append((combo,  diff, np.argsort(absolute_diff)))
			# we can apply this to the original difference vector; then we turn that one around
			# same then for vocab
		#print sorted
		return sorted
	
		
	def cluster_predictors(self, vocab_used_for_feature_extraction):
		# takes a dictionaty of centroids and a dictionary of vocab to compute
		# the features most predictive of each cluster
		# returns dictionary { cluster: {raw_diff:(word X,difference score), (word Y, difference score) ..., zscores_diff: ()()}, cluster2: {...}}
		centroiddicti=self._centroiddictmaker()
		# we take the words out of the dictionary supplied & make it into an array
		vocab=vocab_used_for_feature_extraction.keys()
		arrayed_vocab=np.array(vocab)
		
		# wouldn't we need the whole dataset for z scores to make sense
		zscoredicti={k:scipy.stats.mstats.zscore(centroiddicti[k], axis=0, ddof = 1) for k in centroiddicti.keys()} #setting  "ddof = 1" so we get the same output as in R
		predictdicti=defaultdict()
		# sorting our vectors of interest	
		sorted_values=self._differencemaker(centroiddicti)
		sorted_zscores=self._differencemaker(zscoredicti)
		#building an empty dict
		predictdicti={tup[0]:{
		'raw_diff':None,
		'zscores_diff':None
		} 
		for tup in sorted_values}
		
		# "In other words, a[index_array] yields a sorted a."
		# filling the dict
		for tup in sorted_values:
			index=tup[2]
			#sort by index, then reverse so largest values first
			sorted_diffs=tup[1][index][::-1]
			sorted_vocab=arrayed_vocab[index][::-1]
			raw_dist=zip(sorted_diffs, sorted_vocab)
			predictdicti[tup[0]]['raw_diff']=raw_dist
		for tup in sorted_zscores:
			index=tup[2]
			sorted_diffs=tup[1][index][::-1]
			sorted_vocab=arrayed_vocab[index][::-1]
			zscore_dist=zip(sorted_diffs, sorted_vocab)
			predictdicti[tup[0]]['zscores_diff']=zscore_dist
		return predictdicti
		


class Clusteringsimilarity(Clustering):

	""" Calculates similarity measures between clusterings for cluster comparison. """

	def __init__(self, matrix_with_cats, models): 
		#partitionings consists of model name and model out of the list of tuples input into models
		self.partitionings=dict((k, v) for k, v in models)
		self.matrix_without_cats=matrix_with_cats[:,1:]
			
	def get_variables(self, key):
		return self.partitionings.get(key, None)
	
	def set_variables(self, key, value):
		self.partitionings[key]=value
		
	def _partitionsimilarity_dictmaker(self):		
		# for item in self.partitionings:
		print self.partitionings[item].name
		matrix_without_cats=self.matrix_without_cats
		similaritydict={}
		# all possible combinations between models
		for combo in itertools.combinations(self.partitionings.keys(),2):
			similaritydict[(combo[0], combo[1])]={
		
			'adjustedrand_sim': sklearn.metrics.adjusted_rand_score(self.partitionings[combo[0]].labels, self.partitionings[combo[1]].labels),
			'adjustedmutualinfo_sim':sklearn.metrics.adjusted_mutual_info_score(self.partitionings[combo[0]].labels, self.partitionings[combo[1]].labels),
			'jaccard_sim': sklearn.metrics.jaccard_similarity_score(self.partitionings[combo[0]].labels, self.partitionings[combo[1]].labels),
			#This score is identical to normalized_mutual_info_score:
			'v_sim': sklearn.metrics.v_measure_score(self.partitionings[combo[0]].labels, self.partitionings[combo[1]].labels),
			'completeness_sim': sklearn.metrics.completeness_score(self.partitionings[combo[0]].labels, self.partitionings[combo[1]].labels),
			'homogeneity_sim':sklearn.metrics.homogeneity_score(self.partitionings[combo[0]].labels, self.partitionings[combo[1]].labels),
			#double check this silhouette score. how do we get the matrix without in here???
			'silhouette_score_sim': (sklearn.metrics.silhouette_score(self.matrix_without_cats, self.partitionings[combo[0]].labels), sklearn.metrics.silhouette_score(self.matrix_without_cats, self.partitionings[combo[1]].labels)),
			'variation_of_information':'is in R'
		}
		return similaritydict

	def similarity_matrix(self, metric):
		# this prints out a correlation matrix-style comparison of clusterings. 
		# metric is the metric to use, e.g. one of the entries in the dictionary
		# returned by self._partitionsimilarity_dictmaker
		dict=self._partitionsimilarity_dictmaker()
		entries=dict.items()
		column_names=[i[0][0] for i in entries]		
		column_names = list(set(column_names))
		row_names=column_names.reverse()
		# http://stackoverflow.com/questions/36773329/creating-correlation-matrix-style-table-in-python
		column_names=list(set([i[0][0] for i in entries]))
		row_names=list(set([i[0][1] for i in entries]))
		coltemplate="\t{:<25}"*len(column_names)
		print "Metric: ", metric
		print "{:25}".format(" "), coltemplate.format(*column_names)
		for r in row_names:
			result=[]
			for c in column_names:
				if c == r:
					result.append("***")
				elif dict.get((c,r), None) == None:
					result.append(dict[(r,c)].get(metric, "***"))
				else:
					result.append(dict[(c,r)].get(metric, "SERIOUS ERROR"))
			result=[str(i) for i in result]
			rowtemplate="\t{:25}"*len(result)
			print "{:>25}".format(r), rowtemplate.format(*result)


	def clustering_quality(self):
		# returns Silhouette score for each clustering
		qualitydict={}
		for key in self.partitionings.keys():
			qualitydict[key]=sklearn.metrics.silhouette_score(self.matrix_without_cats, self.partitionings[key].labels)
		return qualitydict
		
		


class Categorystats(Clustering):
	"""basic statistics of categories within a clustering"""
	
	def __init__(self, matrix_with_cats, name, labels , centroids=None, actual_centroids=None): 
		Clustering.__init__(self, name, labels , centroids=None, actual_centroids=None)
		self.matrix_without_cats=matrix_with_cats[:,1:]
		self.matrix_with_cats=matrix_with_cats
			
			
	
	#get item per category and how spread out over clusters
	
	def size_of_categories(self):
		#returns the number of categories, and how they are spread out over clusters
		# format dict{cat 1: {cluster 0: x, cluster 1: y, ...}, cat 2: {}
		dict=self._clustercatdictmaker(self.matrix_with_cats)
		cats=[dict[cluster].keys() for cluster in dict]
		#flattening a list a la http://stackoverflow.com/questions/406121/flattening-a-shallow-list-in-python
		cats=set(list(itertools.chain.from_iterable(cats)))
		cat_features={
			'no_of_cats': len(cats),
			'no_of_clusters': len(dict.keys())
			}
			# total returns the number of item in each category}
		for item in cats:
			cat_features[item]= {
			'total': sum([len(dict[i][item]) for i in dict.keys() if item in dict[i].keys()]),
			# is a dictionary {cluster1: n, cluster2:n,...}
			'cat_per_cluster': {i: len(dict[i][item]) for i in dict.keys() if item in dict[i].keys()}
			}		
		return cat_features
		


#
###FUNCTIONS
##

#setting up some helper functions
def tagextractor(text, tag, fili):
    regexstring="<"+tag+"=(.*?)>"
    result=re.findall(regexstring, text, re.DOTALL)
    if len(result) != 1:
        print "alarm in tagextractor", fili, result
    return result[0]
    
def adtextextractor(text, fili):
    regexstring="<text>(.*?)</text>"
    result=re.findall(regexstring, text, re.DOTALL)
    if len(result) != 1:
        print "alarm in adtextextractor", fili, result
    return result[0]
