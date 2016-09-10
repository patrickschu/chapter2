# -*- coding: utf-8 -*-

"""
reads the pictographs from Wikipedia page https://en.wikipedia.org/wiki/Miscellaneous_Symbols_and_Pictographs.
reads in html file, outputs pictographs to txt file based on user input (Yes/No).
"""


import codecs
from bs4 import BeautifulSoup


with codecs.open("/Users/ps22344/Desktop/Miscellaneous Symbols and Pictographs - Wikipedia, the free encyclopedia.htm", "r") as inputi:
	wikitext=inputi.read()
	
soup=BeautifulSoup(wikitext, "html.parser")

results=[]

for i in soup.find_all('a'):
	#if i.attrs:
	if i.attrs.get('title', None):
		print i.attrs['title']
		results.append(i.text)
	
outski=codecs.open("outski_picti.txt", "a", "utf-8") 
output=[]
for r in results:
	spliti=r.split()
	for s in spliti:
		print "\n\n", s, len(s)
		judgment=raw_input("Y es or N o     ")
		output.append([s, judgment])
		outski.write("\t".join([s, judgment])+"\n")

outski.close()
print output


pictilist=codecs.open("pictilist.txt", "a", "utf-8") 
for emo,judg in output:
	if judg == "Y":
		pictilist.write(emo+"\n")

pictilist.close()

	



