import os
import re
from collections import defaultdict
import shutil
print "start"

#setting up some functions
def tagextractor(text, tag, fili):
	regexstring="<"+tag+"=(.*?)>"
	result=re.findall(regexstring, text)
	if len(result) != 1:
		print "alarm in tagextractor", fili, result
	return result[0]
#read in the files

#set up top dir
directory="/Users/ps22344/Downloads/craig_0118"

#read in subdir, make file list
#subdirs=['adfiles3_output_0116']
subdirs=[s for s in os.listdir(directory) if not s.startswith(".")]
#print subdirs

#set up dictionary
cliddict=defaultdict(list)

# #read in file

## we play some games to get the hidden files out of the way
for sub in subdirs:
	print sub
	#filis=os.listdir(directory+"/"+item)
 	filis=[f for f in os.listdir(directory+"/"+sub) if not f.startswith(".")]
## we iterate over the list of files
 	for fili in filis:
 	#yes we should read the file in first
 	#this is just to show we can do it that way too
 		clid=tagextractor(open(os.path.join(directory, sub, fili)).read(), "clid", fili)
 		#t=open(os.path.join(directory, sub, fili)).read()
 		cliddict[clid].append(sub+"/"+fili)
 	# print "length dicti", len(cliddict)
#   	f=open("cliddict_log_0121_fullpath"+sub+".txt", "a")
#  	for item in cliddict:
#  		f.write(item+","+" ".join(cliddict[item])+"\n")
#  	f.close()

print "length of cliddict", len(cliddict)
# for item in cliddict:
# 	print item, cliddict[item]
# 	break
count=[]


#let's move some files

for item in cliddict:
 	keeper=cliddict[item][0]
 	original=os.path.join(directory, keeper)
 	copy=os.path.join("/Users/ps22344/Downloads/craig_0121", keeper)
 	shutil.copyfile(original, copy)
	
# if len(cliddict[item]) > 2:
# 		count.append((len(cliddict[item]), cliddict[item]))
# 
print count
#get the clid


#put the clid in dictionary, for each clid collect the text name


#print out super long clids







print "finish\n----------\n\n\n"
