import re, os, numpy as np, scipy, itertools, sklearn
from collections import defaultdict




class Clustering(object):
	"""collect basic features of a clustering"""

	def __init__(self, matrix_with_cats, name, labels , centroids=None, actual_centroids=None):
		self.matrix_with_cats=matrix_with_cats  #data frame including "gold labels"
		self.matrix_without_cats=matrix_with_cats[:,1:] #data frame without "gold labels"
		self.name=type(name) #the clustering algorithm we are dealing with
		self.labels=labels #the array of labels: label for each data point
		self.centroids=centroids #the centroids or prototypes if applicable. WATCH:: INDEXES OR ACTUAL????
		self.actual_centroids=actual_centroids #what is this relevant for??
		self.no_of_clusters=len(np.unique(labels)) #how many clusters this algorithm came up with
		self.silhouette=sklearn.metrics.silhouette_score(self.matrix_without_cats, self.labels)
	
	def getName(self):  
		return self.name  #why do we need this??
		
	def _clusterdictmaker(self, matrix_without_cats):
		#in the clusterdicti, we collect for each cluster the data points contained
		# output is a dictionary with ACTUAL vectors
		# why don't we feed it the self.matrix?
		iterator=range(self.no_of_clusters)
		clusterdicti=defaultdict()
		for cluster in iterator:
			#give me indexes of label array where cluster is true	
			#note that where returns a cluster that is always len 1
			# we are interested in l[0]
			#clusterdicti[cluster]=np.where(self.labels==cluster)[0]
			clusterdicti[cluster]=np.array([self.matrix_without_cats[i] for i in np.where(self.labels==cluster)[0]])
		return clusterdicti

	def _clustercatdictmaker(self, matrix_with_cats):
		#in this dicti, we collect for each cluster the items per category
		# output is a dictionary of ACTUAL vectors
		#structure: { cluster: {cat1: ...., cat2:..., cat3:....}, cluster2: {....}
		# why don't we feed it the self.matrix?
		iterator=range(self.no_of_clusters)
		clustercatdicti=defaultdict()
		for cluster in iterator:
			clustercatdicti[cluster]=defaultdict(list)
			#note that where returns a cluster that is always len 1 --> two?
			# we are interested in l[0]
			wordmatrix=[self.matrix_with_cats[i] for i in np.where(self.labels==cluster)[0]]
			for item in wordmatrix:
				clustercatdicti[cluster][item[0]].append(item)
		return clustercatdicti



class Clusteringstats(Clustering):
	"""basic statistics of a clustering"""
	
	def __init__(self, matrix_with_cats, name, labels , centroids=None, actual_centroids=None): 
		Clustering.__init__(self, matrix_with_cats, name, labels , centroids=None, actual_centroids=None)
			
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
		#how spread out is the cluster? ## cluster or clustering???
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




# remember that we could use z scores		
class Centroidstats(Clustering):

	"""statistics and calculations with centroids within a clustering"""
			
	def __init__(self, dataframe, name, labels,centroids=None, actual_centroids=None):
		Clustering.__init__(self, dataframe, name, labels, centroids, actual_centroids)
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
		'raw_diff':[],
		'zscores_diff':[]
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
			predictdicti[tup[0]]['raw_diff'].append(raw_dist)
		for tup in sorted_zscores:
			index=tup[2]
			sorted_diffs=tup[1][index][::-1]
			sorted_vocab=arrayed_vocab[index][::-1]
			raw_dist=zip(sorted_diffs, sorted_vocab)
			predictdicti[tup[0]]['zscores_diff'].append(raw_dist)
		return predictdicti
		


class Partitionsimilarity(Clustering):

	""" Calculates similarity measures between clusterings for cluster comparison. """

	def __init__(self, partition1, partition2): 
			# we treat the part 1 labels as gold standard for now
			self.part1_name=partition1.name
			self.part2_name=partition1.name
			self.part1_labels=partition1.labels
			self.part2_labels=partition2.labels
			self.part1_features=partition1.matrix_without_cats
			self.part2_features=partition2.matrix_without_cats
			self.part1_clusters=range(partition1.no_of_clusters)
			self.part2_clusters= range(partition2.no_of_clusters)
	
	def partition_features(self):		
	#takes the labels (and features, depending on metric) of two partitions and compares
	#returns dict with different metrics for each combination
	# note we need a different combo here cause comparing same numbers is a thing
		similaritydict={}
		similaritydict[(self.part1_name, self.part2_name)]={
		
			'adjustedrand_sim': sklearn.metrics.adjusted_rand_score(self.part1_labels, self.part2_labels),
			'adjustedmutualinfo_sim':sklearn.metrics.adjusted_mutual_info_score(self.part1_labels, self.part2_labels),
			'jaccard_sim': sklearn.metrics.jaccard_similarity_score(self.part1_labels, self.part2_labels),
			#This score is identical to normalized_mutual_info_score:
			'v_sim': sklearn.metrics.v_measure_score(self.part1_labels, self.part2_labels),
			'completeness_sim': sklearn.metrics.completeness_score(self.part1_labels, self.part2_labels),
			'homogeneity_sim':sklearn.metrics.homogeneity_score(self.part1_labels, self.part2_labels),
			'silhouette_score_sim': (sklearn.metrics.silhouette_score(self.part1_features, self.part1_labels), sklearn.metrics.silhouette_score(self.part2_features, self.part2_labels)),
			'variation_of_information':'is in R'
		}
		print similaritydict
		print len(sklearn.metrics.silhouette_samples(self.part1_features, self.part1_labels))
		
	def confusion_matrix_maker(self):
		return "assi"
	# this takes the results of partition features and presents them in a way that makes sense


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
