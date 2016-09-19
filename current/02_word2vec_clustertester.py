#clustertest
import os
import json
import codecs

header="\n\n\n-----\n"
# dir is the place where our jsons of clusters hang out
dir = '/Users/ps22344/Downloads/chapter2/current/outputfiles'
jsons=[i for i in os.listdir(dir) if not i.startswith(".")]



def clustertester(filelist):
	"""
	the clustertester reads in json file, prints out content of each cluster.
	"""
	for fili in filelist:
		print "!!!", fili, "!!!"
		with codecs.open(os.path.join(dir, fili), "r", "utf-8") as jsoninput:
			datafile=json.load(jsoninput)
		print "!!!", len(datafile), "!!!"
		for entry in datafile:
			print header, "******", entry, "******"
			print datafile[entry]['words']
		print header




clustertester(jsons)




