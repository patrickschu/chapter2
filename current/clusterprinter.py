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

with codecs.open('clusters_74_19_45_07_31.json', 'r', 'utf-8') as jsoninput:
	wordtovecclusters=json.load(jsoninput)

wordtovecclusters={int(k):v for k,v in wordtovecclusters.items()}
for entry in sorted(wordtovecclusters):
	print entry
	print wordtovecclusters[entry]['words']
	print header