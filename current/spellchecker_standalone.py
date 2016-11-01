#!/Users/ps22344/Downloads/virtualenv/chapter2_env/bin/python

import enchant

americandict = enchant.Dict("en_US")

def spellchecker(word):
	result=americandict.check(word)
	return result