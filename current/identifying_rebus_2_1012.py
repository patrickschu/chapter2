import time
import codecs
import json
import re
import os
import clustertools as ct
from collections import defaultdict
from nltk import pos_tag

starttime=time.time()
#check if we have this thing somewhere else and then delete from here. oops, this is included in our results
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

nounregex=re.compile("NN.?")
#do we need the to, do ect in post_context
#exclude_post_context=["years?", "months?", "weeks?", "days?", "hours?", "times?", "peoples?", "daughters?", "(boy|girl)?friends?", "girls?", "kids?", "boys?", "children", "dogs?", "jobs?", "things?", "(p|a)\.?m\.?", "to", "or" ]
exclude_post_context=["inche?s?", "wks?", "nd", "i", "sec", "stepping", "asap", "tattoos", "years?", "yrs", "months?", "weeks?", "days?", "hours?", "times?", "peoples?", "(boy|girl)?friends?", "(p|a)\.?m\.?", "to", "or", "full", "wana" ]

exclude_post_context=[re.compile(r"^"+i+"$") for i in exclude_post_context]

exclude_pre_context=["borderlands", "chicago", "c?ops?", "till?", "or", "and", "just", "f(oo|ee)?t", "last", "own", "hsv", "herpes"]
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
						#taking out trash
						if (
							(tagged[0][1] in ["DT", "JJS", "TO", "PRP$"]) 
							or
							(tagged[0][1]=="IN" and h[0] not in ["out", "like"])
							or
							(tagged[0][1] in ["VBG"] and h[0] not in ["talking", "responding", "waiting", "getting","looking", "going", "trying"])
							or
							(tagged[0][1] in ["VB", "VBD", "VBP", "VBZ"] and tagged[2][1] in ["JJ"])
							or
							#this is where we screw up
							(tagged[2][1] in ["NNS"] and h[2] not in ["chat", "kiss", "go", "know", "find", "do", "c", "knees"])
							or
							(tagged[2][1]=="IN")
							or
							(tagged[2][1]=="CC" and h[2] not in ["but"])
							or
							#we don't need this if we are to just ignore whatever goes thru all of it
							#TEMPTEMPTEMP
							(h[0] in ["be", "other", "s", "type", "was", "work", "im", "baths", "you", "maybe", "big", "day", "o", "round", "ride", "avengers", "kids", "had", "number", "have", "like", "here", "size", "got", "are", "send", "only", "have", "go", "is", "bedroom", "but", "beautiful", "nice"])
							or
							(h[2] in ["face", "new", "faced", "wonderful", "must", "min", "short", "si", "br", "step", "start", "so", "out", "story", "bdrm", "other", "out", "story", "yr", "looking", "more", "but", "hrs", "bedroom"])
							or 
							(tagged[2][1] in ["JJ", "VBD", "VBZ", "VBG"])
							):
							#print "killed",tagged, "\n"
							pass
						
						#finding the good
						elif (
							(tagged[2][1] in ["DT", "CD", "EX", "NNS", "VB"])
							or
							(tagged[2][1] in ["JJ"] and h[0] in ["opposed"])
							or
							(tagged[2][1] in ["PRP"] and not nounregex.match(tagged[0][1]))
							or
							(h[0] == "have" and h[2] in ["browse", "force", "go", "send", "talk"])
							or
							(h[0] == "like" and h[2] not in ["furry", "cuz", "straight"])
							or
							(h[0] in ["here"] and nounregex.match(tagged[2][1]))
							or
							#really what we are exluding here is anything non-Verb or Noun
							# we can consider replacing this with a regex
							(h[0] in ["need", "me", "pics"] and tagged[2][1] not in ["JJ", "JJR", "MD"])
							or 
							(h[0] in ["respond", "travel", "veldkum", "happness", "pool", "lots", "bbw", "willin", "luvz", "place", "time", "married", "pixs", "boy", "pictures", "brickz", "somebody", "memphis", "cell", "fear", "hoop", "open", "goes", "afraid", "speak", "lady", "needs", "attracted", "doms", "bottom", "head", "apply", "drive", "pic", "newer", "pinned", "luvs", "sumbody", "face", "due", "tryin", "line", "has", "close", "interested", "alot", "oral", "talk", "new", "girl", "up", "scared", "willing", "cam", "loves", "cock", "out", "u", "nice", "how", "free", "hard", "hope", "able", "someone", "man", "woman", "male", "down", "love", "luv", "ready", "want", "wants"]+["talking", "responding", "waiting", "getting","looking", "lookin", "going", "trying"])
							or
							(h[2] in ["brag", "blow", "grab", "feel", "send", "connect", "hearing", "say", "read", "contact", "please", "run", "host","kno", "talk", "just", "add", "text", "chill", "hang", "date", "find", "chat", "show", "u", "meet", "her", "hear", "me", "my", "b", "know", "play", "do", "suck", "go", "get"])
							):
							#print "hooked the plusloop", tagged
							#print "kept", tagged, "\n"
							pass
						else:
							if tagged[2][1]:#=="VB":# in ["VBP", "VBG"]:#=="go":#:# in ['my']:#, 'know', 'my']:#["me", "need", "man"]:# == "down":#h[2] not in ["have", "and", "like", "hear"]:
								print tagged
								#print "elseloop", tagged
								h0dict[h[0]]=h0dict[h[0]]+1
								h2dict[h[2]]=h2dict[h[2]]+1
								#h0dict[tagged[0][1]]=h0dict[tagged[0][1]]+1
								#h2dict[tagged[2][1]]=h2dict[tagged[2][1]]+1
									
	

						
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