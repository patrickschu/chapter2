import egrammartools as eg
import clustertools as ct


#extract features by gender or category only
import egrammartools as eg
import clustertools as ct
import numpy as np
import time
import scipy
import sklearn
import os

headline="\n\n-----------\n\n"


dir="/Users/ps22344/Downloads/chapter2/current/w4w"

def featurecollector(categories, uniqs, result_mode):
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
	modeindexes={
	"freq":1,
	"count":0}
	
	print "result mode", result_mode
	index=modeindexes[result_mode]
	listi=[]
	listi.append(("category1", category1))
	listi.append(("uniqs", uniqs ))
# 	##collect features
# 
	result= eg.repeatedpunctuationfinder(dir)
	rep_freq= result[index]
	print "shape", rep_freq.shape
	rep_freq=rep_freq.sum(axis=1)
	print "shape", rep_freq.shape
	print range(0, [int(1) if len(rep_freq.shape) < 2 else rep_freq.shape[1] for i in [1]][0])
	listi.append((["repeated_punctuation"+str(count) for count in range(0, [int(1) if len(rep_freq.shape) < 2 else rep_freq.shape[1] for i in [1]][0])], rep_freq))
# 
# 
# 	result= eg.leetcounter(dir)
# 	leet_freq= result[index]
# 	print "shape", leet_freq.shape
# 	leet_freq=leet_freq.sum(axis=1)
# 	listi.append((["leetspeak"+str(count) for count in range(0, [int(1) if len(leet_freq.shape) < 2 else leet_freq.shape[1] for i in [1]][0])], leet_freq))
# 
# 
# 
# 	#all rebus go together
# 
# 	result= eg.rebusfinder_for(dir)
# 	rebfor_freq= result[index]
# 	
# 
# 	result= eg.rebusfinder_to(dir)
# 	rebto_freq= result[index]
# 	
# 	result= eg.rebusfinder_too(dir)
# 	rebtoo_freq= result[index]
# 	
# 	rebus_freq= rebtoo_freq+rebto_freq+rebfor_freq
# 	listi.append((["rebus"+str(count) for count in range(0, [int(1) if len(rebus_freq.shape) < 2 else rebus_freq.shape[1] for i in [1]][0])], rebus_freq))
# 	print "shape of rebus", np.array(rebus_freq).shape
# 	print rebus_freq

	
#	result= eg.capsfinder(dir, 0.5)
#	caps_freq= result[index]
#	caps_freq=caps_freq.sum(axis=1)
#	print "shape", caps_freq.shape
#	listi.append((["capitalization"+str(count) for count in range(0, [int(1) if len(caps_freq.shape) < 2 else caps_freq.shape[1] for i in [1]][0])], caps_freq))

# 	result= eg.singleletterfinder(dir)
# 	single_freq= result[index]
# 	print "shape", single_freq.shape
# 	single_freq=single_freq.sum(axis=1)
# 	listi.append((["single_letters"+str(count) for count in range(0, [int(1) if len(single_freq.shape) < 2 else single_freq.shape[1] for i in [1]][0])], single_freq))
# 
# 	result=eg.clippingcounter(dir)
# 	clip_freq= result[index]
# 	print "shape", clip_freq.shape
# 	clip_freq=clip_freq.sum(axis=1)
# 	listi.append((["clippings"+str(count) for count in range(0, [int(1) if len(clip_freq.shape) < 2 else clip_freq.shape[1] for i in [1]][0])], clip_freq))
# 
# 	result= eg.acronymcounter(dir)
# 	acro_freq= result[index]
# 	print "shape", acro_freq.shape
# 	acro_freq=acro_freq.sum(axis=1)
# 	listi.append((["acronyms"+str(count) for count in range(0, [int(1) if len(acro_freq.shape) < 2 else acro_freq.shape[1] for i in [1]][0])], acro_freq))
# 
# 	result= eg.emoticonfinder(dir, '/Users/ps22344/Downloads/chapter2/textfiles/emolist_final_2.txt')
# 	emos_freq= result[index]
# 	print "shape", emos_freq.shape
# 	emos_freq=emos_freq.sum(axis=1)
# 	listi.append((["emoticons"+str(count) for count in range(0, [int(1) if len(emos_freq.shape) < 2 else emos_freq.shape[1] for i in [1]][0])], emos_freq))
# 
# 
# 	result= eg.prosodycounter(dir)
# 	pros_freq= result[index]
# 	print "shape", pros_freq.shape
# 	pros_freq=pros_freq.sum(axis=1)
# 	listi.append((["prosody"+str(count) for count in range(0, [int(1) if len(pros_freq.shape) < 2 else pros_freq.shape[1] for i in [1]][0])], pros_freq))

 	return listi

completestart=time.time()

category_to_extract= 'addressee1'


##prep
#add cats
categories_dict, no_of_categories = ct.categorymachine(dir, category_to_extract)
category1=ct.categoryarraymachine(dir, category_to_extract, categories_dict)

#add uniqs
uniqs, file_count, filedicti=ct.uniqarraymachine(dir, 0) 	
print "So many files", file_count


#put into one matrix
listi=featurecollector(category1, uniqs, result_mode="count")
print ",".join(['mean','min','max','median','std'])
for item in listi:
	frame= item[1].shape
	
	mean= item[1].mean()
	min= item[1].min()
	max= item[1].max()
	median= np.median(item[1])
	std= item[1].std()
	print '***', item[0]
	#print "For item {}, overall mean is {}, min is {}, max is {}, median is {}, st is {}, shape: {}".format(mean, min, max, median, std, frame)
	print ",".join([str(i) for i in [mean, min, max, median, std]])


t=np.column_stack([i[1] for i in listi])
print "original matrix",  type(t), t.shape


##
###category and feature dicts
catdicti=categories_dict
featuredict=[i[0] for i in listi if i[0] not in ["uniqs", "category1"]]
#flatten it
featuredict=[n for i in featuredict for n in i]

##
###data matrices
#this is the t w/out category without category and without unique as in the matrixmachine
wordmatrix_without_cat=t[:,2:]
#this one keeps the category and the uniq
wordmatrix_with_cat=t
ct.meanmachine(wordmatrix_with_cat, categories_dict, featuredict, verbose="csv", limit=100)

##ZSCORES?
#zscored matrix
wordmatrix_without_cat=scipy.stats.zscore(t[:,2:], axis=0)
wordmatrix_with_cat=np.column_stack([category1, uniqs, scipy.stats.zscore(t[:,2:], axis=0)])
#print "ayayay", wordmatrix_with_cat

##TFIDF?
#textfreq inverse doc freq
#tfidf=sklearn.feature_extraction.text.TfidfTransformer(norm='l2', use_idf=True, smooth_idf=True, sublinear_tf=False)
#wordmatrix_without_cat=tfidf.fit_transform(t[:,2:]).toarray()
#wordmatrix_with_cat=np.column_stack([category1, uniqs, wordmatrix_without_cat])
#print "settings from tfidf", tfidf.get_params()



print "matrix with cat and uniq", wordmatrix_with_cat.shape
print "matrix w/out cat and uniq", wordmatrix_without_cat.shape
ct.matrixstats(wordmatrix_without_cat, wordmatrix_with_cat)


print "feature dict", featuredict, len(featuredict)
#print listi
##ADD SPELLING!!!!TO DO
#print wordmatrix_with_cat
print wordmatrix_with_cat.shape

completeend=time.time()
os.system('say "your program has finished"')

