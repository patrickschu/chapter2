#
setwd('E:/cygwin/home/ps22344/Downloads/chapter2/spreadsheets/')

##READ IN
tt=read.csv(
'E:/cygwin/home/ps22344/Downloads/chapter2/spreadsheets/egrammarstats_only4_0106_meansadded_ranksadded.csv', 
header=T, 
fileEncoding="UTF-8")






##COMPUTE MEANS AND RANKS
#tt=cbind(tt, overall)
#tt[["mean"]]= (tt[["sum"]])/(tt[["Wordcount"]])
#write.csv(tt, "outi.csv", fileEncoding="UTF-8")

#FORMAT aka C&P
tt[["category"]]=ordered(tt[["category"]], levels=c("m4m", "m4w", "w4w", "w4m"))


rankplotter = function(data_set, category_column, rank_column)
#this plots a barplot per category (as listed in category_column
#with the category's rank (from rank_column) in each feature
{
data_set=data_set[order(data_set[["feature"]], decreasing=F),]
print (summary(data_set));
print (colnames(data_set));
print (data_set[["feature"]]);
#print (levels(factor(data_set[[rank_column]])));
#this is to make plotting easier: plot a 4 for # 1 ranked
data_set[["plotranks"]]= 5 - data_set[[rank_column]]
#arrange for four plots

png("eggi.png",  width=297, height=210, unit="mm", res=500)

par(mfrow=c(2,2))
for (c in levels(factor(data_set[[category_column]])))
	{
	cat ("cati", c, "\n");
	print (data_set[data_set[[category_column]] == c, ][["rank"]]);
	print (data_set[data_set[[category_column]] == c, ][["plotranks"]]);
	bari=barplot(
	data_set[data_set[[category_column]] == c, ][["plotranks"]],
	main=paste(c),
	ylim=c(0,4),
	axes=FALSE);
	axis(2, at=1:4, labels= rev(c("1st", "2nd", "3rd", "4th")));
	#read: position @.25, to the top of it (pos), srt for vertical
	text(bari-0.25,  y=0.25, pos=4, c("Acronyms", "Capitals", "Clippings", "Emoticons", "Leetspeak", "Prosody", "Rebus", "Punctuation", "Single Letters"),
	cex=1,  srt=90)
	}
dev.off()
}


rankplotter(tt[tt[["N"]]>1000,], "category", "rank")
