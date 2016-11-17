import json
import codecs


with codecs.open('/Users/ps22344/Downloads/chapter2/current/shorteningdict_2_1115.json', 'r', 'utf-8') as jasi:
	dict=json.load(jasi)

print dict
