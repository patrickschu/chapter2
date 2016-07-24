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


print "start"


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
directory="/Users/ps22344/Downloads/craig_0202"
outputdir="/Users/ps22344/Downloads/craig_0126"
outputfile="corpusstats_0201.txt"

output=codecs.open(outputfile, "a")
#read in subdir, make file list
subdirs=[s for s in os.listdir(directory) if not s.startswith(".")]
#subdirs=["files9_output_0102"]
#print subdirs


for sub in subdirs:
	print sub
# 	#filis=os.listdir(directory+"/"+item)
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
  		length=len(text)
  		output.write(inputfile+","+category+","+gender+","+adtype+","+str(length)+"\n")

output.close()
print "finish"
print ('\a')
os.system('say "your program has finished"')
		
