## plots the percentage of categories contained in each cluster
## relates them to 'expected', random assignment of data points
#data is based on table on pg 25 in chapter 2
#in the future, 'seq_along' might be a good R funcion to use

setwd("~/Desktop/rplots")
#last entry is expected value
cluster0=c(62, 29, 62, 55, 52)
cluster1=c(26, 12, 26, 23, 22)
cluster2=c(11, 27, 12, 19, 17)
cluster3=c(1, 31, 0, 3, 9)

clustering=data.frame(cluster0, cluster1, cluster2, cluster3, row.names=c("m4w", "m4m", "w4m", "w4w", "mean"))
#plot(c(100, 200), ylim=c(-100, 100), xlim=c(0, length(colnames(clustering))), type="n");
#text(x=1, y=50, "XXX")

clusterplotter = function(dataframe, filename)
#this takes a dataframe as input
#needs to be formatted colnames = clustering, categories and mean as row names
{
#we need to subtract 1 because of Python counting
no_of_clusters=c(0:(length(colnames(dataframe))-1));
print (no_of_clusters);
count=.5;
png(paste(filename,".png"), width=279.4, height=215.9, unit="mm", res=500)
plot(c(100, 250), ylim=c(-150, 250), xlim=c(0, length(colnames(dataframe))), ylab="Distance to expected value in percent", xlab= "Cluster (percentage of data set)", type="n", axes=FALSE);
axis(1,at=.5:3.5, labels=c("1 (52 %)", "2 (22 %)", "3 (17 %)", "4 (9 %)"), cex.axis=1)
#axis(side=1,seq(0, length(colnames(dataframe))-1, by=1));
axis(side=2, seq(-250, 250, by=50))
abline(h=0, col="red")

for (c in colnames(dataframe))
	{
	cat ('c: ', c, "\n");
	cat ('count', count, "\n");
	cat ('cluster: ', no_of_clusters[count], "\n");
	subseti=data.frame(dataframe[[c]]);
	rownames(subseti) = rownames(dataframe);
	#add label for expected value
	#text (x=count, y=0, as.character(subseti['mean',]), cex=1.5, col='red');	
	#compute percentages
	cat ("subseti");
	print (subseti);
	print((subseti-subseti['mean',])/(subseti['mean',]/100));
	percentageframe=(subseti-subseti['mean',])/(subseti['mean',]/100);
	print ("rownames");
	print (rownames(percentageframe))
	#set color setting numer
	colcount=0
	#set color vector
	colvec = c('red', 'black', 'green', 'blue')
	for (row in rownames(percentageframe))
	{
		
		if (row != 'mean')
		{
			colcount = colcount +1 
			cat ("row", row, "\n");
			text(x=count, y=percentageframe[row,], as.character(row), col = colvec[colcount])
			cat ("col count", colcount, "\n")
		}
	}
	
	count=count+1
	}
dev.off()	
}


clusterbarplotter = function(dataframe, filename)
#this takes a dataframe as input
#needs to be formatted colnames = clustering, categories and mean as row names
{
#we need to subtract 1 because of Python counting
no_of_clusters=c(0:(length(colnames(dataframe))-1));
print (no_of_clusters);
count=0;
#these are the x axis labels for each barplot
xlabels= c("Cluster 1 (52 % of data)", "Cluster 2 (22 % of data)", "Cluster 3 (17 % of data)", "Cluster 4 (9 % of data)")
png(paste(filename,".png"), width=279.4, height=215.9, unit="mm", res=500)
par(mfrow=c(2,2))

for (c in colnames(dataframe))
	{
	count=count+1
	cat ('c: ', c, "\n");
	cat ('count', count, "\n");
	cat ('cluster: ', no_of_clusters[count], "\n");
	subseti=data.frame(dataframe[[c]]);
	rownames(subseti) = rownames(dataframe);
	#add label for expected value
	#text (x=count, y=0, as.character(subseti['mean',]), cex=1.5, col='red');	
	#compute percentages
	cat ("subseti");
	print (subseti);
	print((subseti-subseti['mean',])/(subseti['mean',]/100));
	
	percentageframe=(subseti-subseti['mean',])/(subseti['mean',]/100);
	colnames(percentageframe) = c("vals")
	print ("perc fraome")
	print (percentageframe)
	print ("rownames");
	cat (class(percentageframe))
	#set color setting numer
	colcount=0
	#set color vector
	colvec = c('red', 'black', 'green', 'blue')
	barplot(
	percentageframe[-which(rownames(percentageframe)=='mean'), ], 
	main = xlabels[count],
	names.arg=c('m4w','m4m','w4m','w4w'),
	ylim = c(min(percentageframe[['vals']])-18, max(percentageframe[['vals']])+15),
	ylab="Distance to expected value in percent", 
	xlab= "Category")
	

	}
dev.off()	
}




clusterbarplotter(clustering, "barclusti")
