import json
import codecs
import os
from collections import defaultdict
import tokenfinder_1004 as tk

#IDing clippings
#make a dict of all words
#find words that match the beginning of other words. or the end?
# initial clipping, final clipping, medial clipping



with codecs.open('/Users/ps22344/Downloads/chapter2/outputfiles/fulldict_1115.json', 'r', 'utf-8') as jsoninput:
	fulldict=json.load(jsoninput)
	print "length of dicti", len(fulldict)


def picker(dictionary, output_name):
	yeslist=[]
	nolist=[]
	#sort alphabetically please
	for entry in dictionary.keys():
		print "\n", entry, dictionary[entry]
		decision=raw_input("Yes or No? ")
		if decision in ["Y", "y"]:
			yeslist.append(entry)
		else:
			nolist.append(entry)
	print "yes"
	print yeslist
	print "\nno"
	print nolist
	outputdict={k:0 for k in yeslist}
	with codecs.open("picker_yes_"+output_name+".json", "w", "utf-8") as writejson:
		json.dump(outputdict, writejson)
	
#use picker to separate good from evil. write yeslist to json

#then run the yeslist thru the tokenfinder

#figure out what is real 


def clippingfinder(dictionary, cutoff):
	"""
	This is kind of a roundabout way of doing this.
	"""
	outputdict=defaultdict(list)
	print "len dict before", len(dictionary)
	dictionary = {k:v for k,v in dictionary.items() if v > cutoff}
	print "len dict after", len(dictionary)
	for length in [3]:
		print length
		for entry in set([i for i in dictionary.keys() if not "/" in i]):
			if len(entry) < length + 3:
				pass
			else:
				#print entry[:length]
				for item in set([i for i in dictionary.keys() if i != entry and not "/" in i]):
					if item == entry[:length]:
						outputdict[item].append(entry)
	picker(outputdict, "3chars_1116")
	# for finding in outputdict.keys():
# 		print "\n", finding, outputdict[finding]
	os.system('say "your program has finished"')
			
# 		#take the first 3,4,5 characters. how many needed?
# 		iterate: if .startswith, add to list
# 		print the list. 
# 		evtl tokenfind it

#clippingfinder(fulldict, 5)


def sampler(json_input, output_name):
	with codecs.open(json_input, 'r', 'utf-8') as jsoninput:
		fulldict=json.load(jsoninput)
		print "length of dicti", len(fulldict)

	for entry in fulldict.keys():
		sampledict=defaultdict(list)
		print entry
		samples=tk.tokenfinder(["\W"+entry+"\W"], "/Users/ps22344/Downloads/craig_0208")
		sampledict[entry]=samples
	with codecs.open("sampler_yes_"+output_name+".json", "w", "utf-8") as writejson:
		json.dump(outputdict, writejson)

sampler('/Users/ps22344/Downloads/chapter2/current/picker_yes_3chars_1116.json', "3chars_1116")
	



