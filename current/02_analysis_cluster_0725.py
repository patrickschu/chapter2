# -*- coding: utf-8 -*-

import clustertools as ct
import sys
import os
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


#moving parts
chapterdir=os.path.split(os.getcwd())
#PRONOUNS
perspronouns=[u'i', u'me', u'we', u'you', u'he', u'him',  u'she', u'her', u'it', u'they', 'them',  u'myself', u'ourselves',  u'yourself', u'yourselves',  u'himself',  u'herself', u'itself', u'themselves', u'who', u'whom', "im"]
dempronouns=[u'that', u'these', u'those']
pospronouns=[u'my', u'our', u'ours', u'your', u'yours', u'his', u'her', u'hers',u'its',  u'their', u'theirs' ]
#VERBS
beverb=[u'am', u'is', u'are', u'was', u'were', u'be', u'been', u'being', u'isn', u'wasn', u'weren', u'won', u'ain', u'aren', u're', u'm', u's', "\'m", "'s", "'re", "im"]
haveverb=[u'have', u'has', u'had', u'having', u'hadn', u'hasn', u'haven', u've', u'd', "'d", "'ve"]
doverb=[u'do', u'does', u'did', u'doing', u'didn', u'doesn', u'don']
modals=[u'mightn', u'mustn', u'needn', u'shan', u'shouldn',  u'wouldn',  u'couldn', u'should',u'can']
negation=[u'mightn', u'mustn', u'needn', u'shan', u'shouldn',  u'wouldn',  u'couldn', u'no', u'nor', u'not', u't', "n\'t"]
aux=[u'll', u'will', "'ll"]
#MISC
prepsandarts=[u'of', u'at', u'by', u'for', u'with', u'about', u'against', u'between', u'into', u'through', u'during', u'before', u'after', u'above', u'below', u'to', u'from', u'up', u'down', u'in', u'out', u'on', u'off', u'over', u'under', u'a', u'an', u'the']
conjuncts=[u'and', u'but', u'if', u'or', u'because', u'as', u'until', u'while']
adverbsandadjects=['again', u'further', u'then', u'once', u'here', u'there',u'when', u'where', u'why', u'how', u'all', u'any', u'what', u'which',  u'this'] 
intensifiers=[u'few', u'more', u'most', u'too', u'very', u'than']
questions=[u'when', u'where', u'why', u'how']
leftovers=[u'all', u'any', u'both', u'each',u'other', u'some', u'such', u'only', u'own', u'same', u'so', u'just', u'now', u'o', u'y', u'ma']



	
stopwords = stopwords.words('english')+["n\'t","\'m", "br/", "'s", "'ll", "'re", "'d", "amp", "'ve","us", "im"]
stopwords = ct.remover(stopwords, [])
print "stopwords", stopwords, "\n\n"

punctuation= list(string.punctuation)+["''", "``", "br/"]
print "punctuation", punctuation, "\n\n"

metriclist=[['cityblock', 'cosine', 'euclidean', 'l1', 'l2', 'manhattan'],['braycurtis', 'canberra', 'chebyshev', 'correlation', 'dice', 'hamming', 'jaccard', 'kulsinski', 'mahalanobis', 'matching', 'minkowski', 'rogerstanimoto', 'russellrao', 'seuclidean', 'sokalmichener', 'sokalsneath', 'sqeuclidean', 'yule']]
scipy_distances=['euclidean', 'minkowski', 'cityblock', 'seuclidean', 'sqeuclidean', 'cosine', 'correlation','hamming', 'jaccard', 'chebyshev', 'canberra', 'braycurtis', 'mahalanobis', 'yule', 'matching', 'dice', 'kulsinski', 'rogerstanimoto', 'russellrao', 'sokalmichener', 'sokalsneath', 'wminkowski']

print "start"
print "\n---------------\nSome public service announcements"


pathi=os.path.expanduser(os.path.join("~/", "Downloads", "craigbalanced_0601"))


##
###COUNTING WORDS
##
def dictmaker(folderlist, threshold, remove_stopwords=True, remove_punct=True):
	"""
	The dictmaker counts the words / items contained in the files found in the folders of folderlist.
	It returns a dictionary of all words that occur more often than the number threshold. 
	remove_stopwords used the stopword list defined above to ignore words. 
	remove_punct works with string.punctuation, cf above. 
	"""
	#threshold sets how many times a word needs to occur to be included in the featuredict
	vocab={}
	for folder in folderlist:
		filis=[i for i in os.listdir(os.path.join(pathi,folder)) if not i.startswith(".")]
		print "Building vocab: we have {} files in folder {}".format(len(filis), folder)
		#collect a dictionary with all words
		#lowercase them    
		for fili in filis:
			inputfile=codecs.open(os.path.join(pathi, folder, fili), "r", "utf-8").read()
			inputtext=ct.adtextextractor(inputfile, fili)
			splittext=nltk.word_tokenize(inputtext)
			splittextlo=[i.lower() for i in splittext]
			#do we want to lemmatize or things like that
			for word in splittextlo:
				if word not in vocab:
					vocab[word]=1
				else:
					vocab[word]=vocab[word]+1
	print "Our vocab dictionary has {} entries".format(len(vocab))
	ct.dictwriter(os.path.join("~/", chapterdir[0], "outputfiles", "fulldict_"+time.strftime("%H_%M_%m_%d")), vocab)
	if remove_stopwords:
		vocab= {key:value for key, value in vocab.items() if key not in stopwords }
		print "After stop word removal, dict is {} long".format(len(vocab))
	if remove_punct:
		vocab= {key:value for key, value in vocab.items() if key not in punctuation }
		print "After punctuation removal, dict is {} long".format(len(vocab))
	featuredict= {key:value for key, value in vocab.items() if value > float(threshold) }
	print "Our feature dictionary has {} entries\n---------------\n".format(len(featuredict))
	print "This is our featuredict", featuredict
	ct.dictwriter(os.path.join("~/", chapterdir[0], "outputfiles", "featuredict_"+time.strftime("%H_%M_%m_%d")), featuredict)
	return featuredict
	
##
###FINDING CATEGORIES
##this extracts the categories from our files
def categorymachine(folderlist):

	print "starting category machine"
	catdicti={}
	catnumber=0
	for folder in folderlist:
		filis=[i for i in os.listdir(os.path.join(pathi,folder)) if not i.startswith (".")]
		for fili in filis:
			inputfile=codecs.open(os.path.join(pathi, folder,fili), "r", "utf-8").read()
			inputtext=ct.adtextextractor(inputfile, fili)
			#lets establish the category
			#we need to make it numeric, so the numpy won't screw up
			category=ct.tagextractor(inputfile, "category1", fili)
			try: 
				cat=catdicti[category]
			except:
				print "We added {} to the category dictionary, coded as {}".format(category, catnumber)
				catdicti[ct.tagextractor(inputfile, "category1", fili)]=catnumber
				catnumber=catnumber+1
				cat=catdicti[ct.tagextractor(inputfile, "category1", fili)]
	return (catdicti, catnumber)

##
###BUILDING MATRICES
##
def matrixmachine(folderlist, featuredict, testmode, *args):

	"""
	The matrixmachine creates matrices of word frequencies / item frequencies.
	It returns 
	wordmatrix_without_cat, a matrix of word frequencies only. This is fed into clustering.
	wordmatrix_with_cat, a matrix of word frequencies, where external categories (defined in *args) are added. For later comparison of clusterings. 
	catdicti, a dictionary that maps categories to numbers used in the wordmatrix_with_cat. Created by the categorymachine(), cf for details. 
	filedict, a dictioanry that maps file names to rows in the matrix. For later comparison of clusterings. 
	It takes
	The folderlist is a collection of folders to iterate over. 
	The featuredict is a dictionary containing the words to count.
	If testmode is set to True, a short test run on a fragment of the dataset is conducted to see if this will run all the way. 
	(Note that the testmode comes all the way from main())
	The args are a number of external categories, each defined in the categorydicti created by categorymachine(). Here, usually a gender category. 
	Args will be added to the matrix_with_cat. 
	"""
	print "Starting the matrixmachine"
	print "external categories: ", len(args)
	print args
	#the plus one in here is for the file id
	wordmatrix=np.empty(shape=(1,(len(featuredict)+len(args)+1)))
	print "Matrix initial shape: ", np.shape(wordmatrix)
	# making a dictionary for the categories
	# we need the zero cause the machine returns 2 items
	count=0
	catdicti=categorymachine(folderlist)[0]
	filedict={}
	featuredict=featuredict.keys()
	for folder in folderlist:
		filis=[i for i in os.listdir(os.path.join(pathi, folder)) if not i.startswith(".")]
		if testmode == True:
			print "\n\nRUNNING\nIN\nTEST\nMODE\n"
			filis=filis[:200]
		print "Building matrices: we have {} files in folder {}".format(len(filis), folder)
		for fili in filis:
			inputfile=codecs.open(os.path.join(pathi, folder, fili), "r", "utf-8").read()
			#establish category
			for external_cat in args:
				cat=catdicti[ct.tagextractor(inputfile, external_cat, fili)]
			count=count+1
			filedict[count]=os.path.join(pathi, folder, fili)
			#note that punctuation is still in here
			splittext=nltk.word_tokenize(inputfile)
			splittextlo=[i.lower() for i in splittext]
			wordcount=float(len(splittextlo))
			# this is a per word frequency
			wordvector=np.array([float(cat)]+[float(count)]+[float(splittextlo.count(i))/wordcount for i in featuredict])
			#print wordvector
			#we append it to the matrix
			wordmatrix=np.append(wordmatrix, [wordvector], axis=0)
	print "Features of word matrix: shape {}, dtype {}".format(np.shape(wordmatrix), wordmatrix.dtype)
	print "---------------\nEnd of public service announcements\n\n"
	#"In 2D, the first dimension corresponds to rows, the second to columns."
	# we don't look at the first row cause that was just for initialization
	# the one without cats we put into the clustering algorithm
	wordmatrix_without_cat=wordmatrix[1:wordmatrix.shape[0],len(args)+1:wordmatrix.shape[1]]
	print "without", np.shape(wordmatrix_without_cat)
	wordmatrix_with_cat=wordmatrix[1:wordmatrix.shape[0],]
	print "with", np.shape(wordmatrix_with_cat)
	return (wordmatrix_without_cat, wordmatrix_with_cat, catdicti, filedict)

##	
###CREATING CLUSTERS
#this makes clusters; takes the dataset (matrix) and the algorithm
def clustermachine(matrix, distance_metric, clusters=4):
	"""
	The clustermachine takes a matrix with word freqs and clusters according to the distance_metric. 
	Clusters sets the input if algorithm needs a pre-determined number of clusters. 
	Last two will not be used by all algorithms. 
	"""
	no_of_clusters=range(clusters)	
	result=[]
	t=time.time()
	
	## # 1: kmeans
# 	for x in [2,4,6,8,10]:
# 		model=sklearn.cluster.KMeans(x,tol=0)
# 		clustering=model.fit(matrix)
# 		centroids=clustering.cluster_centers_
# 		labels=clustering.labels_
# 		inertia=clustering.inertia_
# 		kmeans=ct.Clustering(model, clustering.labels_, clustering.cluster_centers_)
# 		result.append(kmeans)
# 		print [i.name for i in result][len(result)-1], [i.no_of_clusters for i in result][len(result)-1]
# 		u=time.time()
# 		print (u-t)/60
# 		#


#	## #2: MeanShift, takes forever @  12600, 42
#	model=sklearn.cluster.MeanShift()
#	clustering=model.fit(matrix)
#	centroids=clustering.cluster_centers_
#	labels=clustering.labels_
#	meanshift=ct.Clustering(model, clustering.labels_, clustering.cluster_centers_)
#	result.append(meanshift)
#	u=time.time()
#	print [i.name for i in result][len(result)-1]
#	print (u-t)/60
#	
	# 3: Affinity Propagation, breaks @ 12600, 42
# 	model=sklearn.cluster.AffinityPropagation()
# 	clustering=model.fit(matrix)
# 	centroid_index=model.cluster_centers_indices_
# 	centroids=clustering.cluster_centers_
# 	labels=clustering.labels_
# 	aff_matrix=clustering.affinity_matrix_
# 	its= clustering.n_iter_
# 	affinity=ct.Clustering(model, clustering.labels_, clustering.cluster_centers_)
# 	result.append(affinity)
# 	u=time.time()
# 	print [i.name for i in result][len(result)-1], [i.no_of_clusters for i in result][len(result)-1]
# 	print (u-t)/60
	
# 	## #4: Spectral clustering
# 	model=sklearn.cluster.SpectralClustering()
# 	clustering=model.fit(matrix)
# 	labels=clustering.labels_
# 	aff_matrix=clustering.affinity_matrix_
# 	spectral= ct.Clustering(model, clustering.labels_)
# 	result.append(spectral)
# 	u=time.time()
# 	print [i.name for i in result][len(result)-1], [i.no_of_clusters for i in result][len(result)-1]
# 	print (u-t)/60


##watch out --------- centroids are indices!!!!!

	
	# ## # 5: DBCASN,  takes forever @  12600, 42
# 	for x in [2,4,8,16,32]:#[0.175, 0.2, 0.225, 0.3]:
# 		model=sklearn.cluster.DBSCAN(eps=x, metric=distance_metric, algorithm='brute')
# 		clustering=model.fit(matrix)
# 		core_samples=clustering.core_sample_indices_
# 		#print "core samples", matrix[clustering.core_sample_indices_]
# 		components=clustering.components_
# 		print "components", len(components)
# 		labels=clustering.labels_
# 		print labels
# 		dbscan= ct.Clustering(model, clustering.labels_, matrix[clustering.core_sample_indices_])
# 		result.append(dbscan)
# 		u=time.time()
# 		print [i.name for i in result][len(result)-1], [i.no_of_clusters for i in result][len(result)-1]
# 		print (u-t)/60
#	
#	##GUASSIN DOEs NOT FIT OUR SCHEMA AT THIS POINT
#	## 6: GAUSSIAN MIXTURE.
# 	for x in [2,4,6,8,12,16,20,24]:
# 		model=sklearn.mixture.DPGMM(x, n_iter=100, verbose=0)
# 		print "initial weights", model.weights_
# 		print "initial components", model.n_components
# 		print "initial converge", model.converged_
# 		model.fit(matrix)
# 		print "trained weights", model.weights_
# 		print "trained components", model.n_components
# 		print "trained converge", model.converged_
# 		print "\n predict", model.predict(matrix)
# 		print "means", model.means_
# 		#print "\n predict probs", model.predict_proba(matrix)
# 		dirichlet= ct.Clustering(model, model.fit_predict(matrix), model.means_)
#  		u=time.time()
#  		result.append(dirichlet)
#  		print (u-t)/60
# 		
# 	for x in [2,4,8,16,32]:
# 		model=sklearn.mixture.GMM(x, n_iter=500, verbose=0)
# 		print "initial weights", model.weights_
# 		print "initial components", model.n_components
# 		print "initial converge", model.converged_
# 		model.fit(matrix)
# 		print "trained weights", model.weights_
# 		print "trained components", model.n_components
# 		print "trained converge", model.converged_
# 		print "\n predict", model.predict(matrix)
# 		print "means", model.means_
# 		#print "\n predict probs", model.predict_proba(matrix)
# 		gauss= ct.Clustering(model, model.fit_predict(matrix), model.means_)
#  		u=time.time()
#  		result.append(gauss)
#  		print (u-t)/60
#	
#
	#These are essentially trees; maybe need a different approach. They are kinda predictive
	
# 	## #7: Agglomerative 
	for x in [4]:
		model=sklearn.cluster.AgglomerativeClustering(affinity=distance_metric, n_clusters=x, linkage='complete')
		clustering=model.fit(matrix)
		labels=clustering.labels_
		leaves=clustering.n_leaves_
		children=clustering.children_
		components=clustering.n_components_
		ward= ct.Clustering(model, clustering.labels_)
		result.append(ward)
		u=time.time()
		print [i.name for i in result][len(result)-1], [i.no_of_clusters for i in result][len(result)-1]
		print (u-t)/60
# # 	
# 
# 	print [i.name for i in result][len(result)-1], [i.no_of_clusters for i in result][len(result)-1]
# 	print (u-t)/60

	
	
	
# 	model=sklearn.cluster.AgglomerativeClustering(affinity='cosine', linkage='complete')
# 	clustering=model.fit(matrix)
# 	labels=clustering.labels_
# 	leaves=clustering.n_leaves_
# 	components=clustering.n_components_
# 	ward= ct.Clustering(model, clustering.labels_)
# 	result.append(ward)
# 	u=time.time()
# 	print [i.name for i in result][len(result)-1], [i.no_of_clusters for i in result][len(result)-1]
# 	print (u-t)/60

# 	## #8: Birch Hierarchical 	
# 	model=sklearn.cluster.Birch(threshold=0.025)
# 	clustering=model.fit(matrix)
# 	labels=clustering.labels_
# 	root=clustering.root_
# 	subcluster_labels=clustering.subcluster_labels_
# 	birch= ct.Clustering(model, clustering.labels_)
# 	result.append(birch)
# 	u=time.time()
# 	print [i.name for i in result][len(result)-1], [i.no_of_clusters for i in result][len(result)-1]
# 	print (u-t)/60
	
	return(result)

	#######MAIN#########
##
###MAIN
##
	 
def main(distance_metric, threshold, testmode=False):
	starttime=time.time()
	#make this flexible in case there are no subfolders
	folders=[i for i in os.listdir(pathi) if not i.startswith(".")]
	print ", ".join(folders)
	print "Items in folders", ", ".join([str(len(os.listdir(os.path.join(pathi,f)))) for f in folders])
	#folders=['files9_output_0102']#, 'files9_output_0102', 'files9_output_0102', 'files9_output_0102','files9_output_0102', 'files9_output_0102','files9_output_0102', 'files9_output_0102', 'files9_output_0102'] 
	print "We have {} folders".format(len(folders))
	featuredict=dictmaker(folders, threshold, remove_stopwords=True, remove_punct=True)
	
	wordmatrix_without_cat, wordmatrix_with_cat, catdicti, filedicti = matrixmachine(folders, featuredict, testmode, "category1")
	
	wordmatrix_without_cat, wordmatrix_with_cat=ct.matrixstats(wordmatrix_without_cat, wordmatrix_with_cat, distance_metric, zscores=False, outlier_removal=True, outlier_threshold = 2, median_metric='median')
	#apply to wordmatrix with cats
	
	x=clustermachine(wordmatrix_without_cat,distance_metric,4)
	#print [(i.name, i.no_of_clusters) for i in x]
	excludelist=['total','no_of_categories', 'no_of_clusters', 'no_of_cats']
	print "These clusterings have less than 2 clusters\n{}\n\n".format("\n".join([str(c.name) for c in x if c.no_of_clusters < 2]))
	#PRINTING STUFF
	headline="\n\n-----------\n\n"
	print "Working with {} distance metric".format(distance_metric)
		
	#CROSS CLUSTERING COMPARISON
	for clustering in [c for c in x if c.no_of_clusters > 1]:
		cati=ct.Categorystats(wordmatrix_with_cat, clustering.name, clustering.labels)
		sili=ct.Clusteringstats(wordmatrix_with_cat, wordmatrix_without_cat, clustering.name, clustering.labels).cluster_silhouette(distance_metric)
	
		#GENERAL STATS
		print headline, headline, "CLUSTERING CALLED {} HAS {} CLUSTERS". format(clustering.getname()[1], clustering.no_of_clusters)
		print "Its silhouette score is {}".format(str(sili))
		stats=ct.Clusteringstats(wordmatrix_with_cat, wordmatrix_without_cat, clustering.name, clustering.labels).size_of_clusters()
		catstats=ct.Clusteringstats(wordmatrix_with_cat, wordmatrix_without_cat, clustering.name, clustering.labels).cats_per_cluster()
		for cluster in stats:
			print "\nCluster {} contains {} items, {} % of the total".format(cluster, stats[cluster], round(float(stats[cluster])/len(wordmatrix_without_cat)*100))
			for cat in [i for i in catstats[cluster] if not i in excludelist]:
				print "{} items of category {} make up {} % of this cluster".format(catstats[cluster][cat], "".join([i[0] for i in catdicti.items() if i[1] == int(cat)]), round(catstats[cluster][cat]/catstats[cluster]['total']*100))
		cats=ct.Categorystats(wordmatrix_with_cat, clustering.name, clustering.labels).size_of_categories()
		
		#STATS PER CAT
		print headline,"Statistics per category"
		for cat in [i for i in cats if not i in excludelist]:
			print "\nCategory {} has {} items".format("".join([i[0] for i in catdicti.items() if i[1] == int(cat)]), cats[cat]['total'])
			for entry in [i for i in cats[cat]['cat_per_cluster'] if not i in excludelist]:
				print "{} items or {} percent in cluster {}".format(cats[cat]['cat_per_cluster'][entry], round(float(cats[cat]['cat_per_cluster'][entry])/float(cats[cat]['total'])*100), entry)

		#PREDICTIVE FEATURES
		print headline, "Strongly predictive features are"
		cents=ct.Centroidstats(wordmatrix_without_cat, clustering.name, clustering.labels, clustering.centroids).cluster_predictors(featuredict)
		if cents:
			for diff in cents:
				print "\nRaw Scores"
				print "Cluster {} and cluster {} are differentiated by \n{}\n\n\n".format(diff[0], diff[1], ", ".join([" : ".join(map(unicode, i[::-1])) for i in cents[diff]['raw_diff']][:10])) 
				print "Zscores"
				print "Cluster {} and cluster {} are differentiated by \n{}\n\n\n".format(diff[0], diff[1], ", ".join([" : ".join(map(unicode, i[::-1])) for i in cents[diff]['zscores_diff']][:10]))	
			
		
		#PROTOTYPES
		print headline, "Here is a typical document for each cluster"
		distance=distance_metric
		if distance_metric=='manhattan':
			distance='cityblock'
		print "We set the distance metric to {}".format(distance)
		docs=ct.Centroidstats(wordmatrix_without_cat, clustering.name, clustering.labels, clustering.centroids).central_documents(wordmatrix_with_cat, filedicti)
		if docs:
			for cluster in docs:
				print "\nCLUSTER {} \n".format(cluster)
				with open(docs[cluster][distance][0]) as f:
					print f.read()
				if len(docs[cluster][distance]) > 8:
					print "\nOther files close by in cluster {}:\n".format(cluster)
					print ("{}\n"*8).format(*docs[cluster][distance][1:9])
	print headline, "Comparing clusterings"
	for clustering in [c for c in x if c.no_of_clusters > 1]:
		print headline, "CLUSTERING CALLED {} HAS {} CLUSTERS". format(clustering.getname()[0], clustering.no_of_clusters)
		print "Its silhouette score is {}".format(str(ct.Clusteringstats(wordmatrix_with_cat, wordmatrix_without_cat, clustering.name, clustering.labels).cluster_silhouette(distance_metric)))
	#all input does it just concatenate name + cluster # and supply clustering object to similarity measurement
	input=[(str(type(i.name)).split(".")[3].rstrip("'>")+"--"+str(i.no_of_clusters), i) for i in x]
	simi=ct.Clusteringsimilarity(wordmatrix_with_cat, wordmatrix_without_cat ,input)
	options=['adjustedrand_sim', 'adjustedmutualinfo_sim', 'jaccard_sim', 'v_sim', 'completeness_sim', 'homogeneity_sim', 'silhouette_score_sim']
	for o in options:
		print "\n---\n"
		ct.Clusteringsimilarity(wordmatrix_with_cat, wordmatrix_without_cat ,input).similarity_matrix(o)
	
	
	print "\n---\n"
	endtime=time.time()
	process=endtime-starttime
	print headline, "This took us {} minutes".format(process/60)
		#or do we want to do predictive features and typical document per cluster as well????	
	os.system('say "your program has finished"')

for thre in [1000]:
	print "\n\n\n\n\n\n",thre,"\n"
	main('manhattan', thre, testmode=False)

