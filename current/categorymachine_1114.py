import json
import codecs


listi=['aaa', 'bbb', 'acronym', 'trash']

shorteningdict={

'acronym':{'location':[], 'X':[]},
'alphabetism': {'location':[], 'X':[]},
'blend': {'location':[], 'X':[]},
'abbreviation': {'location':[], 'X':[]},
'other': {'location':[], 'X':[]},
'delete':{'location': [], 'X':[]}

}



def categorymachine(json_in, outputname):
	"""
	The categorymachine takes a JSON input and iterates over its keys.
	We can then categorize said keys and enter them into a shorteningdict.
	Anything it cannot fit into the dictionary, it adds to a leftoverlist it prints out.
	This is used to put the acronyms ID with the acronymfinder in their place.  
	"""
	leftoverlist=[]
	#read in json
	with codecs.open(json_in, "r", "utf-8") as jsoninput:
		inputdict=json.load(jsoninput)
	print "Dict is {} long".format(len(inputdict))
	#iterate over keys
	for item in inputdict.keys():
		print item, "\n", len(item)
		ini=raw_input("\nALphabetism, ACronym, ABbreviation, Blend, Other, or Delete? ")
		match=[i for i in shorteningdict.keys() if i.startswith(ini.lower())]
		if len(match) != 1:
			print "WARNING NO OR TOO MANY MATCHES IN DICT KEYS: ", len(match)
			leftoverlist.append(item)
		else:
			ini_2=raw_input("Location or Not? ")
			if ini_2 in ["L"]:
				shorteningdict[match[0]]['location'].append(item)
			else:
				shorteningdict[match[0]]['X'].append(item)
	#we need to make sure theyre in the same order as the printout
	#the json does not come in sorted i think so that needs to happen after
	print shorteningdict
	print "leftovers:\n", leftoverlist
	with codecs.open("shorteningdict_1114.json", "w", "utf-8") as outputi:
		json.dump(shorteningdict, outputi)


categorymachine('/Users/ps22344/Downloads/chapter2/current/output_acronyms6letters.json', "X")	