import egrammartools as eg
import clustertools as ct
import numpy as np
import time
import os
import codecs

completestart=time.time()
listi=[]
dir="/home/ps22344/Downloads/craigbalanced_0601"

##prep
#add cats
categories_dict, no_of_categories = ct.categorymachine(dir, "category1")
category1=ct.categoryarraymachine(dir, "category1", categories_dict)
listi.append(category1)

#add uniqs
def uniqarraymachine(input_dir, start_no):
	"""
	The categoryarraymachine iterates over the input_dir and collects category info for all files.
	It maps the categories to the numbers contained in cat_dict and returns a np.array with results. (The cat_dict will usually come out of the categorymachine above.
	"""
	results=[]
	count=int(start_no)
	for pati in [i for i in os.listdir(input_dir) if not i.startswith(".")]:
		print pati
		for fili in [i for i in os.listdir(os.path.join(input_dir, pati)) if not i.startswith(".")]:
			results.append([count])
			count=count+1
			print "array", count
	return np.array(results), len(results)
	
uniqs, file_count=uniqarraymachine(dir, 0) 	
print "So many files", file_count
listi.append(uniqs)


##collect features
rep_raw, rep_freq= eg.repeatedpunctuationfinder(dir)
listi.append(np.array(rep_freq))


leet_raw, leet_freq= eg.leetcounter(dir)
listi.append(np.array(leet_freq))


rebfor_raw, rebfor_freq= eg.rebusfinder_for(dir)
listi.append(np.array(rebfor_freq))

rebto_raw, rebto_freq= eg.rebusfinder_to(dir)
listi.append(np.array(rebto_freq))

rebtoo_raw, rebtoo_freq= eg.rebusfinder_too(dir)
listi.append(np.array(rebtoo_freq))

caps_raw, caps_freq=eg.capsfinder(dir, 0.5)
listi.append(np.array(caps_freq))

single_raw, single_freq=eg.singleletterfinder(dir)
listi.append(np.array(single_freq))

clip_raw, clip_freq=eg.clippingcounter(dir)
listi.append(np.array(clip_freq))

acro_raw, acro_freq=eg.acronymcounter(dir)
listi.append(np.array(acro_freq))

emos_raw, emos_freq=eg.emoticonfinder(dir)
listi.append(np.array(emos_freq))

# # for x in listi:
	# # print "!!!!!\n\n", x
	
t=np.column_stack(listi)

print type(t), t.shape
completeend=time.time()

#print t

for i in t:
	print "***", i[:3]

print categories_dict

print "This took us {} minutes. So slow!".format((completeend-completestart)/60)