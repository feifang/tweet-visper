#!/usr/bin/env python

# Written by Karen Fang - karen.feifang@gmail.com
# A tool for extracting certain field(s) of tweet data (JSON) and display

# Revision history: 
# 2016/04/09 - implemented basic functionality including get_field() and get_field_with()
# 2016/04/09 - added method for user fields
# 2016/04/12 - added method for entities fields


import json
import string

data = '../pro_data/Springbreak_0311All_sim_nlp.json'

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

def get_user_field(data, key):
	with open(data, 'r') as f:
		result = []
		without_key = 0
		for line in f:
			if check_valid(line):
				user = json.loads(line)['user']
				if user[key]:				
					result.append(user[key])
				else: 
					without_key += 1
	print "Results:", len(result), "out of", len(result)+without_key, "tweets"
	return result
	
def get_entities_field(data, key):
	with open(data, 'r') as f:
		result = []
		without_key = 0
		for line in f:
			#if check_valid(line):
			if True:    # for sim_tweets/ nlp_tweets (no 'lang' field)
				entities = json.loads(line)['entities']
				if entities[key]:				
					result.append(entities[key])
				else: 
					without_key += 1
	print "Results:", len(result), "out of", len(result)+without_key, "tweets"
	return result
		
		
if __name__ == '__main__':
	print get_entities_field(data, 'pos')[:10]
	
	'''
	places = get_field(data, 'place')
	count = 0
	for place in places:
		if place['country_code'] == 'US' and place['place_type']!= 'poi':
			print place['country_code'], place['place_type'], place['name'], place['full_name'], place['attributes']
		elif place['place_type'] == 'poi':
			count += 1
	print 'count:', count
	'''
	