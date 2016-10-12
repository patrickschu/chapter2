import json
import codecs




def word2vecwordfinder(search_terms, input_file):
	"""
	wordfinder looks up individual words in the clusters from word2vec.
	search_terms is list of strings, input_file the path to a JSON file of clusters.
	NOTE THAT THIS ONLY RETURNS FI
	"""
	with codecs.open(input_file, 'r', 'utf-8') as inputfile:
		clusters=json.load(inputfile)
	
	results=[k for term in search_terms for k in clusters.keys() if term in clusters[k]['words']]
	return results
	
	
	
t=word2vecwordfinder(["different"], '/Users/ps22344/Downloads/chapter2/current/clusterskmeans_54_19_10_07_30.json')
print t