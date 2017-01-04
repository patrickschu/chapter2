##
###GRAPHIC TEMPLATE
##DISS

#output PNGs on ltr size
png(paste(filename+".png"), width=279.4, height=215.9, unit="mm", res=500)

#ordering features and categories
data_set[["Category"]]=ordered(data_set[["Category"]], levels=c("m4m", "m4w", "w4w", "w4m"))
data_set[["Feature"]]=ordered(data_set[["Feature"]], levels=sort(levels(data_set[["Feature"]]), decreasing=F))
