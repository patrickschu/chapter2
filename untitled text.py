#!/usr/bin/env python

import numpy as np
import scipy.spatial

r=np.array([-0.00291545, -0.00588915, -0.00663255, -0.0128536 ,  0.06196439,
       -0.01077545, -0.00480579, -0.00834806,  0.00864689,  0.00866725])
x=r-1
t=np.vstack([x,r,x])
print "\n", t, "\n"
      
print r
def add2(i):
	return i +2
	
print "\n", r.shape	
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


a = np.random.normal(size=(10,3))
b = np.random.normal(size=(1,3))
dist = scipy.spatial.distance.cdist(a,b)
print dist