import json
import codecs
import re

tt="lol(kid)"

#print tt[-3:-1]

print re.sub("[\(\)]", "XXXXX", tt)

