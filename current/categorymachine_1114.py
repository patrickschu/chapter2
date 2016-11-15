import json
import codecs


#note that we can use this to make machine below more flexible
categories=['location', 'school', 'X']

shorteningdict={

'acronym':{},
'alphabetism': {},
'blend': {},
'abbreviation': {},
'clipping': {},
'other': {},
'delete':{}

}


for c in categories:
	for entry in shorteningdict:
		shorteningdict[entry][c] = []

print shorteningdict





def categorymachine(json_in, outputname):
	"""
	The categorymachine takes a JSON input and iterates over its keys.
	We can then categorize said keys and enter them into a shorteningdict.
	Anything it cannot fit into the dictionary, it adds to a leftoverlist it prints out.
	This is used to put the acronyms ID with the acronymfinder in their place.  
	"""
	leftoverlist=[]
	with codecs.open(json_in, "r", "utf-8") as jsoninput:
		inputdict=json.load(jsoninput)
	print "Dict is {} long".format(len(inputdict))
	
	
	#iterate over keys
	for item in [i for i in sorted(inputdict, key=inputdict.get, reverse=True) if inputdict[i] > 5]:
		print "\n", item, "\n", len(item)
		ini=raw_input("ALphabetism, ACronym, ABbreviation, Blend, Clipping, Other, or Delete? ")
		match=[i for i in shorteningdict.keys() if i.startswith(ini.lower())]
		if len(match) != 1:
			print "WARNING NO OR TOO MANY MATCHES IN DICT KEYS: ", len(match)
			leftoverlist.append(item)
		else:
			ini_2=raw_input("Location or Not? ")
			if ini_2 in ["L"]:
				shorteningdict[match[0]]['location'].append(item)
			else:
				#shorteningdict[match[0]]['X'].append(item)
				in_3=raw_input("School or Not? ")
				if ini_2 in ["S", "s"]:
					shorteningdict[match[0]]['school'].append(item)
				else:
					shorteningdict[match[0]]['X'].append(item)
	print shorteningdict
	print "leftovers:\n", leftoverlist
	with codecs.open("shorteningdict_"+outputname+"_1115.json", "w", "utf-8") as outputi:
		json.dump(shorteningdict, outputi)


categorymachine('/Users/ps22344/Downloads/chapter2/current/output_acronyms4letters.json', "4")	