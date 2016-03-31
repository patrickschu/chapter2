import os, re,shutil,string,numpy,nltk,codecs, scipy, scipy.cluster, numpy as np
from collections import defaultdict
from nltk.tokenize import word_tokenize

print "start"
topdir="craig_0208"
folders=[i for i in os.listdir(os.path.join("F:", topdir)) if not i.startswith(".")]


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
    pathi=os.path.join("F:", topdir, folder)
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
featuredict= {key:value for key, value in vocab.items() if value > 7000 }
print "number of 'i'", featuredict['i']
print "our featuredict has {} entries".format(len(featuredict))
#constructing matrix
wordmatrix=np.empty(shape=(1,len(featuredict)))
##print wordmatrix
print "matrix initial shape", np.shape(wordmatrix)

for folder in folders:
    pathi=os.path.join("F:", topdir, folder)
    filis=[i for i in os.listdir(pathi) if not i.startswith(".")]
    print "building matrices: we have {} files in folder {}".format(len(filis), folder)
    #collect a dictionary with all words
    #lowercase them    
    for fili in filis:
        inputfile=codecs.open(os.path.join(pathi, fili), "r", "utf-8").read()
        inputtext=adtextextractor(inputfile, fili)
        #we tokenize. note that punctuation is still in here
        splittext=nltk.word_tokenize(inputtext)
        # we lowercase
        splittextlo=[i.lower() for i in splittext]
        #number of "words"
        wordcount=float(len(splittextlo))
        # we make the vector for this file
        wordvector=np.array([float(splittextlo.count(i))/wordcount for i in featuredict])
        #we append it to the matrix
        wordmatrix=np.append(wordmatrix, [wordvector], axis=0)

print "features of word matrix: shape {}, dtype {}".format(np.shape(wordmatrix), wordmatrix.dtype)


##we establish the number of clusters we want
clusters=range(0,4)

centroids, labels=scipy.cluster.vq.kmeans2(wordmatrix[1:len(wordmatrix)], len(clusters), minit='points')
#note that labels are for a specific line in the data
#we can see if cluster is consistent re certain data points
labellist=0
for i in clusters:
    print "For cluster {} there are {} items".format(i, labels.tolist().count(i))


