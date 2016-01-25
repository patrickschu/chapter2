import os
import re
from collections import defaultdict
import shutil
print "start"

###this finds spanish-only posts and removes them


## load a spell checker such as pyenchant; or: celex; or: open office. 
## compare the spell checker with text from ad; report if very low overlap

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
directory="/Users/ps22344/Downloads/craig_0121"
outputdir="/Users/ps22344/Downloads/craig_0125"

#read in subdir, make file list
subdirs=[s for s in os.listdir(directory) if not s.startswith(".")]
#subdirs=["adfiles2_output_0116"]
#print subdirs

#set up dictionary
titledict=defaultdict(list)

for sub in subdirs:
	print sub
	#filis=os.listdir(directory+"/"+item)
 	filis=[f for f in os.listdir(directory+"/"+sub) if not f.startswith(".")]
## we iterate over the list of files
 	for fili in filis:
 	#yes we should read the file in first
 	#this is just to show we can do it that way too with the joini thing
 		title=tagextractor(open(os.path.join(directory, sub, fili)).read(), "title", fili)
 		text=adtextextractor(open(os.path.join(directory, sub, fili)).read(), fili)
 		#t=open(os.path.join(directory, sub, fili)).read()
 		titledict[title].append((sub+"/"+fili, len(text)))
 	# print "length dicti", len(cliddict)
#   	f=open("cliddict_log_0121_fullpath"+sub+".txt", "a")
#  	for item in cliddict:
#  		f.write(item+","+" ".join(cliddict[item])+"\n")
#  	f.close()
