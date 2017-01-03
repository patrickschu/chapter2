
setwd('E:/cygwin/home/ps22344/Downloads/chapter2/spreadsheets/')


tt=read.csv(
'E:/cygwin/home/ps22344/Downloads/chapter2/spreadsheets/egrammarstats_only4cats_0102.csv', 
header=T, 
fileEncoding="ascii", 
sep="\t")

grandmeans=read.csv(
'E:/cygwin/home/ps22344/Downloads/chapter2/spreadsheets/egrammar_grandmeans_0103.csv', 
header=T, 
fileEncoding="UTF-8", 
sep="\t")


tt[["Category"]]=ordered(tt[["Category"]], levels=c("m4m", "m4w", "w4w", "w4m"))

print (colnames(tt))

meanplotter = function(data_set, feature_column, category_column, mean_column)
#this plots the means from mean_column 
#for each category in each feature in feature_column
{
count=0
print (length(levels(data_set[[feature_column]])))
plot(
1,1, 
xlim=c(0, length(levels(data_set[[feature_column]]))), 
ylim=c(-.7, .7), 
type="n")
abline(a=0,b=0)
#iterate over features, add points
for (f in levels(tt[[feature_column]]))
	{
	cat("count", count)
	cat ("\nfeature", f, "\n");
	count= count + 1;
	featureset= tt[tt[[feature_column]] == f,];
	grandmean= grandmeans[grandmeans[["Feature"]] == f, ][["Mean"]];
	grandstdev= grandmeans[grandmeans[["Feature"]] == f, ][["StandardDeviation"]];
	cat ("grand mean for this feature", grandmean, length(grandmean), "\n");
	cat ("stdev for this feature", grandstdev, length(grandstdev), "\n");
	temp= xtabs(featureset[[mean_column]]~featureset[[category_column]]);
	print (temp);
	print ("thus");
	print (temp-grandmean)
	print ((temp-grandmean)/grandstdev)
	temp= ((temp-grandmean)/grandstdev)
	xval=rep(count, length(temp));
	print (xval)
	points(xval, temp, pch= seq(1, length(temp)))
	lines (
setwd('E:/cygwin/home/ps22344/Downloads/chapter2/spreadsheets/')


tt=read.csv(
'E:/cygwin/home/ps22344/Downloads/chapter2/spreadsheets/egrammarstats_only4cats_0102.csv', 
header=T, 
fileEncoding="ascii", 
sep="\t")

grandmeans=read.csv(
'E:/cygwin/home/ps22344/Downloads/chapter2/spreadsheets/egrammar_grandmeans_0103.csv', 
header=T, 
fileEncoding="UTF-8", 
sep="\t")


tt[["Category"]]=ordered(tt[["Category"]], levels=c("m4m", "m4w", "w4w", "w4m"))

print (colnames(tt))

meanplotter = function(data_set, feature_column, category_column, mean_column)
#this plots the means from mean_column 
#for each category in each feature in feature_column
{
count=0
print (length(levels(data_set[[feature_column]])))
plot(
1,1, 
xlim=c(0, length(levels(data_set[[feature_column]]))), 
ylim=c(-.7, .7), 
xaxt="n",
type="n")
abline(a=0,b=0)
#iterate over features, add points
for (f in levels(tt[[feature_column]]))
	{
	cat("count", count)
	cat ("\nfeature", f, "\n");
	count= count + 1;
	featureset= tt[tt[[feature_column]] == f,];
	grandmean= grandmeans[grandmeans[["Feature"]] == f, ][["Mean"]];
	grandstdev= grandmeans[grandmeans[["Feature"]] == f, ][["StandardDeviation"]];
	cat ("grand mean for this feature", grandmean, length(grandmean), "\n");
	cat ("stdev for this feature", grandstdev, length(grandstdev), "\n");
	temp= xtabs(featureset[[mean_column]]~featureset[[category_column]]);
	print (temp);
	print ("thus");
	print (temp-grandmean)
	print ((temp-grandmean)/grandstdev)
	temp= ((temp-grandmean)/grandstdev)
	xval=rep(count, length(temp));
	print (xval)
	text(xval, temp, label= featureset[[category_column]], col=seq(1,4))
	print ("assi")
	}
legend=0 
}

meanplotter(tt, "Feature", "Category", "Mean")

