import re, os, numpy as np

class Cluster(object):
	def __init__(self, dataframe, name, labels , centroids=None, actual_centroids=None):
		self.dataframe=dataframe
		self.name=type(name)
		self.labels=labels
		self.centroids=centroids
		self.actual_centroids=actual_centroids
		self.no_of_clusters=len(np.unique(labels))
	def getName(self):
		return self.name
	# def getClusterNumber(self):
# 		labels=list(self.labels)
# 		labels=set(labels)
# 		return len(labels)


#
###FUNCTIONS
##

#setting up some helper functions
def tagextractor(text, tag, fili):
    regexstring="<"+tag+"=(.*?)>"
    result=re.findall(regexstring, text, re.DOTALL)
    if len(result) != 1:
        print "alarm in tagextractor", fili, result
    return result[0]
    
def adtextextractor(text, fili):
    regexstring="<text>(.*?)</text>"
    result=re.findall(regexstring, text, re.DOTALL)
    if len(result) != 1:
        print "alarm in adtextextractor", fili, result
    return result[0]
