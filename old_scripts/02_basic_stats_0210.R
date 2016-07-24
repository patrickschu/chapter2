#craig=read.csv(file.choose(), header=T)
#summary(craig)

#write.csv(xtabs(~craig$gender))

t=split(craig,craig$type)
#write.csv(xtabs(~t$ad$gender))

write.csv(tapply(t$ad$wordcount, t$ad$gender, sum))
