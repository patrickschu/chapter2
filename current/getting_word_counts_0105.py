import os
import codecs
import clustertools as ct


dir = "/home/ps22344/Downloads/craigbalanced_0601_small"


categorydict, catnumber = ct.categorymachine(dir, "category1")

print categorydict

def wordcounter(input_dir, category_tag, category_dict):
	"""
	counts the words per category in the files in input_dir.
	
	Parameters
	----------
	input_dir is the corpus directoty
	category_tag is the name of the tag to be extracted with tagextractor. 
	category_dict is a dictionary of categories to be computed over (category names as keys)
	e.g. <location="X"> would be input with "location" as the category_tag and a dict with {"Austin":0, "Dallas":0, ...}
	Returns
	-------
	something
	"""
	
	
	
	
	
