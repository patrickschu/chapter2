## plots the percentage of categories contained in each cluster
## relates them to 'expected', random assignment of data points
#data is based on table on pg 25 in chapter 2
#last entry is expected value
cluster0=c(62, 29, 62, 55, 52)
cluster1=c(26, 12, 26, 23, 22)
cluster2=c(11, 27, 12, 19, 17)
cluster3=c(1, 31, 0, 3, 9)

clustering=data.frame(cluster0, cluster1, cluster2, cluster3, row.names=c("m4w", "m4m", "w4m", "w4w", "mean"))


clusterplotter = function(dataframe)
#this takes a dataframe as input
#needs to be formatted colnames = clustering, categories and mean as row names


{

print ("watch this");
print (dataframe['mean',]);
for (c in colnames(dataframe))
{
	
print (c);
subseti=data.frame(dataframe[[c]]);
rownames(subseti) = rownames(dataframe);
print (subseti);

}
	
}

clusterplotter(clustering)
