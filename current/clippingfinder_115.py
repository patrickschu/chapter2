import json
import codecs
import os
from collections import defaultdict
import tokenfinder_1004 as tk

#IDing clippings
#make a dict of all words
#find words that match the beginning of other words. or the end?
# initial clipping, final clipping, medial clipping

#procedure is
# 1. clippingfinder - ID potnetial clippings, invoke picker to separate the good from the evil
# 2. sampler - add context to yeslist


#dont mess with this
with codecs.open('sampler_yes_post_3_chars_1120.json', 'r', 'utf-8') as jsoninput:
	pickerdict=json.load(jsoninput)
	print "length of pickerdict", len(pickerdict)

def picker(dictionary, output_name):
	yeslist=[]
	nolist=[]
	#sort alphabetically please
	for entry in sorted(dictionary.keys()):
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
	print "written to ", writejson



	
#dont mess with this
with codecs.open('/Users/ps22344/Downloads/chapter2/outputfiles/fulldict_1115.json', 'r', 'utf-8') as jsoninput:
	fulldict=json.load(jsoninput)
	print "length of dicti", len(fulldict)

def clippingfinder(length_list, dictionary, cutoff):
	"""
	This is kind of a roundabout way of doing this.
	"""
	outputdict=defaultdict(list)
	print "len dict before", len(dictionary)
	dictionary = {k:v for k,v in dictionary.items() if v > cutoff}
	print "len dict after", len(dictionary)
	for length in length_list:
		print length
		for entry in set([i for i in dictionary.keys() if not "/" in i]):
			if len(entry) < length + 3:
				pass
			else:
				#print entry[:length]
				for item in set([i for i in dictionary.keys() if i != entry and not "/" in i]):
					if item == entry[-length:]:
						outputdict[item].append(entry)
	picker(outputdict, "post_"+str(length)+"_chars_1120")
	os.system('say "your program has finished"')
			
# 		#take the first 3,4,5 characters. how many needed?
# 		iterate: if .startswith, add to list
# 		print the list. 
# 		evtl tokenfind it




def sampler(json_input, output_name):
	
	sampledict=defaultdict(list)
	with codecs.open(json_input, 'r', 'utf-8') as jsoninput:
		fulldict=json.load(jsoninput)
		print "length of dicti", len(fulldict)

	for entry in fulldict.keys():
		
		print entry
		samples=tk.tokenfinder(["\W"+entry+"\W"], "/Users/ps22344/Downloads/craig_0208", length=20)
		sampledict[entry]=samples
	with codecs.open("sampler_yes_"+output_name+".json", "w", "utf-8") as writejson:
		json.dump(sampledict, writejson)
	print "written to ", writejson


#step 1, IDing clippings, pre-choices
clippingfinder([2], fulldict, 5)
#step 2, use the sampler to add context
#sampler('picker_yes_post_3_chars_1120.json', "post_3_chars_1120")
#step 3: final decision based on context from sampler
#picker(pickerdict, "3chars_final_1117")



