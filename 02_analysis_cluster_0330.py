import os, re,shutil,string,numpy,nltk,codecs, scipy, scipy.cluster, numpy as np, time
from collections import defaultdict
from nltk.tokenize import word_tokenize

print "start"
starttime=time.time()
#moving parts
topdir=os.path.join("/Users/ps22344/Downloads","craig_0208")
folders=[i for i in os.listdir(topdir) if not i.startswith(".")]
##we establish the number of clusters we want
clusters=range(0,4)
## the number of times a word needs to occur to be included in the featuredict
threshold=1000

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
#this is our general vocab
vocab={}


#collecting words
for folder in folders:
    pathi=os.path.join(topdir, folder)
    filis=[i for i in os.listdir(pathi) if not i.startswith(".")]
    print "building vocab: we have {} files in folder {}".format(len(filis), folder)
    #collect a dictionary with all words
    #lowercase them    
    for fili in filis:
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

print "our vocab has {} entries".format(len(vocab))

#here we set the threshold
featuredict= {key:value for key, value in vocab.items() if value > float(threshold) }
print "our featuredict has {} entries".format(len(featuredict))

#constructing matrix
wordmatrix=np.empty(shape=(1,len(featuredict)+1))
print "matrix initial shape", np.shape(wordmatrix)

# making a dictionary for the categories
catdicti={}
catnumber=0

for folder in folders:
    pathi=os.path.join(topdir, folder)
    filis=[i for i in os.listdir(pathi) if not i.startswith(".")]
    print "building matrices: we have {} files in folder {}".format(len(filis), folder)
    #collect a dictionary with all words
    #lowercase them    
    for fili in filis:
        inputfile=codecs.open(os.path.join(pathi, fili), "r", "utf-8").read()
        inputtext=adtextextractor(inputfile, fili)
        # lets establish the category
        # we need to make it numeric, so the numpy won't screw up
        try: 
        	cat=catdicti[tagextractor(inputfile, "category1", fili)]
        except:
        	print "this is not in here"
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

for c in clusters:
    print "For cluster {} there are {} items".format(c, labellist.count(c))
    
#check out the groups within in each cluster
labellist_enum=enumerate(labellist)
# we connect labels to entries that contain a category
# remember that labellist_enum consists of tuples where i[0] is the 
# list index and i[1] the value, i.e. the number of the cluster
clustercounts=defaultdict(list)
for i in labellist_enum:
	#print i[1]
	clustercounts[i[1]].append(wordmatrix_with_cat[i[0],0])


for i in clustercounts:
	print i 
	for c in clusters:
		print c
		print clustercounts[i].count(float(c))
	print "\n---\n"

stats=defaultdict(dict)	
for i in clusters:
	print i
	for s in set(clustercounts[float(i)]):
		print set(clustercounts[float(i)])
		stats[i][s] = clustercounts[float(i)].count(s)
#better to give percentage for each category
# how many of category 1 are in cluster x?	
for cluster in stats:
	print "for cluster {} we have the following stats: {}".format(cluster, stats[cluster])
# for i in labellist_enum:
# 	if i[1] == 3:
# 		print i[1]


# for c in clusters:
# 	print c
# 	if l
# 	contents=[wordmatrix_with_cat [i[0]][0] for i in labellist_enum if i[1] == float(c)]
# 	print len(contents)





#calculate distance to centroid

endtime=time.time()
print "finished. the threshold was {}, this took us {} seconds".format(threshold, endtime - starttime)

#exclude too low categories
#express as: percentage of category, percentage of cluster, distance from centroid


