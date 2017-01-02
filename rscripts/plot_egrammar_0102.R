tt=read.csv(
'E:/cygwin/home/ps22344/Downloads/chapter2/spreadsheets/egrammarstats_only4cats_0102.csv', 
header=T, 
fileEncoding="UTF-8", 
sep="\t")

fix(tt)

rankplotter = function(data_set, category_column, rank_column)
{
print (summary(data_set));
print (colnames(data_set));
print (class(data_set[["N"]]));
#print (levels(factor(data_set[[rank_column]])));

for (c in levels(factor(data_set[[rank_column]])))
	{
	cat ("cati", c, "\n");
	barplot(data_set[data_set[[category_column]] == c, ][["Rank"]])
	}

}


rankplotter(tt[tt[["N"]]>1000,], "Category", "Rank")