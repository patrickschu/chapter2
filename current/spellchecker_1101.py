#!/Users/ps22344/Downloads/virtualenv/chapter2_env/bin/python

import enchant



import codecs
import re
import clustertools as ct
import time
import os






def spellchecker(word):
	americandict = enchant.Dict("en_US")
	result=americandict.check(word)
	#print result
	return result


# for pati in [i for i in os.listdir('/Users/ps22344/Downloads/craig_0208') if not i.startswith(".")]:
# 		start=time.time()
# 		print pati
# 		for fili in [i for i in os.listdir(os.path.join('/Users/ps22344/Downloads/craig_0208', pati)) if not i.startswith(".")][:500]:
# 			fili=codecs.open(os.path.join('/Users/ps22344/Downloads/craig_0208', pati, fili), "r", "utf-8")
# 			inputad=ct.adtextextractor(fili.read(), fili)
# 			words=ct.tokenizer(inputad)
# 			
# 			for item in words:
# 				spellchecker(item)
# 		end=time.time()
# 		print "this took us {} minutes".format(end-start/60)