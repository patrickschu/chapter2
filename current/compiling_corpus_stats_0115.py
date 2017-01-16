import os
import clustertools as ct
from collections import defaultdict

"""Compiling corpus stats"""

input_dir="/Users/ps22344/Downloads/craig_0208"


def wordcounter(input_dir):
	"""
	count words 
	"""
	for dir in [i for i in os.listdir(input_dir) if not i.startswith(".")]:
		catdicti=defaultdict(float)
		worddicti=defaultdict(float)
		print dir
		for fili in [i for i in os.listdir(os.path.join(input_dir, dir)) if not i.startswith(".")]:
			inputad=ct.Ad(os.path.join(input_dir, dir, fili))
			catdicti[inputad.meta['category1']]=catdicti[inputad.meta['category1']]+1
			worddicti[inputad.meta['category1']]=worddicti[inputad.meta['category1']]+inputad.wordcount
	print worddicti
			
	
			
			
			
		
wordcounter(input_dir)