## go thru, delete all texts with ratio lower than X

## all the good ones should be protected
try: 
	
	except Some Error, err:
		print fili, "is protected", err
		
		
		
		


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

#set up top dir
directory="/Users/ps22344/Downloads/craig_0125"
outputdir="/Users/ps22344/Downloads/craig_0126"

#read in subdir, make file list
subdirs=[s for s in os.listdir(directory) if not s.startswith(".")]
#subdirs=["files9_output_0102"]
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
 		text1=adtextextractor(codecs.open(os.path.join(directory, sub, fili), "r", "utf-8").read(), fili)
 		text2=re.sub("<.*/?>", " ", text1)
 		#the final product needs to be called text so the script below does not screw up		
 		text=text2.split()
 		length=len(text)
 		
 		#how long a text do we need? ah 10 should be good
 		if length < 10:
 			#print "alarm, this text is so very short", len(text), fili
 			shortlist.append(os.path.join(directory, sub, fili))
 			#print shortlist
 		else: 
 			snippet1=text[int(length/10): int(length/10) + 10]
			#print snippet.translate(None, string.punctuation)
			#check out our text cleaning tool. we can use this later
			#first we delete tags, tags need be deleted earlier or they screw up splitting
			#snippet2=[re.sub("<.*/?>", "", s) for s in snippet]
			#snippet2=[s.translate(None, string.punctuation).lower() for s in snippet]
			snippet=[s.strip(string.punctuation).lower() for s in snippet1]
			#print snippet3, fili
			ratio= len([s for s in snippet if s in lexicon])
			means.append(ratio)
			if ratio  == 4 :
				try:
					
				except Some Error, err:
					print fili, "is protected", err
				
				
				
 				print snippet, ratio, os.path.join(directory, sub, fili)
meanratio=numpy.array(means).mean()	
stdratio=numpy.array(means).std()
medianratio=numpy.array(means).median()	
print "mean ratio", meanratio
print "std ratio", stdratio
print "median ratio", medianratio
 			
print "length of shortlist", len(shortlist) 		
 	# print "length dicti", len(cliddict)
#   	f=open("cliddict_log_0121_fullpath"+sub+".txt", "a")
#  	for item in cliddict:
#  		f.write(item+","+" ".join(cliddict[item])+"\n")
#  	f.close()


print "finish"
print ('\a')
os.system('say "your program has finished"')
