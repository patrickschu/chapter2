import time
import codecs
import json
import re
import os
import clustertools as ct
import tokenfinder_1004 as tk
from collections import defaultdict
from nltk import pos_tag
from string import punctuation
print punctuation


#regexes and utilities
exclude_post_context=["+",  "(", "%"]#re.compile(r"^"+i+"$") for i in exclude_post_context]
punctuationregex="+|".join([re.escape(i) for i in [l for l in list(punctuation) if not l in exclude_post_context]])


#written numbers for quality control
writtennumberdict={}
writtennumbers=["zero", "one","two","three","four","five","six","seven","eight","nine","ten","eleven","twelve","thirteen","fourteen", "twenty", "thirty", "fourty", "fifty", "sixty", "fivefivefive"]	
for writtennumber in writtennumbers:
	writtennumberdict[writtennumber]=0

postwords= ["pickey", "far", "late", "much", "many", "heavy", "old"]
prewords_withpunct= ["ability", "head", "company", "cool", "full"]
prewords= ["band", "ass" ,"groups", "ub", "join"]

def rebusfinder_too(input_path):
	"""
	The rebus_too finder.
	It uses a list of expressions, pre-established thru "identifying_rebus_too_1022.py", to count 
	instances where a writer uses "2" instead of "too". 
	"""
	predict=defaultdict(int)
	postdict=defaultdict(int)
	
	for number in [2]:
		results=[]
		#this is the regular expression to identify instances of the number studied
		numberregex=re.compile("\W([a-z]+)\s*("+punctuationregex+")?\s*("+unicode(number)+")(?:\s+)?("+punctuationregex+")?(?:\s+)?([a-z]+)\W")
		print numberregex.pattern
		#dicts to store statistics about context of number
		h0dict=defaultdict(int)
		h2dict=defaultdict(int)
		#lists to store results and previous search patterns fed into tokenfinder to avoid duplicate output
		previous_patterns=[]
		results=[]
		for pati in [i for i in os.listdir(input_path) if not i.startswith(".")]:
			for fil in [i for i in os.listdir(os.path.join(input_path, pati)) if not i.startswith(".")]:
				fili=codecs.open(os.path.join(input_path, pati, fil), "r", "utf-8")
				inputad=ct.adtextextractor(fili.read(), fil)
				inputad=ct.adcleaner(inputad, replace_linebreak=True)
				inputad=inputad.lower()
				hits=numberregex.findall(inputad)
				#this weeds out all the phonenumbers. 
				hits=[h for h in hits if h[0] not in writtennumberdict and h[2] not in writtennumberdict]
				for h in hits:
					#this is needed for instance where there is no punctuation
					
					h=[" " if i == "" else i for i in h]
					"""
					thus
					[(u'of', 'IN'), (u'2', 'CD'), (u',', ','), (u'single', 'JJ')]
					pre, "2", optional punctuation, post
					"""
					[pre, pre_punct, number, punct, post]=pos_tag(h)
					
					if (
									
					#unique items catcher
					(pre[0] in ["date"]) 
					or
					(pre[0] in ["it"] and post[0] in ["i"])
					or
					(pre[0] in ["cook"] and post[0] in ["im"])
					or
					(pre[0] in ["kids"] and post[0] in ["young"]) 
					or
					(pre[0] in ["life", "way"] and post[0] in ["short"])
					or
					(pre[0] in ["that"] and post[0] in ["hard"])
					or
					(pre[0] in ["real"] and post[0] in ["hope"])
					or
					(pre[0] in ["me"] and post[0] in ["if"])
					or
					(pre[0] in ["dogs"] and post[0] in ["if"])
					or
					(pre[0] in ["can"] and post[0] in ["but"])
					or
					(pre[0] in ["kool"] and not post[0] in ["even"])
					or
					(pre[0] in ["on"] and punct[0] not in [" "] and inputad.split()[inputad.split().index(pre[0])-1] == "later")# and (h[h.index(pre[0])] == "later"))
					or
					(pre[0] in ["love"] and punct[0] not in [" "] and post[0] in ["msg"])
					or
					(pre[0] in ["real"] and post[0] in ["have"])
					or
					#BIGGER NETS
					#you be too in front of punctuation catch
					(pre[0] in ["be", "b", "are", "r"] and punct[0] not in [" ", "-", ")"])
					or
					#this is if we know the pre-word and 2 is followed by punctuation
					# cf 'intellectualy ability 2. '
					(pre[0] in prewords_withpunct and punct[0] not in [" ", ")", ":"])
					or
					#this is if we know the word to follow
					# cf 'not 2 late.' collected in postwords
					(post[0] in postwords)
					or
					#this is if we know the word to precede
					(pre[0] in prewords)
					):
					
						print "\n\n***", [pre, number, punct, post], "**\n", os.path.join(input_path, pati, fil)
						results.append((pre, number, punct, post, os.path.join(input_path, pati, fil)))
						predict[pre[0]]=predict[pre[0]]+1
						postdict[post[0]]=postdict[post[0]]+1
		print "original result list is", len(results)
		seti=set(results)
		print "\n\n", seti
		print "the set is ", len(seti)
		overlap={k:results.count(k) for k in seti}
		print overlap
		print {k:overlap[k] for k in overlap if overlap[k] > 1}
		print "PRE CONTEXT"
		print "\n".join([": ".join([k, unicode(predict[k])]) for k in sorted(predict, key=predict.get, reverse=True)])
		print "POST CONTEXT"
		print "\n".join([": ".join([k, unicode(postdict[k])]) for k in sorted(postdict, key=postdict.get, reverse=True)])





rebusfinder_too("/home/ps22344/Downloads/craig_0208")