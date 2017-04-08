import json
import codecs








def categorymachine(json_in, outputname):
	"""
	The categorymachine takes a JSON input and iterates over its keys.
	We can then categorize said keys and enter them into a shorteningdict.
	Anything it cannot fit into the dictionary, it adds to a leftoverlist it prints out.
	This is used to put the acronyms ID with the acronymfinder in their place.  
	"""
	#note that we can use this to make machine below more flexible
	categories=['location', 'time', 'noun', 'X']

	shorteningdict={
	'clipping': {},
	'other': {},
	'delete':{}
	}

	for c in categories:
		for entry in shorteningdict:
			shorteningdict[entry][c] = []

	print shorteningdict
	leftoverlist=[]
	with codecs.open(json_in, "r", "utf-8") as jsoninput:
		inputdict=json.load(jsoninput)
	print "Dict is {} long".format(len(inputdict))
	
	
	#iterate over keys
	for item in inputdict:
		print "\n", item, "\n", len(item)
		ini=raw_input("Clipping, Other, or Delete? ")
		match=[i for i in shorteningdict.keys() if i.startswith(ini.lower())]
		if len(match) != 1:
			print "WARNING NO OR TOO MANY MATCHES IN DICT KEYS: ", len(match)
			leftoverlist.append(item)
		else:
			ini_2=raw_input("Location or Not? ")
			if ini_2 in ["L", "l"]:
				shorteningdict[match[0]]['location'].append(item)
			else:
				#shorteningdict[match[0]]['X'].append(item)
				ini_3=raw_input("Time or Not? ")
				if ini_3 in ["T", "t"]:
					shorteningdict[match[0]]['time'].append(item)
				else:
					ini_4=raw_input("Noun or Else? ")
					if ini_4 in ["N", "n"]:
						shorteningdict[match[0]]['noun'].append(item)
					else:
						shorteningdict[match[0]]['X'].append(item)
	print shorteningdict
	print "leftovers:\n", leftoverlist
	with codecs.open("clippingdict_"+outputname+"_1121.json", "w", "utf-8") as outputi:
		json.dump(shorteningdict, outputi)
	print "written to", outputi

filelist=[
"/Users/ps22344/Downloads/chapter2/current/clippingfiles/picker_yes_post_3chars_final_1117.json",
"/Users/ps22344/Downloads/chapter2/current/clippingfiles/picker_yes_post_4chars_final_1117.json",
"/Users/ps22344/Downloads/chapter2/current/clippingfiles/picker_yes_post_5chars_final_1117.json",
"/Users/ps22344/Downloads/chapter2/current/clippingfiles/picker_yes_post_6chars_final_1117.json",
"/Users/ps22344/Downloads/chapter2/current/clippingfiles/picker_yes_2chars_final_1117.json",
"/Users/ps22344/Downloads/chapter2/current/clippingfiles/picker_yes_3chars_final_1117.json",
"/Users/ps22344/Downloads/chapter2/current/clippingfiles/picker_yes_4chars_final_1117.json",
"/Users/ps22344/Downloads/chapter2/current/clippingfiles/picker_yes_5chars_final_1117.json",
"/Users/ps22344/Downloads/chapter2/current/clippingfiles/picker_yes_6chars_final_1117.json",
"/Users/ps22344/Downloads/chapter2/current/clippingfiles/picker_yes_7chars_final_1117.json",
]


for fili in filelist:
	print "_".join(fili.split("_")[-4:-2])
	categorymachine(fili, "test_"+"_".join(fili.split("_")[-4:-2]))	