import sklearn.metrics, numpy as np, scipy, re, os, itertools

# Array of pairwise distances between samples, or a feature array.
# labels : array, shape = [n_samples]
# clusters=np.array([[1.0,2,1,0,2], [1.0,2,1,0,2],[.0,0,0,1,2], [1.,1,1,1,1], [1.0,2,1,0,20], [1.0,2,1,0,10]])
# labels=np.array([1,2,2,1,3,3])
# print clusters
# t=sklearn.metrics.jaccard_similarity_score(labels, labels)
# print t

tt=[0,0,0,1,2,3]
for combo in itertools.combinations_with_replacement(tt, 2):
			print combo