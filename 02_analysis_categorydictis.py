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

#calculating lexical distance
# our formula: category frequency - overall frequency = diff
#diff / (category frequency/100) --> puts it in percentages
#better: we move the whole distance business to a function
#
#this function takes two dictionaries with frequencies and relates those to each other
#computing what we might call distance
def distancemachine (name, freqs1, freqs2):
    result=defaultdict(float)
    for entry in freqs1:
        try:
            result[entry]= (freqs1[entry]-freqs2[entry])/(freqs1[entry]/100)
        except KeyError, err:
            faillist.append((err, name))
    return result


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
#faillist for keys that do not exist in dict during comparison
#has tuples with name of offending dicts and word
faillist=[]
#stores counts for each word
dicti=defaultdict(int)
#stores counts for each word by category
catdicti=defaultdict(lambda:defaultdict(int))
#stores the number of total words per category
wordcountdicti=defaultdict(int)
#stores the subset of catdicti for each category. kinda redundant, but who knew about this when
#we started?
compdicti=defaultdict(dict)

#
#iterate over files
subdirs=[s for s in os.listdir(directory) if not s.startswith(".")]
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


for sub in subdirs:
    print sub

    filis=[f for f in os.listdir(directory+"/"+sub) if not f.startswith(".")]
    # BUILDING THE DICTIONARIES
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

print "\n-------\n"

#some prints to check on stuff
#how many words in our overall dictionary?
print "lenght of dict", len(dicti)
#how many words in our dictionary by category?
print "length of catdict", len(catdicti)
print "\n-------\n"

##BUILDING FREQUENCY DICTIONARIES
#calculate frequency for each entry by category and population frequencies
#we establish the categories we're dealing with by seeing which ones the
#loop above entered into the dictionary. We  need this list so we can iterate over all categories below
cats=[catdicti[e].keys() for e in catdicti]
#flatten the list
flatcats=[i for sublist in cats for i in sublist]
#los the duplicates: this is the sets of categories we'll be looking at
setcats=set(flatcats)

#some prints to check on stuff
#how many categories did we find?
print "len cats", len(cats)
print "len flattened", len(flatcats)
#here are the categories
print "len set", len(setcats), ",".join(setcats)


#to calculate frequencies, we need the total number of words per category
#we iterate over our list of categories
#for each, we extract the entry for each word and add
##THIS THING SHOULD BE REPLACED BY OUR COOL COMPDICTI BELOW
## OR READ INTO DIFFERENT DICTS IN THE FIRST PLACE?

for cati in setcats:
    print cati
    wordcount=[catdicti[entry][cati] for entry in catdicti]
    print "number of results", len(wordcount)
    print "word count", sum(wordcount)
    wordcountdicti[cati]=sum(wordcount)



print wordcountdicti
print "\n-------\n"

    
#
#now we use the totals to transform the entries in the catdicti into frequencies
#lets get rid of zero entries first. they are annoying
for entry in catdicti:
    catdicti[entry]={k: float(v) for k, v in catdicti[entry].items() if v}

for entry in catdicti:
    for i in catdicti[entry]:
        #for each category, we divide by the number of total words in this category
        #i.e the frequenc. then multiply by 1 mio for good cheer. 
        #print entry, catdicti[entry][i], catdicti[entry][i]/wordcountdicti[i]
       catdicti[entry][i]=catdicti[entry][i]/wordcountdicti[i]*1000000
        #print entry, catdicti[entry][i]#, catdicti[entry][i]/wordcountdicti[i]

##
##ESTABLISHING DISTANCE
##
### let's exclude all words < 100 from the overall dictionary. they will not ba included in analysis
# total word count
allwords=sum(dicti.values())

#we exlude low freq words and check up on things by printing
print "allwords: ", allwords
print "length dicti", len(dicti)
dicti={k: (float(v)/allwords)*1000000 for k, v in dicti.items() if v > 99}
print "length dicti > 99", len(dicti)



        #print entry, catdicti[entry][i]#, catdicti[entry][i]/wordcountdicti[i]


    
#for each entry in the catdict, we want only the entry with the category we looking at
for cati in setcats:
    #note that we iterate over the overall dictionary to make sure we only get the 99+ words
    for entry in dicti:
        if cati in catdicti[entry]:
            #print entry, catdicti[entry]
            compdicti[cati][entry]=catdicti[entry][cati]

#what comparisons do we want to make?
comps=['w4w_w4m', 'w4w_m4m', 'w4m_m4m', 'w4w_m4w', 'w4m_m4w', 'm4m_m4w']

def dictwriter(name, dictionary):
    output=codecs.open(name+".txt","a", "utf-8")
    #stole this from SO: http://stackoverflow.com/questions/8519599/python-dictionary-to-string-custom-format
    output.write('\n'.join(['%s, %s' % (key, value) for (key, value) in dictionary.items()]))
    output.close()

for compi in comps:
    tempdicti=distancemachine(compi, compdicti[compi.split("_")[0]], compdicti[compi.split("_")[0]])
    dictwriter(compi, tempdicti)
    print compi, "done"
        
# if we rock, we use the name to extract relevant categories from dict
w4w_w4m=distancemachine("w4w_w4m",compdicti['w4w'], compdicti['w4m'])
w4w_m4m=distancemachine("w4w_m4",compdicti['w4w'], compdicti['m4m'])
w4m_m4m=distancemachine("w4m_m4m",compdicti['w4m'], compdicti['w4m'])
w4w_m4w=distancemachine("w4w_m4w",compdicti['w4w'], compdicti['m4w'])
w4m_m4w=distancemachine("w4m_m4w",compdicti['w4m'], compdicti['m4w'])
m4m_m4w=distancemachine("m4m_m4w",compdicti['m4m'], compdicti['m4w'])


print len(w4w_w4m)
print len(w4w_m4m)
print len(w4m_m4m)
print len(w4m_m4w)
print len(m4m_m4w)


    
print len(faillist)
print faillist[0]
##
##for entry in catdicti:
##    for i in catdicti[entry]:
##        try:
##            #print  catdicti[entry][i]
##        #print dicti[entry]
##        #try:
##            catdicti[entry][i]=(catdicti[entry][i]-dicti[entry])/(catdicti[entry][i]/100)
##            print  entry, i, catdicti[entry][i]
##            print dicti[entry], catdicti[entry]
##            print "----\n\n"
##        except KeyError , err:
##            #print "key", err
##            pass
##            faillist.append((entry, i))
##            #print err
##            #print "assi"
##    
##print "faillist", len(faillist)
##print faillist[0]
##print dicti[faillist[0]]

##
##
##
##
####for each word, we end up with a percentage difference
####for item in dicti:
####    print item, dicti[item]
####    break
##
##
##
####for item in catdicti:
####    for thing in catdicti[item]:
####        print catdicti[item][thing]
###print sum(dicti.values())
##
###print sum(catdicti.values())
##
###sorteddicti=sorted(dicti, key=dicti.get, reverse=True)
##sorteddicti=sorted(dicti.items(), key=lambda x: x[1], reverse=True)
###print type(sorteddicti)
###note that sorteddicti becomes a list! cause you cannot order a dict
####for entry in sorteddicti:
####    output.write(entry[0]+","+unicode(entry[1])+"\n")
##
###sum(t.values)
