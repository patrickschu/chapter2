#testing lars' twitter files
import codecs
import json
#import pandas


with codecs.open('/Users/ps22344/Desktop/tweets.csv', "r", "utf-8" ) as inputi:
	spread=inputi.read()


out=codecs.open("tweetout.txt", "a", "utf-8")


for line in spread.split("\n"):
	out.write(line.split(",")[0]+"\n")

out.close()


with codecs.open('/Users/ps22344/Desktop/heb_search_11.json', "r", "utf-8") as jsoninputi:
	data=jsoninputi.read()
	for line in data.split("\n"):
		#print line
		dict=json.loads(line)
		print dict['text']


	
	
