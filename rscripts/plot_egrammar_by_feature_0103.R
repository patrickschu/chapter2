
setwd('E:/cygwin/home/ps22344/Downloads/chapter2/spreadsheets/')


tt=read.csv(
'E:/cygwin/home/ps22344/Downloads/chapter2/spreadsheets/egrammarstats_only4cats_0102.csv', 
header=T, 
fileEncoding="ascii", 
sep="\t")

grandmeans=read.csv(
'E:/cygwin/home/ps22344/Downloads/chapter2/spreadsheets/egrammarstats_grandmeans_0103.csv', 
header=T, 
fileEncoding="ascii", 
sep="\t")


tt[["Category"]]=ordered(tt[["Category"]], levels=c("m4m", "m4w", "w4w", "w4m"))

print (colnames(tt))

meanplotter = function(data_set, feature_column, category_column, mean_column)
#this plots the means from mean_column 
#for each category in each feature in feature_column
{
count=0
for (f in levels(tt[[feature_column]]))
	{
	cat ("\nfeature", f)
	count= count + 1
	featureset= tt[tt[[feature_column]] == f,]
	grandmean= grandmeans[grandmeans[["Feature"]] == f, ]["Mean"]
	grandstdev= grandmeans[grandmeans[["Feature"]] == f, ]["StandardDeviation"]
	cat ("grand mean for this feature", grand)
	temp= xtabs(featureset[[mean_column]]~featureset[[category_column]])
	print temp
	xval=rep(count, length(temp))
	plot(xval, temp, pch= c(1,2,3,4))
	
	}

}





meanplotter(tt, "Feature", "Category", "Mean")