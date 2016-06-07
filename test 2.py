import numpy as np


diff_median_stdev=np.array([[1,1,1], [0,0,0], [-1,-1,-1], [1,0,1]])
# print "input frame\n", diff_median_stdev
# 
# 
# means=np.mean(distance_matrix, axis=1)
# print "mean\n", means
# overmean= np.mean(means)
# 
# 
# print "mean of means",overmean
# 
# 
# std=np.std(means)
# print "std pf means", std
# t=diff_median_stdev[means > overmean+(standard_deviations * std)]
# print "testi\n", t
# tt=[(diff_median_stdev < 1).all(axis=0)]
# print "testing exclusion", tt
# 
# testframe=np.array([[1],[2],[3],[4]])
# print "test  frame\n", testframe
# r=testframe[(diff_median_stdev == 1).all(axis=1)]
# 
# print "after mixing", r


print getattr(np, 'median')(diff_median_stdev, axis=1)