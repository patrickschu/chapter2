excluderegex=re.compile("^["+"|\\".join(exclude)+"]+$")
punctuationregex=re.compile("["+"|\\".join(list(punctuation))+"|\d+]+")
stopregex=re.compile(r"([\.|\?|\!|\-|,]+)(\w)")

sents=r=stopregex.sub(r"\g<1> \g<2>", ad)
			#print sents
			sents=sent_tokenize(sents)
			#print sents
			sents=[s for s in sents if s not in exclude]
			#print sents
			sents=[re.split(r"(<br/>|\n|\.\.+)", s) for s in sents]
			#print sents
			#flatten sents
			sents=[s for longsent in sents for s in longsent]
			#print sents
			sents=[s.lower() for s in sents if s and not excluderegex.match(s)]
			#print sents
			for sent in sents:
				sent=[punctuationregex.sub("",s) for s in sent.split()]