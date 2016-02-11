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

#
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
#    
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



#
#set up counts, dictis
count=0
#stores counts for each word
dicti=defaultdict(int)
#stores counts for each word by category
catdicti=defaultdict(lambda:defaultdict(int))
#stores the number of total words per category
wordcountdicti=defaultdict(int)

#
#iterate over files
subdirs=[s for s in os.listdir(directory) if not s.startswith("\.")]
ads=['adfiles2_output_0116',
'adfiles3_output_0116',
'adfiles4_output_0116',
'adfiles_output_0116']

stp=['files2_output_0102'
'files3_output_0102',
'files4_output_0102',
'files5_output_0102',
'files8_output_0102',
'files9_output_0102',
'files_output_0101']
#subdirs=["files9_output_0102"]


for sub in ads:
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
        #we enter each word intor our dictis
        for word in text:
            dicti[word]=dicti[word]+1
            catdicti[word][category]=catdicti[word][category]+1
    


#some prints to check on stuff
print "lenght of dict", len(dicti)
print "length of catdict", len(catdicti)

#calculate frequency for each entry
# hwo do we calculate the tokens per cat???
#we establish the categories we're dealing with by seeing which ones the
#loop above entered into the dictionary
cats=[catdicti[e].keys() for e in catdicti]
#flatten the list
flatcats=[i for sublist in cats for i in sublist]
#los the duplicates: this is the sets of categories we'll be looking at
setcats=set(flatcats)

print "len cats", len(cats)
print "len flattened", len(flatcats)
print "len set", len(setcats), setcats

total=0

#we iterate over our list of categories
#for each, we extract the entry for each word
for cati in setcats:
    wordcount=[catdicti[entry][cati] for entry in catdicti]
    print cati
    print "number of results", len(wordcount)
    print "word count", sum(wordcount)
    total=total+sum(wordcount)
    wordcountdicti[cati]=sum(wordcount)


print "total words", total
print wordcountdicti

##for item in catdicti:
##    print item, catdicti[item]
##    print wordcountdicti
##    break
    
#
#now we use the totals to transform the entries in the catdicti into frequencies
#lets get rid of zero entries first. they are annoying
for entry in catdicti:
    #print entry,  catdicti[entry]
    catdicti[entry]={k: float(v) for k, v in catdicti[entry].items() if v}
    #print  entry, catdicti[entry]
    
##    
for entry in catdicti:
    #print len(catdicti[entry])
    for i in catdicti[entry]:
       #print entry, catdicti[entry][i], catdicti[entry][i]/wordcountdicti[i]
       catdicti[entry][i]=catdicti[entry][i]/wordcountdicti[i]*1000000
       #print entry, catdicti[entry][i]#, catdicti[entry][i]/wordcountdicti[i]

##for item in catdicti:   
##    print item, catdicti[item]
##    #print wordcountdicti
##    break


##now its getting real: the division
# let's exclude all words < 100 from the overall dictionary
allwords=sum(dicti.values())
print "all", dicti['all']
print "allwords: ", allwords
print "length dicti", len(dicti)
dicti={k: (float(v)/allwords)*1000000 for k, v in dicti.items() if v > 99}
print "length dicti > 99", len(dicti)

#go thru the catdicti, and for each entry transform by subtracting from total
# some percentagewise transformation req'rd
## from the notes on box:
#take smaller value, divide by 100 to get 1 percent;
##difference / 1 percent == how bis is the difference percentagewise?
## our formula: category frequency - overall frequency = diff
##diff / (category frequency/100) --> puts it in percentages

faillist=[]

for entry in catdicti:
    for i in catdicti[entry]:
        try:
            #print  catdicti[entry][i]
        #print dicti[entry]
        #try:
            catdicti[entry][i]=(catdicti[entry][i]-dicti[entry])/(catdicti[entry][i]/100)
            print  entry, i, catdicti[entry][i]
            print dicti[entry], catdicti[entry]
            print "----\n\n"
        except KeyError , err:
            #print "key", err
            pass
            faillist.append((entry, i))
            #print err
            #print "assi"
    
print "faillist", len(faillist)





##for each word, we end up with a percentage difference
##for item in dicti:
##    print item, dicti[item]
##    break



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
