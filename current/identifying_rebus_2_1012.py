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

writtennumbers=["zero", "one","two","three","four","five","six","seven","eight","nine","ten","eleven","twelve","thirteen","fourteen", "twenty", "thirty", "fourty", "fifty", "sixty"]	

for writtennumber in writtennumbers:
	writtennumberdict[writtennumber]=0

print writtennumberdict
#dirs
dir='/Users/ps22344/Downloads/craig_0208/'
#dir='/Users/ps22344/Downloads/craigbalanced_0601'

exclude_post_context=[]#=["fingers","nights", "weeling","wheel",  "s", "am", "a.m.", "figures", "pm", "p.m.","dogs","tattoos", "emails", "foot", "feet", "ft", "children", "guy", "just", "of", "to", "i", "year", "years", "yr", "yrs", "days", "wheeler", "wheelers", "wheeling", "times", "or", "and", "months", "in", "kids", "weeks", "day", "days"]
exclude_pre_context=[]#= ["battlefield", "minimum", "but", "from", "got", "be", "this", "n", "first","only", "these", "has", "all", "are", "and", "feb", "april", "july", "number", "about", "playstation", "our", "on", "sleep","thanks","bedroom", "fine","before","had","except", "acres", "no", "in", "b", "with", "size", "a", "to","have", "of", "or", "the", "for", "feet", "foot", "ft", "my", "your"]+["young","incredable","friendly","very","eiight","every","servicing","like","quick","sev","our","giving","stage","last","son","speak","use","top","least","until","survived","than","those","is","buffy","im","at","after","know"]+[u'holding', u'ad', u'oh', u'gta', u'dogs', u'her', u'look', u'eyes', u'mind', u'make', u'figured', u'nearly', u'lodging', u'marred', u'start', u'taken', u'plus', u'truck', u'own', u'prefers', u'favorite', u'doorsopened', u'weather', u'other', u'gym', u'tandem', u'tongue', u'past', u'who', u'female', u'round', u'as', u'put', u'decent', u'raised', u'fairs', u'driving', u'that', u'beach', u'beach', u'just', u'country', u'carry', u'she', u'shine', u'seen', u'sober', u'dogs', u'same', u'friend', u'hmu', u'time', u'nice', u'guy', u'guy', u's', u'almost', u'o', u'unforgettable', u'zro', u'zro', u'hace', u'hoping', u'other', u'horny', u'regularly', u'nice', u'harts', u'now', u'beg', u'same', u'offing', u'answer', u'host', u'married', u'head', u'befor', u'thick', u'gym', u'f', u'drive', u'hair', u'owned', u're', u'park', u'smash', u'into', u'phase', u'havin', u'wednesday', u'large', u'finding', u'over', u'within', u'run', u'owned', u'answer', u'she', u'sitter', u'apr', u'apr', u'random', u'us', u'taking', u'hotel', u'fishing', u'were', u'interested', u'evil', u'events', u'supported', u'lvl', u'literally', u'may', u's', u'extinct', u'sending', u'hp', u'hp', u'suffered', u'waiting', u'pay', u'extinct', u'til', u'done', u'play', u'beautiful', u'then', u'plus', u'approx', u'lives', u'literally', u'get', u'found', u'someone', u'insert']

include_pre_context=[]#["pay", "m", "w", "up", "swf","love", "here", "not", "there", "ready","lkng","me", "ask", "live", "cheer", "grateful", "thanks", "partner", "men", "man", "male", "woman", "women","looking", "lookin", "pic", "pix", "lookn", "pics", "picture", "photo"]
include_post_context=[]#["swf","yu","who", "dead", "reading", "over", "help", "life", "your", "the", "a", "my", "our", "an", "real", "you", "u", "me", "ltr", "play", "same", "whatever", "sex", "someone", "fun"]

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
					tagged=pos_tag(h)
					if tagged[0][1] == "DT":
						"trash"
					if tagged[0][1]=="JJR":
						"50:50, few tokens"
					if tagged[0][1]=="JJS":
						"this is all trash"
					#remember to re-visit per notes
					if tagged[0][1]=="IN" and tagged[0][0] =="up":#not in ["on", "within", "between", "past", "at", "as", "by", "if", "than", "after", "in", "of", "like", "out", "for", "with", "about", "over", "from"]:
						print h, tagged
					
										
					if h[0] in include_pre_context or h[2] in include_post_context:
					#	print h
						h0dict[h[0]]=h0dict[h[0]]+1
						h2dict[h[2]]=h2dict[h[2]]+1
					elif h[0] not in exclude_pre_context and h[2] not in exclude_post_context:
						if h[2]:#:=="days":
					#		print h
							h0dict[h[0]]=h0dict[h[0]]+1
							h2dict[h[2]]=h2dict[h[2]]+1
		print "We have {} items with a token count of {}".format(len(h0dict.keys()), sum(h0dict.values()))
		h0dict={k:v for k,v in h0dict.items() if v > 0}
		print "\n\n", number, "\n\pretext here be the results\n\n"
		print "\n".join([": ".join([k, unicode(h0dict[k]), ".".join(word2vecwordfinder([k], '/Users/ps22344/Downloads/chapter2/current/clusters_74_19_45_07_31.json'))]) for k in sorted(h0dict, key=h0dict.get, reverse=True)])
		#print "\n".join([": ".join([k, unicode(h2dict[k]), ".".join(word2vecwordfinder([k], '/Users/ps22344/Downloads/chapter2/current/clusters_74_19_45_07_31.json'))]) for k in sorted(h2dict, key=h2dict.get, reverse=True)])

		print "We have {} post items with a token count of {}".format(len(h2dict.keys()), sum(h2dict.values()))
		print "We have {} pre items with a token count of {}".format(len(h0dict.keys()), sum(h0dict.values()))


			
rebusfinder(dir, "worddict_full.json", numberdict, "b")



			

			
			
			
	
endtime=time.time()
print "This took us {} minutes".format((endtime-starttime)/60)	