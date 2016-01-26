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
	lexicon.append(line.split("\\")[1])
lexicon.append("i'm")
	
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
def lexiconcheck(word, lexicon):
	if word in lexicon:
		return 1
	else:
		return 0
	
	
	
	

#read in the files

#set up top dir
directory="/Users/ps22344/Downloads/craig_0125"
outputdir="/Users/ps22344/Downloads/craig_0126"

#read in subdir, make file list
subdirs=[s for s in os.listdir(directory) if not s.startswith(".")]
#subdirs=["adfiles2_output_0116"]
#print subdirs

#set up list of short texts where out magic won't work
shortlist=[]
means=[]

for sub in subdirs:
	print sub
	#filis=os.listdir(directory+"/"+item)
 	filis=[f for f in os.listdir(directory+"/"+sub) if not f.startswith(".")]
## we iterate over the list of files
 	for fili in filis:
 		#yes we should read the file in first
 		#this is just to show we can do it that way too with the joini thing
 		text=adtextextractor(codecs.open(os.path.join(directory, sub, fili), "r", "utf-8").read(), fili).split()
 		length=len(text)
 		
 		#how long a text do we need? ah 10 should be good
 		if len(text) < 10:
 			#print "alarm, this text is so very short", len(text), fili
 			shortlist.append(os.path.join(directory, sub, fili))
 			#print shortlist
 		else: 
 			snippet=text[int(length/10): int(length/10) + 10]
			#print snippet.translate(None, string.punctuation)
			#check out our text cleaning tool. we can use this later
			#first we delete tags
			snippet2=[re.sub("<.*/?>", "", s) for s in snippet]
			#snippet2=[s.translate(None, string.punctuation).lower() for s in snippet]
			snippet3=[s.strip(string.punctuation).lower() for s in snippet2]
			#print snippet3, fili
			ratio= sum([lexiconcheck(s, lexicon) for s in snippet3])
			means.append(ratio)
			# if ratio < 2:
# 				print snippet3, ratio
meanratio=numpy.array(means).mean()	
print "mean ratio", meanratio
 			
print "length of shortlist", len(shortlist) 		
 	# print "length dicti", len(cliddict)
#   	f=open("cliddict_log_0121_fullpath"+sub+".txt", "a")
#  	for item in cliddict:
#  		f.write(item+","+" ".join(cliddict[item])+"\n")
#  	f.close()


print "finish"
