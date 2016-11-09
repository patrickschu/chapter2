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

postwords= ["pickey", "far", "late"]
prewords= ["ability", "head", "dick", "company"]
def rebusfinder_too(input_path, number_dictionary):
	"""
	The rebus_too finder.
	It uses a list of expressions, pre-established thru "identifying_rebus_too_1022.py", to count 
	instances where a writer uses "2" instead of "too". 
	"""
	for number in [2]:
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
					(pre[0] in prewords)
					#(post[0] in postwords)
					#or 
					#you be too in front of punctuation catch
					#(pre[0] in ["be", "b", "are", "r"] and punct[0] not in [" ", "-", ")"])
					):
						print "\n\n***", [pre, number, punct, post], "**\n", os.path.join(input_path, pati, fil)
						print inputad
						


rebusfinder_too("/Users/ps22344/Downloads/craig_0208","x")