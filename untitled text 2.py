import sklearn.metrics, numpy as np, scipy, re, os, itertools, urllib, json
from bs4 import BeautifulSoup 

# Array of pairwise distances between samples, or a feature array.
# labels : array, shape = [n_samples]
# clusters=np.array([[1.0,2,1,0,2], [1.0,2,1,0,2],[.0,0,0,1,2], [1.,1,1,1,1], [1.0,2,1,0,20], [1.0,2,1,0,10]])
# labels=np.array([1,2,2,1,3,3])
# print clusters
# t=sklearn.metrics.jaccard_similarity_score(labels, labels)
# print t
# t=[0]
# tt=[0,1,2,3]
# for combo in itertools.product(tt, t):
# 	print combo
# 	
# 	
# labels=np.array([1,2,1,1,2])
# value=np.array([0,100,0,0,100])
# 
# t=np.where(labels==2)
# print t
# print value[t]

overlap={(0,0): 1, (1,0):0.2, (1,1):0.0, (2,0):0.3, (2,1): 0.02}

t=overlap.items()
# print t

column_names=[i[0][0] for i in t]
# print column_names
# rows=[[i[0][1], i[1]] for i in t]
# print rows


column_names = list(set(column_names))
column_names = [str(element) for element in column_names]

header = '\t' + str('\t'.join(column_names)) # header col name
print header
for columns in column_names:
	print columns, "\t",
	# row name
	for row in column_names:
		key = (int(columns),int(row)) # key for accessing valu in dict
		try: 
			if key in overlap:
				value = overlap[key]
			else:
				value = overlap[key[::-1]] #reverse the tuple 
		except:
			print "out of clusters"
			break
		print value, '\t',

     	print('')

# 
# k=cors.keys()
# v=cors.values()
# print k
# print v
# rowlabels=[i[0] for i in k]
# columnlabels=[i[1] for i in k]
# 
# for k:v in cors:
# 	print k
# 
# template="{[*]}\t"*len(column_names)
# print template
# print template.format
# for row in rows:
# 	print template.format(row[0], row[1], "0")
# 	#first one needs to go to spot 0
# 	#print rows.index(row)

# 	0		1
# 0	0.5		0.2
# 
# 1	0.2		0


link=urllib.urlopen("https://books.google.com/ngrams/graph?content=The+Godfather&year_start=1972-&year_end=2008&corpus=15&smoothing=3&direct_url=t1%3B%2CThe%20Godfather%3B%2Cc0")
content=link.read()
soup=BeautifulSoup(content, "html.parser")
extract=soup.select('script[type="text/javascript"]')[4].string
data=re.findall('(\[.*\])', extract)
t=json.loads(data[0])
print t[0]['timeseries']

