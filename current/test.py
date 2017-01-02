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
import sklearn

def featurecollector(categories, uniqs, mode="freq"):
	"""
	collects those features, returns a np array with frequencies. 
	first item in returned list is a category, 2nd a uniq number. 
	Parameters
	----------
	mode : 'freq' returns a list of items per word, 'count' a list of counts
	
	Returns
	-------
	np array with frequencies..
	"""
	modestring=mode
	listi=[]
	listi.append(("category1", category1))
	listi.append(("uniqs", uniqs ))
	##collect features
	rep_raw, rep_freq= eg.repeatedpunctuationfinder(dir)
	print "shape", rep_freq.shape
	rep_freq=rep_freq.sum(axis=1)
	print "shape", rep_freq.shape
	print range(0, [int(1) if len(rep_freq.shape) < 2 else rep_freq.shape[1] for i in [1]][0])
	listi.append((["repeated_punctuation"+str(count) for count in range(0, [int(1) if len(rep_freq.shape) < 2 else rep_freq.shape[1] for i in [1]][0])], rep_freq))


	leet_raw, leet_freq= eg.leetcounter(dir)
	print "shape", leet_freq.shape
	leet_freq=leet_freq.sum(axis=1)
	listi.append((["leetspeak"+str(count) for count in range(0, [int(1) if len(leet_freq.shape) < 2 else leet_freq.shape[1] for i in [1]][0])], leet_freq))



	#all rebus go together
	rebfor_raw, rebfor_freq= eg.rebusfinder_for(dir)
	rebto_raw, rebto_freq= eg.rebusfinder_to(dir)
	rebtoo_raw, rebtoo_freq= eg.rebusfinder_too(dir)
	rebus_freq=rebtoo_freq+rebto_freq+rebfor_freq
	listi.append((["rebus"+str(count) for count in range(0, [int(1) if len(rebus_freq.shape) < 2 else rebus_freq.shape[1] for i in [1]][0])], rebus_freq))
	print "shape of rebus", np.array(rebus_freq).shape
	print rebus_freq


	caps_raw, caps_freq=eg.capsfinder(dir, 0.5)
	print "shape", caps_freq.shape
	caps_freq=caps_freq.sum(axis=1)
	print caps_freq.shape
	listi.append((["capitalization"+str(count) for count in range(0, [int(1) if len(caps_freq.shape) < 2 else caps_freq.shape[1] for i in [1]][0])], caps_freq))

	single_raw, single_freq=eg.singleletterfinder(dir)
	print "shape", single_freq.shape
	single_freq=single_freq.sum(axis=1)
	listi.append((["single_letters"+str(count) for count in range(0, [int(1) if len(single_freq.shape) < 2 else single_freq.shape[1] for i in [1]][0])], single_freq))

	clip_raw, clip_freq=eg.clippingcounter(dir)
	print "shape", clip_freq.shape
	clip_freq=clip_freq.sum(axis=1)
	listi.append((["clippings"+str(count) for count in range(0, [int(1) if len(clip_freq.shape) < 2 else clip_freq.shape[1] for i in [1]][0])], clip_freq))

	acro_raw, acro_freq=eg.acronymcounter(dir)
	print "shape", acro_freq.shape
	acro_freq=acro_freq.sum(axis=1)
	listi.append((["acronyms"+str(count) for count in range(0, [int(1) if len(acro_freq.shape) < 2 else acro_freq.shape[1] for i in [1]][0])], acro_freq))

	emos_raw, emos_freq=eg.emoticonfinder(dir)
	print "shape", emos_freq.shape
	emos_freq=emos_freq.sum(axis=1)
	listi.append((["emoticons"+str(count) for count in range(0, [int(1) if len(emos_freq.shape) < 2 else emos_freq.shape[1] for i in [1]][0])], emos_freq))


	pros_raw, pros_freq=eg.prosodycounter(dir)
	print "shape", pros_freq.shape
	pros_freq=pros_freq.sum(axis=1)
	listi.append((["prosody"+str(count) for count in range(0, [int(1) if len(pros_freq.shape) < 2 else pros_freq.shape[1] for i in [1]][0])], pros_freq))
	return listi


















#from sklearn import feature_extraction
import scipy
catdict={"m4m":1, "w4m":2, "w4w":3}
feature_list=['fet1', 'fet2']
#array is cat - uniq - data
t=np.array([[1,1,2.],[0,0, 0.],[5,3, 5000000.], [3,3,3]])
cats=np.array([1,2,1,1])
t=np.column_stack([cats, t])
print t

tfidf=sklearn.feature_extraction.text.TfidfTransformer(norm=u'l2', use_idf=True, smooth_idf=True, sublinear_tf=False)
print tfidf.fit(t)
print tfidf.transform(t)
print tfidf.transform(t).toarray()

#print t.shape
#mean, median, range, min-max, n
#For feature {1}, category {2} has {3} data points. The mean is {4} (median: {5}) with a range between {6} and {7}. Standard deviation: {}.
#
# 3 is shape[0]

# A 2-dimensional array has two corresponding axes: the first running vertically downwards across rows (axis 0), and the second running horizontally across columns (axis 1). https://docs.scipy.org/doc/numpy/glossary.html


