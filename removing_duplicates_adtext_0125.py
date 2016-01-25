
import os
import re
from collections import defaultdict
import shutil
print "start"


#look for identical titles, then compare texts

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


#so if there is more than one entry, i.e. two have the same title, we check whether the text 
# has the same length. Let's do little dictionary for each one!
#Then inspect

	#we go thru each entry
for entry in titledict:
	#if there is only one entry to this title, we copy the file. no questions asked  
	if len(titledict[entry]) == 1:
 		keeper=titledict[entry][0][0]
 		#i was thinking about making a function for this, but does not seem
		#all that convenient
		#we locate the original file
		original=os.path.join(directory, keeper)
		#we locate its new place
		copy=os.path.join(outputdir, keeper)
		#off it goes
		shutil.copyfile(original, copy)
	#otherwise, we check: if two files match in title name AND text length, one has to go!
	if len(titledict[entry]) != 1:
		#for this entry, we collect files of the same length in a minidict
 		minidict=defaultdict(list)
 		#we go thru the elements of each entry
 		for thing in titledict[entry]:
  			minidict[thing[1]].append(thing[0])
  		#then we iterate thru the minidict: for each entry, the first file only is copied. 
 			for m in minidict:
 				keeper=minidict[m][0]
 				#same code as above
 				original=os.path.join(directory, keeper)
 				copy=os.path.join(outputdir, keeper)
 				shutil.copyfile(original, copy)
 				print "copying", copy, #minidict[m]



	
print "length of titledict", len(titledict)
print "finish"


