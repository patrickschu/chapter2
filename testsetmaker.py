import sys
import re
import os
import shutil

pathi="craig_0208"

for f in [i for i in os.listdir(pathi) if not i.startswith(".")]:
	filis=[i for i in os.listdir(os.path.join(pathi,f)) if not i.startswith(".")]
	foldername=f
	os.makedirs(os.path.expanduser(os.path.join('~', 'Desktop', 'craig_testset_0522',foldername)))
	for fili in filis[:30]:
		for iter in range(0,3):
			shutil.copyfile(os.path.join(pathi,f, fili), os.path.expanduser(os.path.join('~', 'Desktop', 'craig_testset_0522',foldername, str(iter)+"_"+fili)))
	print "done with", f
