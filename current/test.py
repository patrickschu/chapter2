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

t=np.array([[1,1],[2,2],[3,3]])

uniq=np.array([0,1,2])

r=np.column_stack([ uniq, t])

print r

print "we extract row 1", "\n", r[:,1:]



#number dictionary
numberdict={}

