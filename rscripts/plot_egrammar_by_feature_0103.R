
setwd('E:/cygwin/home/ps22344/Downloads/chapter2/spreadsheets/')


tt=read.csv(
'E:/cygwin/home/ps22344/Downloads/chapter2/spreadsheets/egrammarstats_only4_0106.csv', 
header=T, 
fileEncoding="UTF-8")

overall=read.csv(
'E:/cygwin/home/ps22344/Downloads/chapter2/spreadsheets/wordcounter_categories_only4_0106.csv', 
header=T, 
fileEncoding="UTF-8",
sep="\t")

colnames(tt)

head(tt)
#compute means and stdev
tt=merge(tt, overall)
#this isnt really a mean, rather the per mio token frequency for this cat
#we could call it 'freq' but lets keep it consistent with other plotting
tt[["mean"]]= (tt[["sum"]])/(tt[["wordcount"]])
grandmeans=aggregate(tt[["mean"]], list("feature"=tt[['feature']]), mean)
grandstdev=aggregate(tt[["mean"]], list("feature"=tt[['feature']]), sd)
gg=cbind(grandmeans,grandstdev)
colnames(gg)=c("feature", "grand_mean", "feature_2", "grand_stdev")


meanplotter = function(data_set, feature_column, category_column, mean_column, filename)
#this plots the means from mean_column 
#for each category in each feature in feature_column
{
#order dataset alphabetically
data_set=data_set[order(data_set[["feature"]], decreasing=F),]
data_set[[category_column]]=ordered(data_set[[category_column]], levels=c("m4m", "m4w", "w4w", "w4m"))

count=0
print (length(levels(data_set[[feature_column]])))
png(paste(filename,".png"), width=279.4, height=215.9, unit="mm", res=500)
plot(
1,1, 
xlim=c(0, length(levels(data_set[[feature_column]]))), 
xlab="Feature",
ylim=c(-2, 2), 
ylab= "Distance to feature mean",
xaxt="n",
type="n")
axis(1,at=1:9, labels=c("Acronyms", "Capitals", "Clippings", "Emoticons", "Leetspeak", "Prosody", "Rebus", "Punctuation", "Single Letters"), cex.axis=0.8);
abline(a=0,b=0)

#iterate over features, add points
for (f in levels(tt[[feature_column]]))
	{
	cat("count", count)
	cat ("\nfeature", f, "\n");
	count= count + 1;
	featureset= tt[tt[[feature_column]] == f,];
	grandmean= gg[gg[["feature"]] == f, ][["grand_mean"]];
	grandstdev= gg[gg[["feature"]] == f, ][["grand_stdev"]];
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
dev.off()
}

meanplotter(tt, "feature", "category", "mean", "overfeatures")

