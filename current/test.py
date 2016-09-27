import numpy as np
from string import punctuation
import re
import clustertools as ct
import time
import os
import codecs
from collections import defaultdict
import json 
#how to use numpy unicode in join


x=np.array([U'word', U'assi', 12])
#print type(x[0])
#print "++++".join(x)



one=[['a','b'], [2,1000]]
print "XXXX".join([":".join([unicode(i) for i in x]) for x in one])


#typography={
#emoticons={':)':0, ':(':0 ,...},
#counstruct out of string.puncutation

#punctuation={re.compile("\.\.+":0, ",,+":0




#FINISHED PRODUCT
numbersdict={
re.compile(r"\d+"):0
}
for f in numbersdict:
	print f.pattern
	
numbersdict={
re.compile(r"4+$"):0
}
for f in numbersdict:
	print f.pattern

	
testi=" I am 459 va lonely soul .. deep ?? but 4 you <<<<<<<!! !? what the heck ?!! so.... **haha here i lie:4 5'11'' is some # ## punctuation @@ . "
#words=ct.tokenizer(testi)
#print words
# 
# 
# for i in numbersdict:
# 	result=i.findall(testi)
# 	if result:
# 		print i.pattern
# 		print result
# 	numbersdict[i]=len(result)
# 
# print numbersdict


topic="4"
#dataset
dir='/Users/ps22344/Downloads/craig_0208/'#adfiles_output_0116'

outifile=codecs.open(topic+"words.txt", "a", "utf-8")
onedict=defaultdict(int)
twodict=defaultdict(int)


#check if we find items
starttime=time.time()

for pati in [i for i in os.listdir(dir) if not i.startswith(".")]:
	"""
	this looks over the keys of a dictionary that are regex patterns. 
	it outputs findings in the corpus given in "dir" with context.
	dir needs to have subfolders. 
	ADD: collocation counter
	"""
	print pati
	for fili in [i for i in os.listdir(os.path.join(dir, pati)) if not i.startswith(".")]:
		fili=codecs.open(os.path.join(dir, pati, fili), "r", "utf-8")
		inputad=ct.adtextextractor(fili.read(), fili)
		words=ct.tokenizer(inputad)
		words=[w.lower() for w in words]
		#specific words processing for numbers: introduce space between number immediately followed by word-character
		if [w for w in words if any(k.match(w) for k in numbersdict.keys())]:
			#try:
			if words.index(w) not in [0, 1, len(words) -1, len(words)-2]:
				less2=words[words.index(w)-2]
				plus2=words[words.index(w)+2]
				twodict[less2]=twodict[less2]+1
				twodict[plus2]=twodict[plus2]+1
			if words.index(w) not in [0, len(words)-1]:
				less1=words[words.index(w)-1]
				plus1=words[words.index(w)+1]
				onedict[less1]=onedict[less1]+1
				onedict[plus1]=onedict[plus1]+1
				#print [(words[words.index(w)-2], words[words.index(w)-1],w, words[words.index(w)+1], words[words.index(w)+2]) for w in words if any(k.match(w) for k in numbersdict.keys()) and words.index(w) not in [0, 1, len(words)-1, len(words)-2]]
				outifile.write("\n".join([" ".join([words[words.index(w)-2], words[words.index(w)-1],w, words[words.index(w)+1], words[words.index(w)+2]]) for w in words if any(k.match(w) for k in numbersdict.keys()) and words.index(w) not in [0, 1, len(words)-1, len(words)-2]]))
			else:
				pass
				#print words
			
			
			
			#except IndexError:
			#	print words
			
		# for entry in numbersdict:
# 			t=entry.findall(inputad)
# 			print "regex findall\n", t, "\n\n"
		#print [(words[words.index(w)-2], words[words.index(w)-1], w, words[words.index(w)+1], words[words.index(w)+2])  for w in words if any(k.match(w) for k in numbersdict.keys())]

print numbersdict
print "\n\ndistance of 2"
print "\n".join([": ".join([k, unicode(twodict[k])]) for k in sorted(twodict, key=twodict.get, reverse=True)])

print "\n\ndistance of 1"
print "\n\ndistance of 1"
print "\n".join([": ".join([k, unicode(onedict[k])]) for k in sorted(onedict, key=onedict.get, reverse=True)])

outifile.close()
with codecs.open(topic+"_onedict.json", "w", "utf-8") as oneout:
	json.dump(onedict, oneout)

with codecs.open(topic+"_twodict.json", "w", "utf-8") as twoout:
	json.dump(twodict, twoout)

endtime=time.time()

print "This took us {} minutes".format((endtime-starttime)/60)
