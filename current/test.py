import numpy as np
import codecs
import time
import os
import clustertools as ct
import re
from collections import defaultdict
from string import punctuation
import json
from nltk import pos_tag
import scipy
catdict={1:"m4m", 2:"w4m", 3:"w4w"}

#array is cat - uniq - data
t=np.array([[1,1,2.],[0,0, 0.],[5,3, 5000000.], [3,3,3]])
cats=np.array([1,2,1,1])
t=np.column_stack([cats, t])
print t
print t.shape
#mean, median, range, min-max, n
#For feature {1}, category {2} has {3} data points. The mean is {4} (median: {5}) with a range between {6} and {7}. Standard deviation: {}.
#
# 3 is shape[0]

# A 2-dimensional array has two corresponding axes: the first running vertically downwards across rows (axis 0), and the second running horizontally across columns (axis 1). https://docs.scipy.org/doc/numpy/glossary.html
def categorystats(input_matrix, category_dict, feature_list)
	"""
	The categorystats takes input_matrix, formatted according to guidelines of the matrixmachine: cat - uniq - feature_1, feature_d
	The category_dict maps categories to numbers. 
	The feature_list contains the features in the order they occur in the input_matrix. 
	"""	
	for key in category_dict.keys():
		print key
		tempi=input_matrix[input_matrix[:,0]== key]
		print tempi.shape
		tempi=tempi[:,2:]
		print tempi.shape
		if tempi.shape[0] > 20:
			print "frame", tempi
			print "mean", tempi.mean(axis=0)
			print "max", tempi.max(axis=0)
			print "min", tempi.min(axis=0)
			print "median", np.median(tempi, axis=0)
			print "std", tempi.std(axis=0)
	
	
