##give me size of clusters

import codecs
import json
import numpy as np


with codecs.open('/Users/ps22344/Downloads/chapter2/current/clusterskmeans_54_19_10_07_30.json', 'r', 'utf-8') as jsoninput:
	wordtovecclusters=json.load(jsoninput)

results=[]

for k in wordtovecclusters:
	print k
	print len(wordtovecclusters[k]['words'])
	results.append(len(wordtovecclusters[k]['words']))
	print "\n\n---\n"
	
print "word2vec cluster stats"
print "mean", np.mean(results)
print "range", np.ptp(results)
print "min", np.min(results)
print "max", np.max(results)