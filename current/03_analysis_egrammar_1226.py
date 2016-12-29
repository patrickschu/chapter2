import egrammartools as eg
import clustertools as ct
import numpy as np
import time

#MAKE THEM ALL NUMPY
completestart=time.time()
listi=[]
dir="/home/ps22344/Downloads/craigbalanced_0601"

##prep
#add uniqs
uniqs, file_count, filedicti=ct.uniqarraymachine(dir, 0) 	
print "So many files", file_count
#listi.append(("uniqs", uniqs ))


#add cats
categories_dict, no_of_categories = ct.categorymachine(dir, "category1")
category1=ct.categoryarraymachine(dir, "category1", categories_dict)
listi.append(("category1", category1))

##collect features
rep_raw, rep_freq= eg.repeatedpunctuationfinder(dir)
print "shape", rep_freq.shape
rep_freq=rep_freq.sum(axis=1)
print "shape", rep_freq.shape
print range(0, [int(1) if len(rep_freq.shape) < 2 else rep_freq.shape[1] for i in [1]][0])
listi.append((["repeated_punctuation"+str(count) for count in range(0, [int(1) if len(rep_freq.shape) < 2 else rep_freq.shape[1] for i in [1]][0])], rep_freq))


leet_raw, leet_freq= eg.leetcounter(dir)
print "shape", leet_freq.shape
leet_freq=leet_freq.sum(axis=1)
listi.append((["leetspeak"+str(count) for count in range(0, [int(1) if len(leet_freq.shape) < 2 else leet_freq.shape[1] for i in [1]][0])], leet_freq))



#all rebus go together
rebfor_raw, rebfor_freq= eg.rebusfinder_for(dir)
rebto_raw, rebto_freq= eg.rebusfinder_to(dir)
rebtoo_raw, rebtoo_freq= eg.rebusfinder_too(dir)
rebus_freq=rebtoo_freq+rebto_freq+rebfor_freq
listi.append((["rebus"+str(count) for count in range(0, [int(1) if len(rebus_freq.shape) < 2 else rebus_freq.shape[1] for i in [1]][0])], rebus_freq))
print "shape of rebus", np.array(rebus_freq).shape
print rebus_freq


caps_raw, caps_freq=eg.capsfinder(dir, 0.5)
print "shape", caps_freq.shape
caps_freq=caps_freq.sum(axis=1)
print caps_freq.shape
listi.append((["capitalization"+str(count) for count in range(0, [int(1) if len(caps_freq.shape) < 2 else caps_freq.shape[1] for i in [1]][0])], caps_freq))

single_raw, single_freq=eg.singleletterfinder(dir)
print "shape", single_freq.shape
single_freq=single_freq.sum(axis=1)
listi.append((["single_letters"+str(count) for count in range(0, [int(1) if len(single_freq.shape) < 2 else single_freq.shape[1] for i in [1]][0])], single_freq))

clip_raw, clip_freq=eg.clippingcounter(dir)
print "shape", clip_freq.shape
clip_freq=clip_freq.sum(axis=1)
listi.append((["clippings"+str(count) for count in range(0, [int(1) if len(clip_freq.shape) < 2 else clip_freq.shape[1] for i in [1]][0])], clip_freq))

acro_raw, acro_freq=eg.acronymcounter(dir)
print "shape", acro_freq.shape
acro_freq=acro_freq.sum(axis=1)
listi.append((["acronyms"+str(count) for count in range(0, [int(1) if len(acro_freq.shape) < 2 else acro_freq.shape[1] for i in [1]][0])], acro_freq))

emos_raw, emos_freq=eg.emoticonfinder(dir)
print "shape", emos_freq.shape
emos_freq=emos_freq.sum(axis=1)
listi.append((["emoticons"+str(count) for count in range(0, [int(1) if len(emos_freq.shape) < 2 else emos_freq.shape[1] for i in [1]][0])], emos_freq))


pros_raw, pros_freq=eg.prosodycounter(dir)
print "shape", pros_freq.shape
pros_freq=pros_freq.sum(axis=1)
listi.append((["prosody"+str(count) for count in range(0, [int(1) if len(pros_freq.shape) < 2 else pros_freq.shape[1] for i in [1]][0])], pros_freq))

#put into one matrix
t=np.column_stack([i[1] for i in listi])


print type(t), t.shape
completeend=time.time()

#this is the t w/out uniq and category
wordmatrix_without_cat=t[:,1:]
print "matrix w/out cat", wordmatrix_without_cat.shape
#this one keeps the category but not the uniq
wordmatrix_with_cat=t
print "matrix wit cat", wordmatrix_with_cat.shape
catdicti=categories_dict


featuredict=[i[0] for i in listi if i[0] not in ["uniq", "category1"]]
#flatten it
featuredict=[n for i in featuredict for n in i]


print "feature dict", featuredict, len(featuredict)

print listi
##ADD SPELLING!!!!TO DO

def main(distance_metric, testmode=False):
	starttime=time.time()

	x=ct.clustermachine(wordmatrix_without_cat,distance_metric,4)
	print "These clusterings have less than 2 clusters\n{}\n\n".format("\n".join([str(c.name) for c in x if c.no_of_clusters < 2]))
	#PRINTING STUFF
	headline="\n\n-----------\n\n"
	print "Working with {} distance metric".format(distance_metric)
	excludelist=['total','no_of_categories', 'no_of_clusters', 'no_of_cats']
	#CROSS CLUSTERING COMPARISON
	for clustering in [c for c in x if c.no_of_clusters > 1]:
		cati=ct.Categorystats(wordmatrix_with_cat, clustering.name, clustering.labels)
		print "Categorystats done"
		sili=ct.Clusteringstats(wordmatrix_with_cat, wordmatrix_without_cat, clustering.name, clustering.labels).cluster_silhouette(distance_metric)
		print "Clusteringstats done"
	
		#GENERAL STATS
		print headline, headline, "CLUSTERING CALLED {} HAS {} CLUSTERS". format(clustering.getname()[1], clustering.no_of_clusters)
		print "Its silhouette score is {}".format(str(sili))
		stats=ct.Clusteringstats(wordmatrix_with_cat, wordmatrix_without_cat, clustering.name, clustering.labels).size_of_clusters()
		catstats=ct.Clusteringstats(wordmatrix_with_cat, wordmatrix_without_cat, clustering.name, clustering.labels).cats_per_cluster()
		for cluster in stats:
			print "\nCluster {} contains {} items, {} % of the total".format(cluster, stats[cluster], round(float(stats[cluster])/len(wordmatrix_without_cat)*100))
			for cat in [i for i in catstats[cluster] if not i in excludelist]:
				print "{} items of category {} make up {} % of this cluster".format(catstats[cluster][cat], "".join([i[0] for i in catdicti.items() if i[1] == int(cat)]), round(catstats[cluster][cat]/catstats[cluster]['total']*100))
		cats=ct.Categorystats(wordmatrix_with_cat, clustering.name, clustering.labels).size_of_categories()
		
		#STATS PER CAT
		print headline,"Statistics per category"
		for cat in [i for i in cats if not i in excludelist]:
			print "\nCategory {} has {} items".format("".join([i[0] for i in catdicti.items() if i[1] == int(cat)]), cats[cat]['total'])
			for entry in [i for i in cats[cat]['cat_per_cluster'] if not i in excludelist]:
				print "{} items or {} percent in cluster {}".format(cats[cat]['cat_per_cluster'][entry], round(float(cats[cat]['cat_per_cluster'][entry])/float(cats[cat]['total'])*100), entry)

		# #PREDICTIVE FEATURES
		print headline, "Strongly predictive features are"
		cents=ct.Centroidstats(wordmatrix_without_cat, clustering.name, clustering.labels, clustering.centroids).cluster_predictors(featuredict)
		if cents:
			for diff in cents:
				print "\nRaw Scores"
				print "Cluster {} and cluster {} are differentiated by \n{}\n\n\n".format(diff[0], diff[1], ", ".join([" : ".join(map(unicode, i[::-1])) for i in cents[diff]['raw_diff']][:10])) 
				print "Zscores"
				print "Cluster {} and cluster {} are differentiated by \n{}\n\n\n".format(diff[0], diff[1], ", ".join([" : ".join(map(unicode, i[::-1])) for i in cents[diff]['zscores_diff']][:10]))	
			
		
		#PROTOTYPES
		print headline, "Here is a typical document for each cluster"
		distance=distance_metric
		if distance_metric=='manhattan':
			distance='cityblock'
		print "We set the distance metric to {}".format(distance)
		docs=ct.Centroidstats(wordmatrix_without_cat, clustering.name, clustering.labels, clustering.centroids).central_documents(wordmatrix_with_cat, filedicti)
		if docs:
			for cluster in docs:
				print "\nCLUSTER {} \n".format(cluster)
				print docs[cluster][distance]
				with open(docs[cluster][distance][0]) as f:
					print f.read()
				if len(docs[cluster][distance]) > 8:
					print "\nOther files close by in cluster {}:\n".format(cluster)
					print ("{}\n"*8).format(*docs[cluster][distance][1:9])
	print headline, "Comparing clusterings"
	for clustering in [c for c in x if c.no_of_clusters > 1]:
		print headline, "CLUSTERING CALLED {} HAS {} CLUSTERS". format(clustering.getname()[0], clustering.no_of_clusters)
		print "Its silhouette score is {}".format(str(ct.Clusteringstats(wordmatrix_with_cat, wordmatrix_without_cat, clustering.name, clustering.labels).cluster_silhouette(distance_metric)))
	#all input does it just concatenate name + cluster # and supply clustering object to similarity measurement
	input=[(str(type(i.name)).split(".")[3].rstrip("'>")+"--"+str(i.no_of_clusters), i) for i in x]
	simi=ct.Clusteringsimilarity(wordmatrix_with_cat, wordmatrix_without_cat ,input)
	options=['adjustedrand_sim', 'adjustedmutualinfo_sim', 'jaccard_sim', 'v_sim', 'completeness_sim', 'homogeneity_sim', 'silhouette_score_sim']
	for o in options:
		print "\n---\n"
		ct.Clusteringsimilarity(wordmatrix_with_cat, wordmatrix_without_cat ,input).similarity_matrix(o)
	
	
	print "\n---\n"
	endtime=time.time()
	process=endtime-starttime
	print headline, "This took us {} minutes".format(process/60)


main('manhattan', testmode=False)




print "This took us {} minutes. So slow!".format((completeend-completestart)/60)