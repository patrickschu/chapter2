
#so excel changes the encoding to ASCII. Thanks for that. 
setwd('E:/cygwin/home/ps22344/Downloads/chapter2/spreadsheets/')


tt=read.csv(
'E:/cygwin/home/ps22344/Downloads/chapter2/spreadsheets/egrammarstats_only4cats_0102.csv', 
header=T, 
fileEncoding="ascii", 
sep="\t")

tt[["Category"]]=ordered(tt[["Category"]], levels=c("m4m", "m4w", "w4w", "w4m"))

rankplotter = function(data_set, category_column, rank_column)

#this plots a barplot per category (as listed in category_column
#with the category's rank (from rank_column) in each feature

{
print (summary(data_set));
print (colnames(data_set));
print (class(data_set[["N"]]));
#print (levels(factor(data_set[[rank_column]])));
#this is to make plotting easier: plot a 4 for # 1 ranked
data_set[["plotranks"]]= 5 - data_set[[rank_column]]
#arrange for four plots

png("eggi.png",  width=297, height=210, unit="mm", res=500)

par(mfrow=c(2,2))
for (c in levels(factor(data_set[[category_column]])))
	{
	cat ("cati", c, "\n");
	print (data_set[data_set[[category_column]] == c, ][["Rank"]]);
	print (data_set[data_set[[category_column]] == c, ][["plotranks"]]);
	bari=barplot(
	data_set[data_set[[category_column]] == c, ][["plotranks"]],
	main=paste(c),
	ylim=c(0,4),
	axes=FALSE);
	axis(2, at=1:4, labels= rev(c("1st", "2nd", "3rd", "4th")));
	text(bari, 0.5,
	c("Leetspeak", "Rebus", "Capitals", "Single Letter", "Clippings", "Acronyms", "Emoticons", "Prosody"),
	 cex=0.6, pos=3)
	}
dev.off()
}


rankplotter(tt[tt[["N"]]>1000,], "Category", "Rank")