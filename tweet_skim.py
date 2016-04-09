# coding=utf-8
# Written by Karen Fang - karen.feifang@gmail.com
# A tool for extracting certain field(s) of tweet data (JSON) and display

# Revision history: 
# 2016/04/09 - implemented basic functionality including get_field() and get_field_with()

import json
import string

data = '../data/Springbreak_0311All.json'

def get_tweet_lang(tweet):
	tweet_json = json.loads(tweet)
	if 'lang' in tweet_json.keys():
		return tweet_json['lang']
	else:
		return ""
		
def check_valid(tweet):
	lang = get_tweet_lang(tweet) 
	if len(tweet) > 100 and lang=='en':
		return True;
	else:
		return False;

def get_field(data, key):
	with open(data, 'r') as f:
		result = []
		without_key = 0
		for line in f:
			if check_valid(line):
				tweet = json.loads(line)
				if tweet[key]:				
					result.append(tweet[key])
				else: 
					without_key += 1
	print "Results:", len(result), "out of", len(result)+without_key, "tweets"
	return result
	
def get_field_with(data, key, withkey):
	with open(data, 'r') as f:
		result = []
		without_key = 0
		for line in f:
			if check_valid(line):
				tweet = json.loads(line)
				if tweet[withkey]:
					if tweet[key]:
						result.append(tweet[key])
					else: 
						without_key += 1
	print "Results:", len(result), "out of", len(result)+without_key, "tweets"
	return result
		
		
if __name__ == '__main__':
	places = get_field(data, 'place')
	count = 0
	for place in places:
		if place['country_code'] != 'US':
			print place['country_code'], place['place_type'], place['name'], place['full_name']
			count += 1
	print 'count:', count
	
	