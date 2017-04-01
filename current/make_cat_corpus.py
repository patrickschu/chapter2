import shutil
import codecs
import os
import clustertools as ct

#this we use with tokens_by_cat

dir= "/Users/ps22344/Downloads/craig_0208"

for folder in [i for i in os.listdir(dir) if not i.startswith(".")]:
	for fili in [i for i in os.listdir(os.path.join(dir, folder)) if not i.startswith(".")]:
		if ct.Ad(os.path.join(dir, folder, fili)).meta["category1"] in ['w4m']:
			print "copy from {} to {}".format(os.path.join(dir, folder, fili), os.path.join("samplecorpus", fili))
			shutil.copy2(os.path.join(dir, folder, fili), os.path.join("samplecorpus", fili))
