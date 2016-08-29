# -*- coding: utf-8 -*-

import sys
import os
import json
import re 
import shutil
import string
import nltk
import codecs 
import scipy, scipy.cluster, scipy.spatial
import time
import sklearn
import itertools
import numpy as np 
from sklearn import cluster, mixture, metrics
from scipy import spatial, sparse
from collections import defaultdict
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

header="\n---------------\n"

with codecs.open('clusterskmeans_54_19_10_07_30.json', 'r', 'utf-8') as jsoninput:
	wordtovecclusters=json.load(jsoninput)

wordtovecclusters={int(k):v for k,v in wordtovecclusters.items()}
for entry in sorted(wordtovecclusters):
	print entry
	for word in wordtovecclusters[entry]['words']:
		print word
	print header