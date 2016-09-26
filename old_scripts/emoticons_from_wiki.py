# -*- coding: utf-8 -*-

"""
reads the emoticons from Wikipedia page.
reads in html file, outputs emoticons to txt file based on user input (Yes/No).
manullay then create files for character based versus graphics based emoticons.
"""


import codecs
from bs4 import BeautifulSoup


with codecs.open("/Users/ps22344/Desktop/List of emoticons - Wikipedia, the free encyclopedia.htm", "r") as inputi:
	wikitext=inputi.read()
	
soup=BeautifulSoup(wikitext, "html.parser")

results=[]

for i in soup.find_all('td'):
	if not i.attrs:
		print i
		results.append(i.text)
	
#print results
outski=codecs.open("outski.txt", "a", "utf-8") 
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


emolist=codecs.open("emolist.txt", "a", "utf-8") 
for emo,judg in output:
	if judg == "Y":
		emolist.write(emo+"\n")

emolist.close()

	



