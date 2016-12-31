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

t=np.array([[1,1, 1000],[2,2, 20],[5,3, 5000000]])

print t
print t.shape
print scipy.stats.zscore(t, axis=0)




uniq=np.array([0,1,2])

r=np.column_stack([ uniq, t])

#print r

#print "we extract row 1", "\n", r[:,1:]



#number dictionary
numberdict={}

