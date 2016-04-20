import sklearn.metrics, numpy as np, scipy, re, os, itertools, tabulate

# Array of pairwise distances between samples, or a feature array.
# labels : array, shape = [n_samples]
# clusters=np.array([[1.0,2,1,0,2], [1.0,2,1,0,2],[.0,0,0,1,2], [1.,1,1,1,1], [1.0,2,1,0,20], [1.0,2,1,0,10]])
# labels=np.array([1,2,2,1,3,3])
# print clusters
# t=sklearn.metrics.jaccard_similarity_score(labels, labels)
# print t
# t=[0]
# tt=[0,1,2,3]
# for combo in itertools.product(tt, t):
# 	print combo
# 	
# 	
# labels=np.array([1,2,1,1,2])
# value=np.array([0,100,0,0,100])
# 
# t=np.where(labels==2)
# print t
# print value[t]

cors={(0,0): 10, (1,0):0.2, (1,1):0.0}

k=cors.keys()
v=cors.values()
print k
print v
rowlabels=[i[0] for i in k]
columnlabels=[i[1] for i in k]

for k:v in cors:
	print k


