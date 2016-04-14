import re, os

class Cluster(object):
	def __init__(self, dataframe, name, labels , centroids=None, actual_centroids=None):
		self.dataframe=dataframe
		self.name=name
		self.labels=labels
		self.centroids=centroids
		self.actual_centroids=actual_centroids
	def getName(self):
		return self.name


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
