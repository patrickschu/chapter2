import time
import codecs
import json
import re
import os
import clustertools as ct
from collections import defaultdict
from nltk import pos_tag

starttime=time.time()

def word2vecwordfinder(search_terms, input_file):
	"""
	wordfinder looks up individual words in the clusters from word2vec.
	search_terms is list of strings, input_file the path to a JSON file of clusters.
	"""
	with codecs.open(input_file, 'r', 'utf-8') as inputfile:
		clusters=json.load(inputfile)
	
	results=[k for term in search_terms for k in clusters.keys() if term in clusters[k]['words']]
	return results
	


#number dictionary
numberdict={}

numbers=[2]#range(11,20)
for number in numbers:
	numberdict[number]=0


#written numbers for quality control
writtennumberdict={}

writtennumbers=["zero", "one","two","three","four","five","six","seven","eight","nine","ten","eleven","twelve","thirteen","fourteen", "twenty", "thirty", "fourty", "fifty", "sixty", "fivefivefive"]	

for writtennumber in writtennumbers:
	writtennumberdict[writtennumber]=0

print writtennumberdict
#dirs
dir='/Users/ps22344/Downloads/craig_0208/'
#dir='/Users/ps22344/Downloads/craigbalanced_0601'


#do we need the to, do ect in post_context
#exclude_post_context=["years?", "months?", "weeks?", "days?", "hours?", "times?", "peoples?", "daughters?", "(boy|girl)?friends?", "girls?", "kids?", "boys?", "children", "dogs?", "jobs?", "things?", "(p|a)\.?m\.?", "to", "or" ]
exclude_post_context=["years?", "months?", "weeks?", "days?", "hours?", "times?", "peoples?", "(boy|girl)?friends?", "(p|a)\.?m\.?", "to", "or" ]

exclude_post_context=[re.compile(r"^"+i+"$") for i in exclude_post_context]

exclude_pre_context=["ops", "till?"]
exclude_pre_context=[re.compile(r"^"+i+"$") for i in exclude_pre_context]

def rebusfinder(input_path, word_dictionary, number_dictionary, excluded_words):
	"""
 	This finds words that are represented as numbers. 
 	All combinations \W([a-z]+)\s+("+unicode(number)+")\s+([a-z]+)\W for the number put in are identified.
 	The lists exclude_pre and exclude_post word for negative contexts in 4.
 	It print the results and give type and token counts. 
	
	"""
	#with codecs.open(word_dictionary, "r", "utf-8") as worddictionary:
	#	worddictionary=json.load(worddictionary)
	#worddictionary={k:v for k,v in worddictionary.items() if not k in excluded_words and worddictionary[k] > 1}
	for number in number_dictionary.keys():
		numberregex=re.compile("\W([a-z]+)\s+("+unicode(number)+")\s+([a-z]+)\W")
		#just for now
		h0dict=defaultdict(int)
		h2dict=defaultdict(int)
		print numberregex.pattern
		for pati in [i for i in os.listdir(input_path) if not i.startswith(".")]:
			for fil in [i for i in os.listdir(os.path.join(input_path, pati)) if not i.startswith(".")]:
				fili=codecs.open(os.path.join(input_path, pati, fil), "r", "utf-8")
				inputad=ct.adtextextractor(fili.read(), fil)
				inputad=inputad.lower()
				hits=numberregex.findall(inputad)
				#this weeds out all the phonenumbers. 
				hits=[h for h in hits if h[0] not in writtennumberdict and h[2] not in writtennumberdict]
				for h in hits:
					#print  h
					if not any (regex.match(h[2]) for regex in exclude_post_context) and not any (regex.match(h[0]) for regex in exclude_pre_context):
						tagged=pos_tag(h)
						#pretext
						if (tagged[0][1] in ["DT", "JJS", "TO", "PRP$"]) or

							"these are all trash"
						

						
						(tagged[0][1] in ["VB", "VBD", "VBP", "VBZ"] and tagged[2][1] in ["JJ"]):
							print "hooked the if"
							"more is so ambigous, same is younger, older --> comparatives out"
							"Verb + JJ is trash"
	# 						
# 						if tagged[2][1] in ["DT", "CD", "EX"]:
# # 							"these are all good"
# 						if tagged[2][1] in ["NNS"] and h[2] not in ["chat", "kiss", "go", "know", "find", "do", "c", "knees"]:
# 							"these are trash"
# 							x=0
# 						if tagged[2][1] in ["VB"]:
# 							"we keep all these"
# 							pass
# 						if tagged[2][1]=="IN" and tagged[2][0] not in ["through", "ago", "from", "without", "since", "about", "before", "if", "that", "after", "during", "as", "for", "at", "on", "with", "of", "in", "off"]:
# 							"these are all trash"
# 							pass
# 						if tagged[2][1]=="CC" and h[2] not in ["but"]:
# 							"this is trash"
# 		
# 						if tagged[0][1] in ["VBG"] and h[0] not in ["talking", "responding", "waiting", "getting","looking", "going", "trying"]:
# 							"we disregard the matches"
# 						
# 						if tagged[0][1]=="IN" and h[0] not in ["out", "like"]:# and tagged[0][0] not in ["de", "that", "beyond", "until", "upon", "up", "within", "between", "past", "at", "as", "by", "if", "than", "after", "in", "of", "for", "with", "about", "over", "from"]:
# 							"this is trash"
						else:
							print "elseloop", tagged
							h0dict[h[0]]=h0dict[h[0]]+1
							h2dict[h[2]]=h2dict[h[2]]+1
						
						
					# 	if tagged[0][1]=="JJR":
# 							"50:50, few tokens"
				
						#remember to re-visit per notes
						
# 						if tagged[0][1]=="JJ":
# 							"these are almost all mistagged"
# 						if tagged[0][1]=="MD":
# 							"few tokens and most suck: mis-tagged month, random numbers"
# 						if tagged[0][1]=="PDT":
# 							"these dont exist"	
# 						if tagged[0][1]=="POS":
# 							"NA"	
# 						if tagged[0][1]=="PRP":
# 							"mostly trash but 2 prosper"	
# 						if tagged[0][1]=="PRP$":
# 							"all trash"						
# 						if tagged[0][1]=="RB":
# 							"this is a random collection of stuff"						
# 						if tagged[0][1] in ["RBR", "RBS"]:
# 							"3 tokens fro RBR 2 + 1 -"
# 						if tagged[0][1] in ["RP"]:
# 							"NA"
# 
# 						if tagged[0][1] in ["SYM", "UH", "WP$"]:
# 							"THESE DONT EXIST"
# 						if tagged[0][1] in ["VBG"]:
# 							"LOTS OF VERBS, NOT GETTING INTP THAT RIGHT NOW"
# 						if tagged[0][1] in ["WDT", "WP"]:
# 							"2 results make sense"
# 						if tagged[0][1] in ["WRB"]:
# 							"where is out, when is in, how is in"
# 
# 						if tagged[0][1] in ["FW", "EX"]:
# 							"NA"
									
						#posttext
						if tagged[2][1]=="CC" and tagged[2][0] not in ["and", "but", "less", "plus"]:
							"this is good except for but which needs to be re-visited"

						
						#else:
						#	print h
						#	if h[0]:
					#	print h
						#		h0dict[h[0]]=h0dict[h[0]]+1
						#		h2dict[h[2]]=h2dict[h[2]]+1
						#else:
						#	if h[2]:#:=="days":
						#		#print tagged
						#		h0dict[h[0]]=h0dict[h[0]]+1
						#		h2dict[h[2]]=h2dict[h[2]]+1
		print "We have {} items with a token count of {}".format(len(h0dict.keys()), sum(h0dict.values()))
		h0dict={k:v for k,v in h0dict.items() if v > 0}
		print "\n\n", number, "\npretext here be the results\n\n"
		print "\n".join([": ".join([k, unicode(h0dict[k]), ".".join(word2vecwordfinder([k], '/Users/ps22344/Downloads/chapter2/current/clusters_74_19_45_07_31.json'))]) for k in sorted(h0dict, key=h0dict.get, reverse=True)])
		print "\n\n", number, "\nposttext here be the results\n\n"
		print "\n".join([": ".join([k, unicode(h2dict[k]), ".".join(word2vecwordfinder([k], '/Users/ps22344/Downloads/chapter2/current/clusters_74_19_45_07_31.json'))]) for k in sorted(h2dict, key=h2dict.get, reverse=True)])

		print "We have {} post items with a token count of {}".format(len(h2dict.keys()), sum(h2dict.values()))
		print "We have {} pre items with a token count of {}".format(len(h0dict.keys()), sum(h0dict.values()))


			
rebusfinder(dir, "worddict_full.json", numberdict, "b")



			

			
			
			
	
endtime=time.time()
print "This took us {} minutes".format((endtime-starttime)/60)	