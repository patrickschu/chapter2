
#so excel changes the encoding to ASCII. Thanks for that. 

tt=read.csv(
'E:/cygwin/home/ps22344/Downloads/chapter2/spreadsheets/egrammarstats_only4cats_0102.csv', 
header=T, 
fileEncoding="ascii", 
sep="\t")


rankplotter = function(data_set, category_column, rank_column)
{
print (summary(data_set));
print (colnames(data_set));
print (class(data_set[["N"]]));
#print (levels(factor(data_set[[rank_column]])));
#this is to make plotting easier: plot a 4 for # 1 ranked
data_set[["plotranks"]]= 5 - data_set[[rank_column]]
for (c in levels(factor(data_set[[category_column]])))
	{
	cat ("cati", c, "\n");
	print (data_set[data_set[[category_column]] == c, ][["Rank"]]);
	print (data_set[data_set[[category_column]] == c, ][["plotranks"]]);
	bari=barplot(
	data_set[data_set[[category_column]] == c, ][["plotranks"]],
	main=paste(c),
	axes=FALSE);
	axis(2, at=1:4, labels= rev(c("1st", "2nd", "3rd", "4th")));
	text(bari, 1,
	c("Leetspeak", "Rebus", "Capitalization", "Single Letters", "Clippings", "Acronyms", "Emoticons", "Prosody"),
	 cex=0.9, pos=3)
	}

}


rankplotter(tt[tt[["N"]]>1000,], "Category", "Rank")