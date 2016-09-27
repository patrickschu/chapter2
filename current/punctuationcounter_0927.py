#FINISHED PRODUCT



"""
The punctuationcounter uses string.punctuation to create a dictionary of regexes.
These are used to identify non-Standard usage of punctuation. 
The returned punctuationdict= {regex_object: count_of_matches, regex_object_2: count_of_matches,}
""""
punctuationdict={
re.compile(r"(?:\s|\w)(!\?|\?!)(?:\s|\w)"):0
}

for stringi in punctuation:
	print stringi, "-->", re.escape(stringi)
	punctuationdict[re.compile(re.escape(stringi)+"{2,}")]=0	

print punctuationdict
print len(punctuationdict)


testi=" I am a lonely soul .. deep ?? but <<<<<<<!! !? what the heck ?!! so.... **haha here is some # ## punctuation @@ . "


for i in punctuationdict:
	result=i.findall(testi)
	if result:
		print i.pattern
		print result
	punctuationdict[i]=len(result)

print punctuationdict