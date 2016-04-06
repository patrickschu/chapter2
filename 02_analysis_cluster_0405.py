import os, re,shutil,string,numpy,nltk,codecs, scipy, scipy.cluster, numpy as np, time, sklearn.cluster
from collections import defaultdict
from nltk.tokenize import word_tokenize
# read the clustering documentation here: 
# http://docs.scipy.org/doc/scipy-0.14.0/reference/generated/scipy.cluster.vq.kmeans2.html

print "start"
starttime=time.time()
print "\n---------------\nSome public service announcements"
#moving parts
pathi=os.path.join("/Users/ps22344/Downloads","craig_0208")

#how many times do we need to see a category for it to be included in the stats
#move to stats functions
catthreshold=10



#setting up some functions
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

#folders=['files9_output_0102']



#
###BUILDING VOCAB
#
#threshold sets how many times a word needs to occur to be included in the featuredict
def dictmaker(folderlist, threshold=1000):
	#this is our general vocab
	vocab={}
	#collecting words
	for folder in folderlist:
		filis=[i for i in os.listdir(os.path.join(pathi,folder)) if not i.startswith(".")]
		print "Building vocab: we have {} files in folder {}".format(len(filis), folder)
		#collect a dictionary with all words
		#lowercase them    
		for fili in filis:
			inputfile=codecs.open(os.path.join(pathi, folder, fili), "r", "utf-8").read()
			inputtext=adtextextractor(inputfile, fili)
			splittext=nltk.word_tokenize(inputtext)
			splittextlo=[i.lower() for i in splittext]
			#do we want to lemmatize or things like that
			for word in splittextlo:
				if word not in vocab:
					vocab[word]=1
				else:
					vocab[word]=vocab[word]+1
	print "Our vocab dictionary has {} entries".format(len(vocab))
	#here we set the threshold
	featuredict= {key:value for key, value in vocab.items() if value > float(threshold) }
	print "Our feature dictionary has {} entries\n---------------\n".format(len(featuredict))
	return featuredict




#how often a category has to be in the cluster to be included in statistics
catnumber=0




#
##FINDING CATEGOIRES
#
def categorymachine(folderlist):
	print folderlist
	catdicti={}
	catnumber=0
	for folder in folderlist:
		filis=os.listdir(os.path.join(pathi,folder))
		for fili in filis:
			inputfile=codecs.open(os.path.join(pathi, folder,fili), "r", "utf-8").read()
			inputtext=adtextextractor(inputfile, fili)
			# lets establish the category
			# we need to make it numeric, so the numpy won't screw up
			category=tagextractor(inputfile, "category1", fili)
			try: 
				cat=catdicti[category]
			except:
				print "We added {} to the category dictionary, coded as {}".format(category, catnumber)
				catdicti[tagextractor(inputfile, "category1", fili)]=catnumber
				catnumber=catnumber+1
				cat=catdicti[tagextractor(inputfile, "category1", fili)]
	return (catdicti, catnumber)

# for c in clusters:
#     print "For cluster {} there are {} items".format(c, labellist.count(c))
    
#check out the groups within in each cluster

#
###BUILDING MATRICES
#
#matrixmachine takes a list of folders	and of external categories to be included
#note that it calls on the category machine

def matrixmachine(folderlist, featuredict, external_category): 
	#constructing matrix
	print "Starting the matrixmachine"
	wordmatrix=np.empty(shape=(1,len(featuredict)+1))
	print "Matrix initial shape: ", np.shape(wordmatrix)
	# making a dictionary for the categories
	catdicti=categorymachine(folderlist)[0]
	for folder in folderlist:
		filis=[i for i in os.listdir(os.path.join(pathi, folder)) if not i.startswith(".")]
		print "Building matrices: we have {} files in folder {}".format(len(filis), folder)
		for fili in filis: 
			inputfile=codecs.open(os.path.join(pathi, folder, fili), "r", "utf-8").read()
			#establish category
			cat=catdicti[tagextractor(inputfile, external_category, fili)]
			#collect a dictionary with all lowercased words
			#note that punctuation is still in here
			splittext=nltk.word_tokenize(inputfile)
			# we lowercase
			splittextlo=[i.lower() for i in splittext]
			#number of "words"
			wordcount=float(len(splittextlo))
			# we make the vector for this file
			# this is a per word frequency
			wordvector=np.array([float(cat)]+[float(splittextlo.count(i))/wordcount for i in featuredict])
			#print wordvector
			#we append it to the matrix
			wordmatrix=np.append(wordmatrix, [wordvector], axis=0)
	print catdicti
	print "Features of word matrix: shape {}, dtype {}".format(np.shape(wordmatrix), wordmatrix.dtype)
	print "---------------\nEnd of public service announcements\n\n"
	#"In 2D, the first dimension corresponds to rows, the second to columns."
	# we don't look at the first row cause that was just for initialization
	# the one without cats we put into the clustering algorithm
	wordmatrix_without_cat=wordmatrix[1:wordmatrix.shape[0],1:wordmatrix.shape[1]]
	wordmatrix_with_cat=wordmatrix[1:wordmatrix.shape[0],]
	return (wordmatrix_without_cat, wordmatrix_with_cat)
	
#this makes clusters; takes the dataset (matrix) and the algorithm
def clustermachine(matrix, algorithm, clusters=4):
	no_of_clusters=range(clusters)
	centroids, labels=algorithm(matrix, len(no_of_clusters), minit='points')
	#for testing purposes, here we fit the scikit learn kmeans
	t=sklearn.cluster.KMeans(n_clusters=4)
	x=t.fit(matrix)
	# #note that labels are for a specific line in the data
	# #we can see if cluster is consistent re certain data points
	labellist=labels.tolist()
	labellist_enum=list(enumerate(labellist))
	#this needs to output
	#return (clusterlabel, index, [cat x, cat y], 
	return centroids, labels 


	
	
	#######MAIN#########
	
def main():
	folders=[i for i in os.listdir(pathi) if not i.startswith(".")]
	folders=['files9_output_0102']
	print "We have {} folders".format(len(folders))
	featuredict=dictmaker(folders)
	wordmatrix_without_cat, wordmatrix_with_cat = matrixmachine(folders, featuredict, "category1")
	print "Shape of the matrix", wordmatrix_without_cat.shape
	centroids, labels=clustermachine(wordmatrix_without_cat, scipy.cluster.vq.kmeans2)
	print "Centroids and labels established"



main()




#
###CLUSTERSTATS
#
# print "\n---------------\nThe makeup of clusters:\n"
# # we connect labels to category of entry
# # remember that labellist_enum consists of tuples where i[0] is the 
# # list index and i[1] the value, i.e. the number of the cluster
# 
# #clustercounts collects a list with the items for each cluster
# clustercounts=defaultdict(list)
# for i in labellist_enum:
#  	clustercounts[i[1]].append(wordmatrix_with_cat[i[0],0])
# 
# #clusterstats contains the statistics of each cluster
# clusterstats=defaultdict()
# 
# for i in clustercounts:
# 	print "Cluster {} contains {} items".format(i, len(clustercounts[i]))
# 	#this dict comprehension makes a sub dict for each cluster:
# 	#CLUSTER: {cat1: {count:x, alias:x}, cat2: {ibid}...}
# 	#e.g. 0 {u'w4w': {'count': 111, 'percentage': 32.080924855491325, 'code': 5}, u'm4w': {'count': 6 ...
# 	clusterstats[i]={c: {
# 	'code':catdicti[c],
# 	'count':clustercounts[i].count(catdicti[c]),
# 	'percentage':float(clustercounts[i].count(catdicti[c]))/len(clustercounts[i])*100
# 	} 
# 	for c in catdicti}
# 	
# print "\n---------------\nThe stats of clusters:\n"
# 
# for i in clusterstats:
# 	print "CLUSTER ",i, ":"
# 	for c in clusterstats[i]:
# 		if clusterstats[i][c]['count'] > catthreshold:
# 			print "category {:>5}, coded as {:>4}: {:>4} items, or {:>4} percent of the cluster".format(
# 			c,
# 			clusterstats[i][c]['code'],
# 			clusterstats[i][c]['count'],
# 			round(clusterstats[i][c]['percentage'])
# 			)
# 	print "\n---\n"
# 		
# #
# ###CATEGORYSTATS
# #
# catstats=defaultdict()
# #for each cat in the catdicti, we collect the total count
# for i in catdicti:
# 	catstats[i]={str(c): clusterstats[c][i]['count'] for c in clusterstats}
# 	catstats[i]['total']=sum(catstats[i].values())
# 
# 
# print "\n---------------\nThe stats of categories:\n"
# 	
# for i in catstats:	
# 	if catstats[i]['total'] > catthreshold:
# 		print "CATEGORY ",i.upper(), ":"
# 		for c in clusters:
# 			c=str(c)
# 			print "cluster {:>2} contains {:>5} out of {:>5} items in this category, or {:>4} percent of the total".format(
# 			c,
# 			catstats[i][c], 
# 			catstats[i]['total'],
# 			round(float(catstats[i][c])/catstats[i]['total']*100)
# 			)
# 		print "\n---\n"
# 		
# 		
# 		
# 		
# 		
# 		
# 		
# 		
# 		
# #
# ###DISPERSION
# #
# # How good are our clusters?
# # maybe just calculate the square of the distance to the centroid, then sum
# # ??
# # then average out per data point
# # look at real outliers (more than 2 stdevs)
# 
# #in this distancedict, we collect the indexes for each cluster 
# #that way we can access the actual data points
# distancedict=defaultdict(list)
# for item in labellist_enum:
# 	#establish index numbers for each cluster
# 	#items are (index, value). thus: item[0] - index, item[1]-cluster
# 	distancedict[item[1]].append(item[0])
# 
# print "\n---------------\nThe dispersion of clusters:\n"
# 
# # print distancedict[1]
# for c in clusters:
# 	print "CLUSTER ",c, ":"
# 	centroid_by_cluster=centroids[c]
# 	wordmatrix_by_cluster=[wordmatrix_without_cat[i] for i in distancedict[c]]
# 	difference=[pow((np.array(centroid_by_cluster) - np.array(i)),2) for i in wordmatrix_by_cluster]
# 	# print wordmatrix_by_cluster[0][:3]
# # 	print centroid_by_cluster[:3]
# # 	print difference[0][:3]
# 	totaldifference=sum([sum(i) for i in difference])
# 	meantotaldifference= totaldifference/len(wordmatrix_by_cluster)
# 	print "Total difference is {} for {} data points, mean difference: {}".format(
# 	round(totaldifference), 
# 	len(wordmatrix_by_cluster),
# 	round(meantotaldifference*1000))
# 	print "\n---\n"
# 	
# 	
# #
# ###PREDICTORS
# #
# #which words drive our clusters?
# # we have a number of centroids == len(clusters)
# #centroids=[x,y,z]
# # for each x,y,z we calculate the range
# # note that we would have to scale them if we dont have per word counts
# # then we have to relate the centroids to the value in the vocab
# # they should have the same index but vocab is a dict
# # but it is fixed; if we do an items(). ?
# #ranges=[range() for c in centroids
# range=np.ptp(centroids, axis=0)	
# #range_with_words=[(i, 
# #note that this was stolen from 
# # http://stackoverflow.com/questions/26984414/efficiently-sorting-a-numpy-array-in-descending-order
# # http://stackoverflow.com/questions/14875248/python-numpy-sort-array
# sorted_range= np.sort(range)[::-1]
# sorted_range_index=np.argsort(range)[::-1]
# print "range", range
# print "sorted range", sorted_range
# print "indexes", sorted_range_index
# print "original keys", featuredict.keys()
# print "original items", featuredict.items()
# sorted_range_keys=[featuredict.keys()[i] for i in sorted_range_index]
# sorted_range_values=[float(featuredict.values()[i]) for i in sorted_range_index]
# sorted_range_ranges=[range[i] for i in sorted_range_index]
# sorted_range_centroids=[centroids[:,i].tolist() for i in sorted_range_index]
# #flattened = [val for sublist in list_of_lists for val in sublist]
# 
# 
# #t=[i[0] for i in sorted_range_centroids for i in [l] ]	
# # t=[entry[0] for entry in i for l in sorted_range_centroids]
# 		
# # print "the keys", sorted_range_keys
# # print "the values", sorted_range_values
# # print "the ranges", sorted_range_ranges
# print "the original range", sorted_range_centroids
# 
# #now that were doing it this way, we could have sorted on the list in the first place
# #but its whatevs at this point
# result=zip(sorted_range_ranges, sorted_range_centroids, sorted_range_keys, sorted_range_values)
# print "result", result
# 
# endtime=time.time()
# print "Finished. the threshold was {}, this took us {} minutes".format(threshold, (endtime - starttime)/60)
# 
# #exclude too low categories
# #express as: percentage of category, percentage of cluster, distance from centroid


