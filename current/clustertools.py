import re
import os
import numpy as np
import scipy
import itertools
import sklearn
import codecs
import json
from collections import defaultdict

scipy_distances=['euclidean', 'minkowski', 'cityblock', 'seuclidean', 'sqeuclidean', 'cosine', 'correlation','hamming', 'jaccard', 'chebyshev', 'canberra', 'braycurtis', 'mahalanobis', 'yule', 'matching', 'dice', 'kulsinski', 'rogerstanimoto', 'russellrao', 'sokalmichener', 'sokalsneath']#, 'wminkowski']


class Clustering(object):
	"""
	Collect features of a clustering, compute basic features.
	"""

	def __init__(self, name, labels , centroids=None, actual_centroids=None):
		self.name=name #the clustering algorithm we are dealing with
		self.labels=labels #the array of labels: label for each data point
		self.centroids=centroids #the centroids or prototypes if applicable. WATCH:: INDEXES OR ACTUAL????
		self.actual_centroids=actual_centroids #what is this relevant for??
		self.no_of_clusters=len(np.unique(labels)) #how many clusters this algorithm came up with

	
	def getname(self):  
		return type(self.name), self.name  
		
	def _clusterdictmaker(self, matrix_without_cats):
		"""
		takes a matrix without labels, returns a dictionary with the vectors / cluster.
		structure: clusterdicti {cluster 0: [[0,1,2], [1,2,2], ...] cluster 1: [], }.
		in the clusterdicti, we collect for each cluster the data points contained.
		output is a dictionary with ACTUAL vectors.
		"""
		iterator=range(self.no_of_clusters)
		clusterdicti=defaultdict()
		for cluster in iterator:
			# note that "where" returns a cluster that is always len = 2, we are interested in l[0]
			clusterdicti[cluster]=np.array([matrix_without_cats[i] for i in np.where(self.labels==cluster)[0]])
		return clusterdicti

	def _clustercatdictmaker(self, matrix_with_cats):
		"""
		takes a matrix with labels, collects the vectors for each label per cluster.
		structure: { clustercatdicti: {cat1: ...., cat2:..., cat3:....}, cluster2: {....}.
		"""
		iterator=range(self.no_of_clusters)
		clustercatdicti=defaultdict()
		for cluster in iterator:
			clustercatdicti[cluster]=defaultdict(list)
			wordmatrix=[matrix_with_cats[i] for i in np.where(self.labels==cluster)[0]]
			for item in wordmatrix:
				clustercatdicti[cluster][item[0]].append(item)
		return clustercatdicti



class Clusteringstats(Clustering):
	"""
	Compute basic statistics of a clustering.
	"""
	
	def __init__(self, matrix_with_cats, matrix_without_cats, name, labels , centroids=None, actual_centroids=None): 
		Clustering.__init__(self, name, labels , centroids=None, actual_centroids=None)
		self.matrix_with_cats=matrix_with_cats
		self.matrix_without_cats=matrix_without_cats		
			
	def size_of_clusters(self):
		#how many items in each cluster? returns dictionary {cluster:size, cluster:size ...}	
		dict=self._clusterdictmaker(self.matrix_without_cats)
		return {k:len(dict[k]) for k in dict}

	def cats_per_cluster(self):
		#how many categories in each cluster? returns dictionary: {cluster: { categ x: N, cat y: N, total: x=y, no_of_categories: len[x,y]}	
		dict=self._clustercatdictmaker(self.matrix_with_cats)
		cluster_features=defaultdict()
		for i in dict:
			cluster_features[i]={k:float(len(v)) for k,v in dict[i].items()}
			cluster_features[i]['total']=sum(cluster_features[i].values())
			cluster_features[i]['no_of_categories']=len(dict[i])
		return cluster_features
		
	def cluster_features(self):
		#how spread out is each cluster? , returns dictionary of basic stats such as mean, std, per cluster
		featuredicti=defaultdict()
		dict=self._clusterdictmaker(self.matrix_without_cats)
		zscoredict={k:scipy.stats.mstats.zscore(dict[k], axis=0, ddof = 1) for k in dict.keys()} #setting  "ddof = 1" so we get the same output as in R
		silhouette=sklearn.metrics.silhouette_samples(self.matrix_without_cats, self.labels)
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

	def cluster_silhouette(self, distance_metric):
		silhouette=sklearn.metrics.silhouette_score(self.matrix_without_cats, self.labels, metric=distance_metric)
		return silhouette


# remember that we could use z scores		
class Centroidstats(Clustering):
	"""
	Returns statistics and calculations with centroids of a clustering.
	"""
			
	def __init__(self, matrix_without_cats, name, labels, centroids=None, actual_centroids=None):
		Clustering.__init__(self, name, labels, centroids, actual_centroids)
		#relevant here: centroids and actual centroids
		#centroid will be a vector of len (x)
		self.matrix_without_cats=matrix_without_cats
		
	def _centroid_check(self):
		if self.centroids == None:
			#raise ValueError("Model {} has no centroids".format(self.name))
			#make a new centroid for each cluster
			centroids=[]
			try:
				for c in range(0,len(np.unique(self.labels))):
					vectors=self.matrix_without_cats[np.where(self.labels==c)]
					centroid=np.mean(vectors, axis=0)
					centroids.append(centroid)
				print "Warning:\nCentroids for {} calculated after the clustering".format(self.name)
				self.centroids=centroids
			except:
				raise ValueError("Model {} has no centroids".format(self.name))
		else:
			pass
			
	def _centroiddictmaker(self):
		# returns a dictionary of centroid per cluster
		# structure: {cluster:vector_of_centorids, cluster2: ....}
		try:
			self._centroid_check()
			centroiddicti=defaultdict()
			for i in range(self.no_of_clusters):
				centroiddicti[i]=self.centroids[i]
			return centroiddicti
		except ValueError as err:
			print err
	
			
	def distance_between_centroids(self):
		#returns dictionary of distance between centroids of clustering
		# structure: {cluster_to_cluster2:{hamming_dist:x, euclid_dist:y ....} , cluster_to_cluster3: ....}	
		try:
			self._centroid_check()
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
		except ValueError as err:
			print err		
	
	def _differencemaker(self, dict_of_values):
		"""
		takes a dictionary, computes differences between each pair of entries. 
		returns (comparison pair, differences, array of sorted indexes).
		"""
		sorted=[]
		for combo in itertools.combinations(dict_of_values.keys(), 2):
			diff=dict_of_values[combo[0]]-dict_of_values[combo[1]]
			absolute_diff=abs(diff)
			sorted.append((combo,  diff, np.argsort(absolute_diff)))
		return sorted
	
		
	def cluster_predictors(self, vocab_used_for_feature_extraction):
		"""
		takes a dictionary of centroids and a dictionary of features to compute features most predictive of each cluster
		returns dictionary { cluster: {raw_diff:(word X,difference score), (word Y, difference score) ..., zscores_diff: ()()}, cluster2: {...}}
		"""
		try:
			self._centroid_check()
			centroiddicti=self._centroiddictmaker()
			vocab=vocab_used_for_feature_extraction.keys()
			arrayed_vocab=np.array(vocab)
			zscoredicti={k:scipy.stats.mstats.zscore(centroiddicti[k], axis=0, ddof = 1) for k in centroiddicti.keys()} #setting  "ddof = 1" so we get the same output as in R
			predictdicti=defaultdict()
			sorted_values=self._differencemaker(centroiddicti)
			sorted_zscores=self._differencemaker(zscoredicti)
			predictdicti={tup[0]:{
			'raw_diff':None,
			'zscores_diff':None
			} 
			for tup in sorted_values}
			
			# "In other words, a[index_array] yields a sorted a."
			for tup in sorted_values:
				index=tup[2]
				#sort by index, reverse so largest values are first
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
		except ValueError as err:
			print err
	
	def central_documents(self, wordmatrix_with_cats, filedict):
		"""
		takes a matrix with labels and the dictionary of files ({number: file_location})
		returns a sorted list of file_locations with first file closest to centroid
		"""
		try:
			self._centroid_check()
			centroids=self._centroiddictmaker()
			docs={}
			# note that we can use the distance metric above as well
			for entry in centroids:
				centroid=np.array([centroids[entry]])
				docs[entry]=defaultdict(list)
				matrix_without_cats=wordmatrix_with_cats[:wordmatrix_with_cats.shape[0], wordmatrix_with_cats.shape[1]-centroid.shape[1]:wordmatrix_with_cats.shape[1]]
				for d in scipy_distances:
					dist=scipy.spatial.distance.cdist(matrix_without_cats,centroid, d)
					sorted_index=np.argsort(dist, axis=0)
					result = wordmatrix_with_cats.take(sorted_index.reshape(-1), 0)
					# row 1 contains the file number
					for item in result[:20,1]:
						docs[entry][d].append(filedict[item])
			return docs
		except ValueError as err:
			print err
	


class Clusteringsimilarity(Clustering):
	""" 
	Calculates similarity measures between clusterings, tools for  clustering comparison. 
	"""

	def __init__(self, matrix_with_cats, matrix_without_cats, models): 
		#partitionings consists of model name and model out of the list of tuples input into models
		self.partitionings=dict((k, v) for k, v in models)
		self.matrix_without_cats=matrix_without_cats
		self.matrix_with_cats=matrix_with_cats
				
	def get_variables(self, key):
		return self.partitionings.get(key, None)
	
	def set_variables(self, key, value):
		self.partitionings[key]=value
		
	def _partitionsimilarity_dictmaker(self):		
		# for item in self.partitionings:
# 		print self.partitionings[item].name
# 		# what is this?
		similaritydict={}
		# all possible combinations between models
		for combo in itertools.combinations(self.partitionings.keys(),2):
			similaritydict[(combo[0], combo[1])]={
		
			'adjustedrand_sim': sklearn.metrics.adjusted_rand_score(self.partitionings[combo[0]].labels, self.partitionings[combo[1]].labels),
			'adjustedmutualinfo_sim':sklearn.metrics.adjusted_mutual_info_score(self.partitionings[combo[0]].labels, self.partitionings[combo[1]].labels),
			'jaccard_sim': sklearn.metrics.jaccard_similarity_score(self.partitionings[combo[0]].labels, self.partitionings[combo[1]].labels),
			#"This score is identical to normalized_mutual_info_score":
			'v_sim': sklearn.metrics.v_measure_score(self.partitionings[combo[0]].labels, self.partitionings[combo[1]].labels),
			'completeness_sim': sklearn.metrics.completeness_score(self.partitionings[combo[0]].labels, self.partitionings[combo[1]].labels),
			'homogeneity_sim':sklearn.metrics.homogeneity_score(self.partitionings[combo[0]].labels, self.partitionings[combo[1]].labels),
			#double check this silhouette score. how do we get the matrix without in here???
			#'silhouette_score_sim': (sklearn.metrics.silhouette_score(self.matrix_without_cats, self.partitionings[combo[0]].labels), sklearn.metrics.silhouette_score(self.matrix_without_cats, self.partitionings[combo[1]].labels)),
			'variation_of_information':'is in R'
		}
		return similaritydict

	def similarity_matrix(self, metric):
		"""
		this prints out a correlation matrix-style comparison of clusterings. 
		metric is the metric to use, e.g. one of the entries in the dictionary.
		returned by self._partitionsimilarity_dictmaker.
		"""
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
		"""
		returns Silhouette score for each clustering.
		"""
		qualitydict={}
		for key in self.partitionings.keys():
			qualitydict[key]=sklearn.metrics.silhouette_score(self.matrix_without_cats, self.partitionings[key].labels)
		return qualitydict
		
		


class Categorystats(Clustering):
	"""
	Statistics of categories within a clustering.
	"""
	
	def __init__(self, matrix_with_cats, name, labels , centroids=None, actual_centroids=None): 
		Clustering.__init__(self, name, labels , centroids=None, actual_centroids=None)
		self.matrix_with_cats=matrix_with_cats
	
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

def basicstatsmaker(dataset):
		statdict={
		'means':np.mean(dataset, axis=0),
		'median':np.median(dataset, axis=0),
		'std':np.std(dataset, axis=0),
		'min':np.min(dataset, axis=0),
		'max':np.max(dataset, axis=0),
		'range':np.ptp(dataset, axis=0)
		}
		return statdict


def outlierremover(dataset_without_cats, dataset_with_cats, distance_metric, median_metric, standard_deviations):
	''' 
	Removes outliers from dataset removed more than standard_deviations * standard deviations removed from median
	'''
	print "We are removing outliers"
	print "before outlier removal\n", dataset_without_cats
	distance_matrix=sklearn.metrics.pairwise.pairwise_distances(dataset_without_cats, Y=None, metric=distance_metric, n_jobs=1)
	#print "dista matrix\n", distance_matrix
	average=getattr(np, median_metric)(distance_matrix, axis=1)
	#print "mean\n", average
	overall_avg=getattr(np, median_metric)(average)
	print "mean\n", overall_avg
	print np.mean(average)
	overall_std=np.std(average)
	print "stdev\n", overall_std
	gooddata_without_cats=dataset_without_cats[average < overall_avg+(standard_deviations * overall_std)]
	gooddata_with_cats=dataset_with_cats[average < overall_avg+(standard_deviations * overall_std)]
	print "output\n", gooddata_with_cats
	return gooddata_without_cats, gooddata_with_cats
	



def matrixstats(matrix, matrix_with_cats, distance_metric, zscores=False, outlier_removal=False, outlier_threshold=2, median_metric='median', compute_distance = False ):
	'''
	Matrixstats computes basic statistics and optionally normalizes scores and removes outliers.
	It computes basic statistical values such as the mean, median, standard deviation, and range of values.
	Outliers can be removed by specifying a limit on the number of standard deviations a score may be removed from the median.
	For the zscore transformation, degrees of freedom is set to 1 to make results equivalent to R zscores. 
	'''
	print "Starting the matrix stats"
	#print "Sample rows\n", matrix[:3,:], "\n"
	print "\nInput statistics"
	inputstats=basicstatsmaker(matrix)
	for entry in inputstats:
		print entry, "\n", inputstats[entry]
	print "\n"

	# here we remove outliers
	if outlier_removal:
		print "\n\nWe are removing outliers"
		print "Matrix shape before outlier removal", matrix.shape
		matrix, matrix_with_cats=outlierremover(matrix, matrix_with_cats, distance_metric, median_metric, outlier_threshold)
		print "Matrix shape after outlier removal", matrix.shape
		print "\n"

	# here we transform data set to zscores
	if zscores:
		print "\n\nWe are computing zscores"
		matrix = scipy.stats.mstats.zscore(matrix, axis=0, ddof=1)
		print "Sample rows zscores", matrix[:3,:]
		if np.isnan(np.min(matrix)):
			print "\n\nAlarm. NaNs detected in zscore transformation\n\n"
		zscoredict=basicstatsmaker(matrix)
		for entry in zscoredict:
			print entry, "\n", zscoredict[entry]
		
			
	# compute a distance matrix
	if compute_distance:
		distmatrix=sklearn.metrics.pairwise.pairwise_distances(matrix, Y=None, metric=distance_metric, n_jobs=1)
		diststats=basicstatsmaker(distmatrix)
		print "\nDistance matrix"
		print "Sample rows distance matrix", distmatrix[:3,:]
		print "Statistics distance matrix"
		for item in diststats:
			print item, diststats[item]
# 	distzscores = scipy.stats.mstats.zscore(distmatrix, axis=0, ddof=1)
# 	diststats=basicstatsmaker(distzscores)
# 	print "Distance matrix statistics"
# 	for item in diststats:
# 		print item, "\n", diststats[item]
# 	print "Range of distances", np.ptp(diststats['range'])
	print "\n\ndone with matrix stats"
	return matrix, matrix_with_cats


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
    
def remover(original_list, to_delete):
	"""
	This is to adapt our stopword list.  
	"""
	newlist=[s for s in original_list if s not in to_delete]
	print "We deleted {}".format(",".join(to_delete))
	return set(newlist)
	
    
def dictwriter(file_name, dictionary, sort_dict=True):
	"""
	writes out a dictionary to a text file after sorting it.
	"""
	#it would be nice if input was just the file name and we add ending according to format
	#right now, we do ".txt.json"
	print "Starting the dictionarywriter, sorting is", sort_dict
	sorteddict=sorted(dictionary.items(), key=lambda x: x[1], reverse=True)
	with codecs.open(os.path.expanduser(file_name+".txt"), "w", "utf-8") as outputi:
		outputi.write("\n".join([":".join([i[0],unicode(i[1])]) for i in sorteddict]))
	with codecs.open(os.path.expanduser(file_name+".json"), "w", "utf-8") as jsonoutputi:
		json.dump(dictionary, jsonoutputi, ensure_ascii=False)
	print "Written to",  os.path.join("outputfiles",file_name)