##go thru, for each extract tags and word coutn
##note that word count needs to be sophisticated cause just whitespace not gonna 
##cut it
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
inputname="craig_0204_2"
directory=os.path.join("Users","ps22344","Downloads",inputname)
print directory
outputdir=os.path.join("Users","ps22344","Downloads","craig_0205")

outputname="corpusstats_0204.csv"
outputfile=os.path.join("Users","ps22344","Downloads", outputname)

output=codecs.open(outputfile, "a")
#read in subdir, make file list
#subdirs=os.listdir(directory)
subdirs=[s for s in os.listdir(directory) if not s.startswith("\.")]
#subdirs=["files9_output_0102"]


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
        #split text on whitespace, comma, stop
        #maybe only btw characters?
        #text=re.split("(?:\s|\W)+", text2.lower())
        text=word_tokenize(text2)
        # alot of items are just punctuation. needs to go.
        text = [w for w in text if not re.search("\W+", w)]
        length=len(text)
##        if count < 20:
##            print fili, length, text[10:20]
##            count+=1
        
        output.write(inputfile+","+category+","+gender+","+adtype+","+str(length)+"\n")

output.close()
print "finish"
print ('\a')
os.system('say "your program has finished"')
        
