import os, re,shutil,string,numpy,nltk,codecs, scipy, scipy.cluster, numpy as np, time
from collections import defaultdict
from nltk.tokenize import word_tokenize

print "start"
starttime=time.time()
print "\n---------------\nSome public service announcements"

#moving parts
topdir=os.path.join("/Users/ps22344/Downloads","craig_0208")
folders=[i for i in os.listdir(topdir) if not i.startswith(".")]
##we establish the number of clusters we want
clusters=range(0,4)
## the number of times a word needs to occur to be included in the featuredict
threshold=1000

## stat settings
#how many times do we need to see a category for it to be included in the stats
catthreshold=10

print "we have {} folders".format(len(folders))

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

#this is our general vocab
vocab={}

#collecting words
for folder in folders:
    pathi=os.path.join(topdir, folder)
    filis=[i for i in os.listdir(pathi) if not i.startswith(".")]
    print "building vocab: we have {} files in folder {}".format(len(filis), folder)
    #collect a dictionary with all words
    #lowercase them    
    for fili in filis[:100]:
        inputfile=codecs.open(os.path.join(pathi, fili), "r", "utf-8").read()
        inputtext=adtextextractor(inputfile, fili)
        splittext=nltk.word_tokenize(inputtext)
        splittextlo=[i.lower() for i in splittext]
        #do we want to lemmatize or things like that
        for word in splittextlo:
            if word not in vocab:
                vocab[word]=1
            else:
                vocab[word]=vocab[word]+1

print "Our vocab has {} entries".format(len(vocab))

#here we set the threshold
featuredict= {key:value for key, value in vocab.items() if value > float(threshold) }
print "Our feature dictinoary has {} entries".format(len(featuredict))

#constructing matrix
wordmatrix=np.empty(shape=(1,len(featuredict)+1))
print "Matrix initial shape: ", np.shape(wordmatrix)

# making a dictionary for the categories
catdicti={}
catnumber=0

#
###BUILDING MATRICES
#

for folder in folders:
    pathi=os.path.join(topdir, folder)
    filis=[i for i in os.listdir(pathi) if not i.startswith(".")]
    print "Building matrices: we have {} files in folder {}".format(len(filis), folder)
    #collect a dictionary with all words
    #lowercase them    
    for fili in filis[:100]:
        inputfile=codecs.open(os.path.join(pathi, fili), "r", "utf-8").read()
        inputtext=adtextextractor(inputfile, fili)
        # lets establish the category
        # we need to make it numeric, so the numpy won't screw up
        try: 
        	cat=catdicti[tagextractor(inputfile, "category1", fili)]
        except:
        	print "We added something to the category dictionary"
        	catdicti[tagextractor(inputfile, "category1", fili)]=catnumber
        	catnumber=catnumber+1
        	cat=catdicti[tagextractor(inputfile, "category1", fili)]
        #we tokenize. note that punctuation is still in here
        splittext=nltk.word_tokenize(inputtext)
        # we lowercase
        splittextlo=[i.lower() for i in splittext]
        #number of "words"
        wordcount=float(len(splittextlo))
        # we make the vector for this file
        wordvector=np.array([float(cat)]+[float(splittextlo.count(i))/wordcount for i in featuredict])
        #print wordvector
        #we append it to the matrix
        wordmatrix=np.append(wordmatrix, [wordvector], axis=0)

print catdicti
print "features of word matrix: shape {}, dtype {}".format(np.shape(wordmatrix), wordmatrix.dtype)
print "---------------\nEnd of public service announcements\n\n"

#In 2D, the first dimension corresponds to rows, the second to columns.
# we don't look at the first row cause that was just for initialization
# the one without cats we put into the clustering algorithm
wordmatrix_without_cat=wordmatrix[1:wordmatrix.shape[0],1:wordmatrix.shape[1]]
wordmatrix_with_cat=wordmatrix[1:wordmatrix.shape[0],]
# print wordmatrix_without_cat[0:4,]
# print "\n----\n"
# print wordmatrix_with_cat[0:4,]

centroids, labels=scipy.cluster.vq.kmeans2(wordmatrix_without_cat, len(clusters), minit='points')
# 
# #note that labels are for a specific line in the data
# #we can see if cluster is consistent re certain data points
labellist=labels.tolist()


# for c in clusters:
#     print "For cluster {} there are {} items".format(c, labellist.count(c))
    
#check out the groups within in each cluster
labellist_enum=enumerate(labellist)

#
###CLUSTERSTATS
#
print "\n---------------\nThe makeup of clusters:\n"
# we connect labels to category of entry
# remember that labellist_enum consists of tuples where i[0] is the 
# list index and i[1] the value, i.e. the number of the cluster

#clustercounts collects a list with the items for each cluster
clustercounts=defaultdict(list)
for i in labellist_enum:
 	clustercounts[i[1]].append(wordmatrix_with_cat[i[0],0])

#clusterstats contains the statistics of each cluster
clusterstats=defaultdict()

for i in clustercounts:
	print "Cluster {} contains {} items".format(i, len(clustercounts[i]))
	#this dict comprehension makes a sub dict for each cluster:
	#CLUSTER: {cat1: {count:x, alias:x}, cat2: {ibid}...}
	#e.g. 0 {u'w4w': {'count': 111, 'percentage': 32.080924855491325, 'code': 5}, u'm4w': {'count': 6 ...
	clusterstats[i]={c: {
	'code':catdicti[c],
	'count':clustercounts[i].count(catdicti[c]),
	'percentage':float(clustercounts[i].count(catdicti[c]))/len(clustercounts[i])*100
	} 
	for c in catdicti}
	
print "\n---------------\nThe stats of clusters:\n"

for i in clusterstats:
	print "CLUSTER ",i, ":"
	for c in clusterstats[i]:
		if clusterstats[i][c]['count'] > catthreshold:
			print "category {:>5}, coded as {:>4}: {:>4} items, or {:>4} percent of the cluster".format(
			c,
			clusterstats[i][c]['code'],
			clusterstats[i][c]['count'],
			round(clusterstats[i][c]['percentage'])
			)
	print "\n---\n"
		
#
###CATEGORYSTATS
#
catstats=defaultdict()
#for each cat in the catdicti, we collect the total count
for i in catdicti:
	catstats[i]={str(c): clusterstats[c][i]['count'] for c in clusterstats}
	catstats[i]['total']=sum(catstats[i].values())


print "\n---------------\nThe stats of categories:\n"
	
for i in catstats:	
	if catstats[i]['total'] > catthreshold:
		print "CATEGORY ",i.upper(), ":"
		for c in clusters:
			c=str(c)
			print "cluster {:>2} contains {:>5} out of {:>5} items in this category, or {:>4} percent of the total".format(
			c,
			catstats[i][c], 
			catstats[i]['total'],
			round(float(catstats[i][c])/catstats[i]['total']*100)
			)
		print "\n---\n"
	# 	if clusterstats[i][c]['count'] > catthreshold:
# 			print "category {:>5}, coded as {:>4}: {:>4} items, or {:>4} percent of the cluster".format(
# 			c,
# 			clusterstats[i][c]['code'],
# 			clusterstats[i][c]['count'],
# 			round(clusterstats[i][c]['percentage'])
# 			)
# 	print "\n---\n"
	
# 	total.append([clusterstats[c][i]['count'] for c in clusterstats])
# 	print total
	
# 	for c in catdicti:
# 		clusterstats[i]=(c, catdicti[c], clustercounts[i].count(catdicti[c]), 
# 			round(float(clustercounts[i].count(catdicti[c]))/len(clustercounts[i])*100))
# 		if clustercounts[i].count(catdicti[c]) > catthreshold:
# 			
# 		# better to make new data file?
# 			print "category {}, coded as {}: {} items, or {} percent of the cluster".format(c, 
# 			catdicti[c], clustercounts[i].count(catdicti[c]), 
# 			round(float(clustercounts[i].count(catdicti[c]))/len(clustercounts[i])*100))
# 	print clusterstats
# 	print "\n-------\n"

# 			
# 		else:
# 			continue
# # 
# for i in clustercounts:
# 	print i 
# 	for c in clusters:
# 		print c
# 		print clustercounts[i].count(float(c))
# 	print "\n---\n"
# 
# stats=defaultdict(dict)	
# for i in clusters:
# 	print i
# 	for s in set(clustercounts[float(i)]):
# 		print set(clustercounts[float(i)])
# 		stats[i][s] = clustercounts[float(i)].count(s)
# #better to give percentage for each category
# # how many of category 1 are in cluster x?	
# for cluster in stats:
# 	print "for cluster {} we have the following stats: {}".format(cluster, stats[cluster])
# # for i in labellist_enum:
# # 	if i[1] == 3:
# # 		print i[1]


# for c in clusters:
# 	print c
# 	if l
# 	contents=[wordmatrix_with_cat [i[0]][0] for i in labellist_enum if i[1] == float(c)]
# 	print len(contents)





#calculate distance to centroid

endtime=time.time()
print "Finished. the threshold was {}, this took us {} seconds".format(threshold, endtime - starttime)

#exclude too low categories
#express as: percentage of category, percentage of cluster, distance from centroid


