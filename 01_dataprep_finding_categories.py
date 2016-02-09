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
print "we're looking for categories we dont' like"

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
	
#here we set up some lists etc that we'll need
acceptable=["w4m","m4w", "w4w", "m4m","wm4m", "m4wm", "m4mm", "mm4m","m4t", "t4m", "mw4m", "m4mw", "mw4w", "m4ww", "ww4m", 
"ww4w", "w4ww", "t4w", "w4t", "mm4w", "w4mm", "w4t", "t4w"]
problemlist=[]
#read in the files

#set up top dir
directory="/Users/ps22344/Downloads/craig_0208"

#read in subdir, make file list
subdirs=[s for s in os.listdir(directory) if not s.startswith(".")]
#subdirs=["files9_output_0102"]
#print subdirs
count=0

for sub in subdirs:
	print sub
# 	#filis=os.listdir(directory+"/"+item)
  	filis=[f for f in os.listdir(directory+"/"+sub) if not f.startswith(".")]
# ## we iterate over the list of files
  	for fili in filis:
  		#print fili
		inputfile=os.path.join(directory, sub, fili)
		inputi=codecs.open(inputfile, "r", "utf-8")
		inputtext=inputi.read()
		#we extract gender
		cati=tagextractor(inputtext, "category1", inputfile)
		if not re.search("(m{1,2}|w{1,2}|t{1,2}|wm|mw)4(m{1,2}|w{1,2}|t{1,2}|wm|mw)", cati):
			#we need to supply title, cat and text, too
			category=tagextractor(inputtext, "category1", inputfile)
			texti=adtextextractor(inputtext, inputfile)
			title=tagextractor(inputtext, "title", inputfile)
			addressee=tagextractor(inputtext, "addressee1", inputfile)
			print "\n\n------------------\n"			
			print cati, inputfile
			print title
			print addressee
			#print texti
			count=count+1
			eval=raw_input("category?  ")
			print eval[0]
			rightcattags=re.sub('<category1=(.*?)>', '<category1='+str(eval)+'>', inputtext)
			##rightcatadrestags=re.sub('<addressee1=(.*?)>', '<addressee1='+str(eval)+'>', rightcattags)
			rightgendercategoryaddresseetags=re.sub('<addressee1=(.*?)>', '<addressee1='+str(eval[2])+'>', rightcattags)
			print rightgendercategoryaddresseetags
			print "adres", eval[2]
			print "gender", eval[0]
			inputi.close()
		# #here is what this looks like in the file:
# 		#<gender=w> <category1=w4m>
			outputi=codecs.open(inputfile, "w", "utf-8")
			outputi.write(rightgendercategoryaddresseetags)
			outputi.close()
			print "file processed: ", inputfile
		# adtype=tagextractor(input, "plat", inputfile)
		
# 		#getting text length
#   		text1=adtextextractor(input, inputfile)
#   		#remove html tags
#   		text2=re.sub("<.*/?>", " ", text1)
#   		#split text on whitespace, comma, stop
#   		#maybe only btw characters?
#   		#this we steal from nltk word_tokenize
#   		#(?:[?!)\";}\]\*:@\'\({\[])
#   		text=re.split("(?:\s|\W)+", text2.lower())
#   		length=len(text)
#   		output.write(inputfile+","+category+","+gender+","+adtype+","+str(length)+"\n")
print "count", count

print "finish"
print ('\a')
os.system('say "your program has finished"')
		
