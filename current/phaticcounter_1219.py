import codecs
import re
import clustertools as ct

#; and spellings that represent prosody or nonlinguistic sounds, such as a “calling voice” (helloooo), laughter, and other (nonhuman) noises



		


def prosodycounter(input_dir):
	"""
	 
	Returns a list of lists where each list contains raw and per word counts.
	
	"""
	start=time.time()
	#creating the search terms
	filelist=[
	
	]

	search_terms = []

	for fili in filelist:
		with codecs.open(fili, "r", "utf-8") as inputfile:
			acronym_dict=json.load(inputfile)
			for key in [i for i in acronym_dict.keys() if i not in ["delete", "other"]]:
				for cat in ['X']:
					#print "adding", acronym_dict[key][cat]
					search_terms = search_terms + acronym_dict[key][cat]
				for cat in ['noun']:
	 				#special treatment for nouns to accept plurals
					print "adding", acronym_dict[key][cat]
					search_terms = search_terms + [i if i in ["loc", "les", "sis"] else i + "s?" for i in acronym_dict[key][cat]]

	for i in search_terms:
		print i, search_terms.count(i)
			
	print "we have {} search terms".format(len(search_terms))
	print "we have {} set search terms".format(len(set(search_terms)))
	
	clipping_list=search_terms
	#start actual counting		
	excludelist=[]
	
	#dicts to store results
	dicti=defaultdict(float)
	matchesdicti=defaultdict(list)
	results=[]
	
	clipping_list=[re.compile("\W("+i+")\W") for i in clipping_list]
	#clipping_list=[re.compile("\W("+i+")\W") for i in clipping_list]
	clipping_list=set(clipping_list)
	#print [i.pattern for i in clipping_list]
	#iterate and match
	for dir in [i for i in os.listdir(input_dir) if not i.startswith(".")]:
		print dir
		for fili in [i for i in os.listdir(os.path.join(input_dir, dir)) if not i.startswith(".")]:
			with codecs.open(os.path.join(input_dir, dir, fili), "r", "utf-8") as inputtext:
				inputad=ct.adtextextractor(inputtext.read(), fili).lower()
			#result is a list of lists which contain matches for each regex/acronym
			wordcount=float(len(ct.tokenizer(inputad)))
			result=[([m for m in i.findall(inputad) if not m in excludelist], i.pattern) for i in clipping_list] 
			# o=[(r,os.path.join(input_dir, dir, fili)) for r in result if len(r[0]) > 2]
# 				if o:
# 					print o
			results.append([(len(matches), len(matches)/wordcount) for matches, pattern in result])
			for matches, pattern in result:
				#the dicti is {pattern:count, pattern: count, ...}
				dicti[pattern]=dicti[pattern]+len(matches)
				matchesdicti[pattern]=matchesdicti[pattern]+matches
	print "\n".join([":".join((i, str(dicti[i]), "|".join(set(matchesdicti[i])))) for i in sorted(dicti, key=dicti.get, reverse=True)])	
	#for entry in {k:v for k,v in matchesdicti.items() if v > 10}:
	#	print entry

	end=time.time()
	print "This took us {} minutes".format((end-start)/60)
	#for u in [[x[1] for x in i] for i in results]:
	#	print u
	print "shape of results, number of lists:", len(results),  "-- length of lists", set([len(i) for i in results])
	#for u in [[x[1] for x in i] for i in results]:
	#	print u
	return [[x[0] for x in i] for i in results], [[x[1] for x in i] for i in results] 
	
	
plus=[]
minus=[]

def listmaker():
	with codecs.open ("/home/ps22344/Downloads/chapter2/textfiles/non_standard_words_0920.txt", "r", "utf-8") as inputfile:
		for lini in inputfile.read().split(")\n(u"):
			print lini, "\n"
			ini=raw_input("X FOR YES ")
			if ini == "X":
				plus.append(lini)
			if ini == "ENDE":
				print plus
			else:
				minus.append(lini)