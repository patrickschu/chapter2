import json
import codecs
import re

tt="lol(kid)"

#print tt[-3:-1]

#print re.sub("[\(\)]", "XXXXX", tt)


p1=(1,2)
p2=(4,4)

def dist(pt1, pt2):
	print abs(pt1[0]-pt2[0]) + abs(pt1[1]-pt2[1])
	
dist(p1,p2)

