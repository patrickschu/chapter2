#deleting files from list file
import os


filelist=[]
f=open("spanishtoedelete.txt", "r")
for line in f:
	filelist.append(line.strip())
	print line.strip()
	
f.close()

print "yes"

for fili in filelist:
	try:
		os.remove(fili)
		print "deleted", fili
	except:
		print fili
