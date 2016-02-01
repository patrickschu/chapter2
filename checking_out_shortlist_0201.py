import os
import re
import codecs
from collections import defaultdict
import shutil
import string
import numpy

print string.punctuation

print "start"

###this finds spanish-only posts and removes them


## load a spell checker such as pyenchant; or: celex; or: open office. 
## compare the spell checker with text from ad; report if very low overlap
#reading CELEX
#the formatting of eol.cd is: 8\abacus\8\1\B\8\0\ab-a-cus
#
#opening the celexfile
celexinput=open("/Users/ps22344/Downloads/eow.cd", "r")

#i guess we just throw it all into a list called lexicon
lexicon=[]
for line in celexinput:
	lexicon.append(line.split("\\")[1].lower())

# we add some common English words not in Celex

lexicon=lexicon+["i'm", "etc"]
print "length of lexicon", len(lexicon)


## go into each ad, extract random string of words, compare to spell checker

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
	
#this one compares input to celex or other list of allowed words
#it returns a 1 if yes, a zero if not
#its a completely unncessary function but here we go
#at some point. let us time this and compare to listcomp below
def lexiconcheck(word, lexicon):
	if word in lexicon:
		return 1
	else:
		return 0
	
#read in the files

# #set up top dir
directory="/Users/ps22344/Downloads/craig_0201"
# outputdir="/Users/ps22344/Downloads/craig_0126"

f=open("shortlist.txt", "r")

for line in f:
	filename=os.path.join(directory, line)
	inputfile=open(filename.rstrip("\n"), "r").read()
	adtext=adtextextractor(inputfile, filename)
	print adtext, line, "\n"

print "finish"
print ('\a')
os.system('say "your program has finished"')
