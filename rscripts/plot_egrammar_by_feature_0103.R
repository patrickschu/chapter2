
setwd('E:/cygwin/home/ps22344/Downloads/chapter2/spreadsheets/')


tt=read.csv(
'E:/cygwin/home/ps22344/Downloads/chapter2/spreadsheets/egrammarstats_0106.csv', 
header=T, 
fileEncoding="UTF-8")

overall=read.csv(
'E:/cygwin/home/ps22344/Downloads/chapter2/spreadsheets/wordcounter_categories_0104.csv', 
header=T, 
fileEncoding="UTF-8",
sep="\t")

colnames(tt)

#compute means and stdev
tt=merge(tt, overall)#[overall[["Wordcount"]] > 100, ])
#this isnt really a mean, rather the per mio token frequency for this cat
#we could call it 'freq' but lets keep it consistent with other plotting
tt[["mean"]]= tt[["sum"]]/tt[["wordcount"]]

grandmeans=aggregate(tt[["mean"]], list("feature"=tt[['feature']]), mean)
grandstdev=aggregate(tt[["mean"]], list("feature"=tt[['feature']]), sd)
gg=cbind(grandmeans,grandstdev)
colnames(gg)=c("feature", "grand_mean", "feature_2", "grand_stdev")


meanplotter = function(data_set, feature_column, category_column, mean_column)
#this plots the means from mean_column 
#for each category in each feature in feature_column
{
#order dataset alphabetically
data_set=data_set[order(data_set[["feature"]], decreasing=F),]
data_set[[category_column]]=ordered(data_set[[category_column]], levels=c("m4m", "m4w", "w4w", "w4m"))
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

meanplotter(tt, "feature", "category", "mean")

