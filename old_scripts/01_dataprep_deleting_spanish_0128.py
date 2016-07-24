## go thru, delete all texts with English - to non-English ratio lower than X
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
#reading English dictionary from CELEX
#the formatting of eow.cd is: 8\abacus\8\1\B\8\0\ab-a-cus
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
	
#read in the files

#set up top dir
directory="/Users/ps22344/Downloads/craig_0201"
outputdir="/Users/ps22344/Downloads/craig_0126"

#read in subdir, make file list
subdirs=[s for s in os.listdir(directory) if not s.startswith(".")]
#subdirs=["files9_output_0102"]
#print subdirs

#set up list of short texts where our magic won't work
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
 		#how long a text do we need?  10 should be good
 		if length < 10:
 			#print "alarm, this text is so very short", len(text), fili
 			shortlist.append(os.path.join(directory, sub, fili))
 		else: 
 			snippet1=text[int(length/10): int(length/10) + 10]
			#check out our text cleaning tool. we can use this later
			#first we delete tags, tags need be deleted earlier or they screw up splitting
			#snippet2=[re.sub("<.*/?>", "", s) for s in snippet]
			#snippet2=[s.translate(None, string.punctuation).lower() for s in snippet]
			snippet=[s.strip(string.punctuation).lower() for s in snippet1]
			#print snippet3, fili
			ratio= len([s for s in snippet if s in lexicon])
			if ratio  < 4 :
				try:
					os.remove(os.path.join(directory, sub, fili))
					print "deleted: ", os.path.join(directory, sub, fili)
				except OSError, err:
					print os.path.join(directory, sub, fili), "is protected", err
 			
print "length of shortlist", len(shortlist) 	

print "shortlist"
for shortie in shortlist:
	print shortie

print "finish"
print ('\a')
os.system('say "your program has finished"')
