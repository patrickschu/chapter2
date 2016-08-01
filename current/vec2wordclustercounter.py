#counting clusters
import os
import json
import codecs

pathi=os.path.expanduser(os.path.join("~/", "Downloads", "craigbalanced_0601"))


folders=[i for i in os.listdir(pathi) if not i.startswith(".")]
print folders

def vec2wordclustercounter(folderlist, threshold, remove_stopwords=True, remove_punct=True):
	"""
	
	This is stolen from the cluster_analysis dictmaker. 
	The dictmaker counts the words / items contained in the files found in the folders of folderlist.
	It returns a dictionary of all words that occur more often than the number threshold. 
	remove_stopwords used the stopword list defined above to ignore words. 
	remove_punct works with string.punctuation, cf above. 
	"""
	#threshold sets how many times a word needs to occur to be included in the featuredict
	vocab={}
	for folder in folderlist:
		filis=[i for i in os.listdir(os.path.join(pathi,folder)) if not i.startswith(".")]
		print "Building vocab: we have {} files in folder {}".format(len(filis), folder)
		#collect a dictionary with all words
		#lowercase them    
		for fili in filis:
			inputfile=codecs.open(os.path.join(pathi, folder, fili), "r", "utf-8").read()
			inputtext=ct.adtextextractor(inputfile, fili)
			#pre-processing here
			inputtext=adcleaner(inputtext ,replace_linebreak=True, remove_html=False)
			splittext=word_tokenize(inputtext)
			splittextlo=[i.lower() for i in splittext]	
			finaltext=[punctuationregex.sub("",i) for i in splittextlo]
			finaltext=[i for i in finaltext if i and i not in ['br']]	
			#do we want to lemmatize or things like that
			for word in finaltext:
				if word not in vocab:
					vocab[word]=1
				else:
					vocab[word]=vocab[word]+1
	print "Our vocab dictionary has {} entries".format(len(vocab))
	ct.dictwriter(os.path.join("~/", chapterdir[0], "outputfiles", "fulldict_"+time.strftime("%H_%M_%m_%d")), vocab)
	if remove_stopwords:
		vocab= {key:value for key, value in vocab.items() if key not in stopwords }
		print "After stop word removal, dict is {} long".format(len(vocab))
	if remove_punct:
		vocab= {key:value for key, value in vocab.items() if key not in punctuation }
		print "After punctuation removal, dict is {} long".format(len(vocab))
	featuredict= {key:value for key, value in vocab.items() if value > float(threshold) }
	print "Our feature dictionary has {} entries\n---------------\n".format(len(featuredict))
	print "This is our featuredict", featuredict
	ct.dictwriter(os.path.join("~/", chapterdir[0], "outputfiles", "featuredict_"+time.strftime("%H_%M_%m_%d")), featuredict)
	return featuredict