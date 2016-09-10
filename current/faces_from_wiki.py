# -*- coding: utf-8 -*-

"""
reads the faces from Wikipedia page https://en.wikipedia.org/wiki/Miscellaneous_Symbols_and_Pictographs.
reads in html file, outputs pictographs to txt file based on user input (Yes/No).
THESE ARE ADDED TO PICTILIST
"""


import codecs
from bs4 import BeautifulSoup


with codecs.open("/Users/ps22344/Desktop/Miscellaneous Symbols and Pictographs - Wikipedia, the free encyclopedia.htm", "r") as inputi:
	wikitext=inputi.read()
	
soup=BeautifulSoup(wikitext, "html.parser")

results=[]

for i in soup.find_all('td'):
	if not i.attrs:
		print i.text
		results.append(i.text)
		
outski_face=codecs.open("outski_face.txt", "a", "utf-8") 
output=[]
for r in results:
	spliti=r.split()
	for s in spliti:
		print "\n\n", s, len(s)
		judgment=raw_input("Y es or N o     ")
		output.append([s, judgment])
		outski_face.write("\t".join([s, judgment])+"\n")

outski_face.close()
print output


emolist=codecs.open("facelist.txt", "a", "utf-8") 
for emo,judg in output:
	if judg == "Y":
		emolist.write(emo+"\n")

emolist.close()

	



