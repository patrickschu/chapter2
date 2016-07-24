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
from collections import defaultdict
import operator

os.chdir("C://")
print "start"
print "this scripts looks at files that are shorter4 than 20 words and thus escaped before"

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
#set up top dir
inputname="craig_0204_2"
directory=os.path.join("Users","ps22344","Downloads",inputname)
print directory
outputdir=os.path.join("Users","ps22344","Downloads","craig_0205")

outputname="corpusstats_0204.txt"
outputfile=os.path.join("Users","ps22344","Downloads", outputname)

#this dict collects 20 word chunks 
textdicti=defaultdict(list)
count=0


#read in subdir, make file list
subdirs=[s for s in os.listdir(directory) if not s.startswith(".")]
#subdirs=["files9_output_0102"]
#print subdirs


for sub in subdirs:
    print sub
#   #filis=os.listdir(directory+"/"+item)
    filis=[f for f in os.listdir(directory+"/"+sub) if not f.startswith(".")]
# ## we iterate over the list of files
    for fili in filis:
        inputfile=os.path.join(directory, sub, fili)
        input=codecs.open(inputfile, "r", "utf-8").read()
        
        #we extract category, gender, plat versus ad for now
        category=tagextractor(input, "category1", inputfile)
        gender=tagextractor(input, "gender", inputfile)
        adtype=tagextractor(input, "plat", inputfile)
        
        #getting text length
        text1=adtextextractor(input, inputfile)
        #remove html tags
        text2=re.sub("<.*/?>", " ", text1)
        #split text on whitespace, comma, stop
        #maybe only btw characters?
        #this we steal from nltk word_tokenize
        #(?:[?!)\";}\]\*:@\'\({\[])
        text=re.split("(?:\s|\W)+", text2.lower())
        if len(text) < 20 and len(text) > 9:
                count=count+1
                #print text, inputfile
                snippet="".join(text[:10])
                textdicti[snippet].append((inputfile, len(text)))

print "textdicti", len(textdicti)
### we sort each entry by length so we keep the longest text
for item in textdicti:
  textdicti[item].sort(key=operator.itemgetter(1), reverse=True)



for item in textdicti:
  if len(textdicti[item]) > 1:
      print item
      entry=textdicti[item]
      print entry
      for e in entry [1:len(entry)]:
          os.remove(e[0])
          print "deleted", e[0]
      count=count+1
        
print "aha", count
        
print ('\a')
os.system('say "your program has finished"')
        

