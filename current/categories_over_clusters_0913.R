## plots the percentage of categories contained in each cluster
## relates them to 'expected', random assignment of data points
#data is based on table on pg 25 in chapter 2
#in the future, 'seq_along' might be a good R funcion to use

#last entry is expected value
cluster0=c(62, 29, 62, 55, 52)
cluster1=c(26, 12, 26, 23, 22)
cluster2=c(11, 27, 12, 19, 17)
cluster3=c(1, 31, 0, 3, 9)

clustering=data.frame(cluster0, cluster1, cluster2, cluster3, row.names=c("m4w", "m4m", "w4m", "w4w", "mean"))
plot(c(100, 200), ylim=c(-100, 100), xlim=c(0, length(colnames(clustering))-1), type="n");
text(x=1, y=50, "XXX")

clusterplotter = function(dataframe)
#this takes a dataframe as input
#needs to be formatted colnames = clustering, categories and mean as row names
{
#we need to subtract 1 because of Python counting
no_of_clusters=c(0:(length(colnames(dataframe))-1));
print (no_of_clusters);
count=0;	
plot(c(100, 200), ylim=c(-100, 100), xlim=c(0, length(colnames(dataframe))-1), type="n");


for (c in colnames(dataframe))
	{
	cat ('c: ', c, "\n");
	cat ('count', count, "\n");
	cat ('cluster: ', no_of_clusters[count], "\n");
	subseti=data.frame(dataframe[[c]]);
	rownames(subseti) = rownames(dataframe);
	#add label for expected value
	text (x=count, y=0, as.character(subseti['mean',]));	
	#compute percentages
	cat ("subseti");
	print (subseti);
	print((subseti-subseti['mean',])/(subseti['mean',]/100));
	
	#text (c(count, 0), as.character(c));
	count=count+1
	}
	
}

clusterplotter(clustering)
