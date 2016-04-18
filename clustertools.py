import re, os, numpy as np, scipy
from collections import defaultdict




class Cluster(object):
	"""collect basic features of a cluster"""

	def __init__(self, matrix_with_cats, name, labels , centroids=None, actual_centroids=None):
		self.matrix_with_cats=matrix_with_cats  #data frame including "gold labels"
		self.matrix_without_cats=matrix_with_cats[:,1:] #data frame without "gold labels"
		self.name=type(name) #the clustering algorithm we are dealing with
		self.labels=labels #the array of labels: label for each data point
		self.centroids=centroids #the centroids or prototypes if applicable. WATCH:: INDEXES OR ACTUAL????
		self.actual_centroids=actual_centroids #what is this relevant for??
		self.no_of_clusters=len(np.unique(labels)) #how many clusters this algorithm came up with
	def getName(self):  
		return self.name  #why do we need this??



class Clusterstats(Cluster):
	"""basic statistics of a cluster"""

	def __init__(self, matrix_with_cats, name, labels , centroids=None, actual_centroids=None): 
		Cluster.__init__(self, matrix_with_cats, name, labels , centroids=None, actual_centroids=None)
		
		
	def _clusterdictmaker(self, matrix):
		#in the clusterdicti, we collect for each cluster the data points contained
		# output is a dictionary with ACTUAL vectors
		# why don't we feed it the self.matrix?
		iterator=range(self.no_of_clusters)
		clusterdicti=defaultdict()
		for cluster in iterator:
			#print "cluster: " ,cluster
			#give me indexes of label array where cluster is true	
			#note that where returns a cluster that is always len 1
			# we are interested in l[0]
			#clusterdicti[cluster]=np.where(self.labels==cluster)[0]
			clusterdicti[cluster]=np.array([matrix[i] for i in np.where(self.labels==cluster)[0]])
		return clusterdicti
	
	def _clustercatdictmaker(self, matrix):
		#in this dicti, we collect for each cluster the items per category
		# output is a dictionary of ACTUAL vectors
		#structure: { cluster: {cat1: ...., cat2:..., cat3:....}, cluster2: {....}
		# why don't we feed it the self.matrix?
		iterator=range(self.no_of_clusters)
		clustercatdicti=defaultdict()
		for cluster in iterator:
			clustercatdicti[cluster]=defaultdict(list)
			#note that where returns a cluster that i always len 1
			# we are interested in l[0]
			wordmatrix=[matrix[i] for i in np.where(self.labels==cluster)[0]]
			for item in matrix:
				clustercatdicti[cluster][item[0]].append(item)
		return clustercatdicti
		
	
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
		#how spread out is the cluster?
		# returns dictionary of basic stats
		featuredicti=defaultdict()
		dict=self._clusterdictmaker(self.matrix_without_cats)
		zscoredict={k:scipy.stats.mstats.zscore(dict[k], axis=0, ddof = 1) for k in dict.keys()} #setting  "ddof = 1" so we get the same output as in R
		for i in dict:
			featuredicti[i]={
			'mean':np.mean(dict[i], axis=0), #mean of column
			'median':np.median(dict[i], axis=0), #median of column
			'std':np.std(dict[i], axis=0,ddof = 1 ), #setting  "ddof = 1" so we get the same output as in R
			'var':np.var(dict[i], axis=0), #variance of column
			'range':np.ptp(dict[i], axis=0), #range of column, raw scores
			'zscore_range':np.ptp(zscoredict[i], axis=0), #range of column, zscores
			#this is still very under development
			'feature_correlation':np.corrcoef(dict[i], rowvar=0) #feature correlation over rows
			} 
		return featuredicti




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
