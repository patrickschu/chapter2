import codecs
import os
import re
import shutil
# read in file
# add name to list
# copy to new place till 10000
# 10 x 4= 40 000
# 
# done


#funcs
def tagextractor(text, tag, fili):
    regexstring="<"+tag+"=(.*?)>"
    result=re.findall(regexstring, text, re.DOTALL)
    if len(result) != 1:
        print "alarm in tagextractor", fili, result
    return result[0]

def writer(list_of_files, target_directory, threshold):
	for f in list_of_files[:threshold]:
		shutil.copy(f, os.path.expanduser(target_directory))
	print  len(list_of_files[:threshold]), " files copied"

w4wlist=[]
w4mlist=[]
m4wlist=[]
m4mlist=[]



pathi=os.path.expanduser(os.path.join("~/Downloads","craig_0208"))

folderlist=[i for i in os.listdir(pathi) if not i.startswith(".")]
print folderlist
for f in folderlist:
	filis=[i for i in os.listdir(os.path.join(pathi, f)) if not i.startswith(".")]
	for fili in filis:
		with open(os.path.join(pathi, f, fili)) as input:
			cat=tagextractor(input.read(), 'category1', fili)
			if cat=='w4w':
				w4wlist.append(os.path.join(pathi, f, fili))
			if cat=='m4w':
				m4wlist.append(os.path.join(pathi, f, fili))
			if cat=='w4m':
				w4mlist.append(os.path.join(pathi, f, fili))
			if cat=='m4m':
				m4mlist.append(os.path.join(pathi, f, fili))
result=[w4wlist,w4mlist,m4wlist,m4mlist]
print [len(y) for y in result]
count=0
for li in result:
	count=count+1
	writer(li, '~/Desktop/balanced_2/'+str(count), 10000)
		
	
		
