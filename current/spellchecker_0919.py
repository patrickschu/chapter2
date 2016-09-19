#!/Users/ps22344/Downloads/virtualenv/chapter2_env/bin/python


##Doing a spellchecker
## With pyenchant
##This needs to run in virtual env


import enchant



testi="I love going home on a Sanday nighht"

spelldicti=enchant.Dict("en_US")

print spelldicti.check("helo")

errors=[]

for word in testi.split():
	errors.append(spelldicti.check(word))

print errors
