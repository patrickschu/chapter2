setwd('E:/cygwin/home/ps22344/Downloads/chapter2/spreadsheets/')
setwd('../spreadsheets/')

tt=read.csv(
'/Users/ps22344/Downloads/chapter2/spreadsheets/egrammarstats_only4_0309.csv', 
header=T, 
fileEncoding="UTF-8")

overall=read.csv(
'/Users/ps22344/Downloads/chapter2/spreadsheets/generalstats_perfeature_0309.csv', 
header=T, 
fileEncoding="UTF-8")

colnames(tt)

#tt[['category']]=ordered(tt[['category']], levels=c("m4m", "m4w", "w4w", "w4m"))

head(tt)
#compute means and stdev
#tt=merge(tt, overall)
#this isnt really a mean, rather the per mio token frequency for this cat
#we could call it 'freq' but lets keep it consistent with other plotting
tt[["mean"]]= (tt[["sum"]])/(tt[["wordcount"]])
print (tt)



meanplotter = function(data_set, feature_column, category_column, mean_column, filename)
#this plots the means from mean_column 
#for each category in each feature in feature_column
{
#order dataset alphabetically
data_set=data_set[order(data_set[[feature_column]], decreasing=F),]
data_set[[category_column]]=ordered(data_set[[category_column]], levels=c("m4m", "m4w", "w4w", "w4m"))
print (levels(data_set[[category_column]]))
#data_set[[category_column]]=ordered(data_set[[category_column]], levels=c("m", "w"))

count=0
print (length(levels(data_set[[feature_column]])))
png(paste(filename,".png"), width=279.4, height=215.9, unit="mm", res=500)
plot(
1,1, 
xlim=c(0, length(levels(data_set[[feature_column]]))), 
xlab="Feature",
ylim=c(-1, 1), 
ylab= "Distance to feature mean (standard deviations)",
xaxt="n",
type="n")
axis(1,at=1:9, labels=c("Abbreviations", "Capitals", "Clippings", "Emoticons", "Leetspeak", "Prosody", "Rebus", "Punctuation", "Single Letters"), cex.axis=0.8);
abline(a=0,b=0)

#iterate over features, add points
for (f in levels(data_set[[feature_column]]))
	{
	cat("count", count)
	cat ("\nfeature", f, "\n");
	count= count + 1;
	cat ("\nlabels,data", data_set[[category_column]], "\n")
	featureset= data_set[data_set[[feature_column]] == f,]
	cat ("\nlabels", featureset[[category_column]], "\n")
	print (featureset[[category_column]])
	grandmean= overall[overall[["feature"]] == f, ][["mean"]];
	grandstdev= overall[overall[["feature"]] == f, ][["std"]];
	cat ("grand mean for this feature", grandmean, length(grandmean), "\n");
	cat ("stdev for this feature", grandstdev, length(grandstdev), "\n");
	temp= xtabs(featureset[[mean_column]]~featureset[[category_column]]);
	cat ("\nlabels", featureset[[category_column]], "\n")
	print (temp);
	print ("thus");
	print (temp-grandmean)
	print ((temp-grandmean)/grandstdev)
	temp= ((temp-grandmean)/grandstdev)
	xval=rep(count, length(temp))
	cat ("xval", xval)
	cat ("\nlabels", featureset[[category_column]], "\n")	
	text(xval, temp, label= featureset[[category_column]], col=palette()[ featureset[[category_column]]])
	}
dev.off()
}

meanplotter(tt, "feature", "category", "mean", "overfeatures_test")

