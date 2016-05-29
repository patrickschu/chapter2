#!/usr/bin/env python

import numpy as np
import scipy.spatial
import sklearn
from sklearn import metrics
# 
# r=np.array([-0.00291545, -0.00588915, -0.00663255, -0.0128536 ,  0.06196439,
#        -0.01077545, -0.00480579, -0.00834806,  0.00864689,  0.00866725])
# x=r-1
# t=np.vstack([x,r,x])
# print "\n", t, "\n"
#       
# print r
# def add2(i):
# 	return i +2
# 	
# print "\n", r.shape	
#c=np.vectorize(scipy.spatial.distance.pdist(t,r,'euclidean'))

#print c


#

#
#print t.shape
#print t

#centroid=[1,2,3]
#print t[:t.shape[0],t.shape[1]-len(centroid):t.shape[1]]
       
#index=np.argsort(abs(r))
#print r[index][::-1]


#dist = scipy.spatial.distance.cdist(t,r) # pick the appropriate distance metric 
#print dist


# a = np.random.normal(size=(10,3))
# b = np.random.normal(size=(1,3))
# dist = scipy.spatial.distance.cdist(a,b)
# print dist

tt=np.array([[1,1,1,1,1],[0,2000,122,33,5.4], [1,1,1,1,1], [33,34,32,35,39], [22.,33.5,32,35,39], [1,1,1,1,1]])
tt=np.array([[.1,.001,.00001,.001,.001],[0,0,0,0,0], [.1,.001,.00001,.001,.001], [0,0,.00032,.0000000035,.0039], [0.000022,0.000033,.0032,.0035,.0039], [.1,.001,.00001,.001,.001]])

tt=np.random.uniform(0, .1, size=(12,300))
rr=np.random.uniform(0, .1, size=(12,300))
tt=tt+rr

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


def outlierremover(dataset, median_metric, standard_deviations):
	''' 
	Removes outliers from dataset removed more than standard_deviations * standard deviations removed from median
	'''
	print "We are removing outliers"
	stats=basicstatsmaker(dataset)
	diff_to_median = dataset - stats[median_metric]
	
	# print "medi", stats['median']
# 	print "stdev", stats['std']
# 	print "diffi with meedian\n", diff_to_median
	diff_median_stdev=np.absolute(diff_to_median)-(standard_deviations * np.absolute(stats['std']))
	#print "diffi with stdev\n", diff_median_stdev
	#http://stackoverflow.com/questions/11130831/getting-all-rows-where-complex-condition-holds-in-scipy-numpy
	gooddata=diff_median_stdev[(diff_median_stdev < 0).all(axis=1)]
	return gooddata



def matrixstats(matrix, distance_metric, zscores=False, outlier_removal=False, outlier_threshold=2, median_metric='median' ):
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
	#for entry in inputstats:
	#	print entry, inputstats[entry]
	print "\n"

	# here we remove outliers
	if outlier_removal:
		print "Matrix shape before outlier removal", matrix.shape
		matrix=outlierremover(matrix, median_metric, outlier_threshold)
		print "Matrix shape after outlier removal", matrix.shape
		outlierstats=basicstatsmaker(matrix)
		for entry in outlierstats:
			print entry, outlierstats[entry]
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
			print entry, zscoredict[entry]
		
			
	# compute a distance matrix
	distmatrix=sklearn.metrics.pairwise.pairwise_distances(matrix, Y=None, metric=distance_metric, n_jobs=1)
	diststats=basicstatsmaker(distmatrix)
	print "\nDistance matrix"
	print "Sample rows distance matrix", distmatrix[:3,:]
	for item in diststats:
		print item, diststats[item]
	distzscores = scipy.stats.mstats.zscore(distmatrix, axis=0, ddof=1)
	diststats=basicstatsmaker(distzscores)
	print "Distance matrix statistics"
	for item in diststats:
		print item, diststats[item]
	print "Range of distances", np.ptp(diststats['range'])
	#
	print "\n\ndone with matrix stats"
	return matrix
	
scipy_distances=['euclidean', 'minkowski', 'cityblock', 'seuclidean', 'sqeuclidean', 'cosine', 'correlation','hamming', 'jaccard', 'chebyshev', 'canberra', 'braycurtis', 'mahalanobis', 'yule', 'matching', 'dice', 'kulsinski', 'rogerstanimoto', 'russellrao', 'sokalmichener', 'sokalsneath', 'wminkowski']

for d in scipy_distances:
	matrixstats(tt, d)