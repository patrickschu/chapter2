####
##set up 4 dictis
##extract category
##access right dicti
##count
##
##
##after 4 dictis are made
##writen them?
##compare pairwise
##
##m4m vs m4w vs w4w vs w4m
##m4w vs w4w vs w4m
##w4w vs w4m

#compare to general population first
# we make dicts for each category

import os
import re
import codecs
from collections import defaultdict
import shutil
import string
import numpy
import nltk
from nltk.tokenize import word_tokenize

print "start"
os.chdir("C://")

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
    
#read in the files

#set up top dir
inputname="craig_0208"
directory=os.path.join("Users","ps22344","Downloads",inputname)
print directory
outputdir=os.path.join("Users","ps22344","Downloads","craig_0210")

outputname="corpusdict_0210.txt"
outputfile=os.path.join("Users","ps22344","Downloads", outputname)

output=codecs.open(outputfile, "a")
#read in subdir, make file list
#subdirs=os.listdir(directory)
subdirs=[s for s in os.listdir(directory) if not s.startswith("\.")]
subdirs=["files9_output_0102"]


##these are our NLTK options
##from nltk.tokenize.simple   import (SpaceTokenizer, TabTokenizer, LineTokenizer,
##                                    line_tokenize)
##from nltk.tokenize.regexp   import (RegexpTokenizer, WhitespaceTokenizer,
##                                    BlanklineTokenizer, WordPunctTokenizer,
##                                    wordpunct_tokenize, regexp_tokenize,
##                                    blankline_tokenize)
##from nltk.tokenize.punkt    import PunktSentenceTokenizer
##from nltk.tokenize.sexpr    import SExprTokenizer, sexpr_tokenize
##from nltk.tokenize.treebank import TreebankWordTokenizer
##from nltk.tokenize.stanford import StanfordTokenizer
##from nltk.tokenize.texttiling import TextTilingTokenizer
##from nltk.tokenize.casual   import (TweetTokenizer, casual_tokenize)
##from nltk.tokenize.mwe      import MWETokenizer

#from nltk.tokenize import word_tokenize
count=0
dicti=defaultdict(int)
catdicti=defaultdict(lambda:defaultdict(int))
for sub in subdirs:
    print sub
#   #filis=os.listdir(directory+"/"+item)
    filis=[f for f in os.listdir(directory+"/"+sub) if not f.startswith(".")]

# ## we iterate over the list of files
    for fili in filis:
        inputfile=os.path.join(directory, sub, fili)
        inputi=codecs.open(inputfile, "r", "utf-8").read()
        
        #we extract category, gender, plat versus ad for now
        category=tagextractor(inputi, "category1", inputfile)
        gender=tagextractor(inputi, "gender", inputfile)
        adtype=tagextractor(inputi, "plat", inputfile)
        
        #getting text length
        text1=adtextextractor(inputi, inputfile)
        #remove html tags
        text2=re.sub("<.*/?>", " ", text1)
        text=word_tokenize(text2)
        # alot of items are just punctuation. needs to go.
        text = [w.lower() for w in text if not re.search("\W+", w)]
        for word in text:
            dicti[word]=dicti[word]+1
            catdicti[word][category]=catdicti[word][category]+1
            #print catdicti
    
        
##        if count < 20:
##            print fili, length, text[10:20]
##            count+=1
        
        #output.write(inputfile+","+category+","+gender+","+adtype+","+str(length)+"\n")


print "lenght of dict", len(dicti)
print "length of catdict", len(catdicti)

#calculate frequency for each entry
# hwo do we calculate the tokens per cat???
cats=[catdicti[e].keys() for e in catdicti]
flatcats=[i for sublist in cats for i in sublist]
setcats=set(flatcats)
print t
print "len cats", len(cats)
print "len flattened", len(flatcats)
print "len set", len(setcats)

for cati in setcats:
    






##for item in catdicti:
##    for thing in catdicti[item]:
##        print catdicti[item][thing]
#print sum(dicti.values())

#print sum(catdicti.values())

#sorteddicti=sorted(dicti, key=dicti.get, reverse=True)
sorteddicti=sorted(dicti.items(), key=lambda x: x[1], reverse=True)
#print type(sorteddicti)
#note that sorteddicti becomes a list! cause you cannot order a dict
##for entry in sorteddicti:
##    output.write(entry[0]+","+unicode(entry[1])+"\n")

#sum(t.values)
