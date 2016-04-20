#!/usr/bin/env python

# Written by Karen Fang - karen.feifang@gmail.com
# A tool for generating customized reduced tweets based on API returned ones.

# Revision history: 
# 2016/04/09 - implemented basic functionality including get_field() and get_field_with()
# 2016/04/10 - fixed some I/O bugs, added retweeted_status


import json
import string
from datetime import datetime
from datetime import timedelta

filename = 'Springbreak_All_0303_0405'
data = '../data/Springbreak_All_0303_0405.json'
outpath = '../pro_data/'

geo_data = '../pro_data/Springbreak_All_0303_0405_sim_nlp_geo.json'

def get_tweet_lang(tweet):
	if tweet.has_key('lang'):
		return tweet['lang']
	else:
		return ""
		
def check_valid(line):
	# ensure it is a tweet rather than an error code
	if len(line) > 100: 
		tweet = json.loads(line)
		# tweet language is English
		if get_tweet_lang(tweet) == 'en':
			# if valid, return the tweet in JSON type
			return tweet;
	# if not valid, then None will be returned

def save_json_to_file(tweets, delimiter, path, filename):
	with open(path+filename, 'w') as out_file:
		for tweet in tweets:
			out_file.write(json.dumps(tweet) + delimiter)

def extract_tweet_entities(tweet):
	# extract the entities in text
	# Todo: for mentioned user, get he's id too, so as to get further info.
	screen_names = [ user_mention['screen_name']
						for user_mention in tweet['entities']['user_mentions']]
	hashtags = [ hashtag['text'].lower()
					for hashtag in tweet['entities']['hashtags']]
	urls = [ url['expanded_url']
				for url in tweet['entities']['urls']]
	symbols = [ symbol['text']
					for symbol in tweet['entities']['symbols']]
	# extract urls of uploaded photo (media entity)
	# sometimes might not appear 
	if tweet['entities'].has_key('media'):
		media = [ media['url']
					for media in tweet['entities']['media']]
	else: 
		media = []
	entities = {
		'screen_names': screen_names,
		'hashtags': hashtags,
		'urls': urls,
		'symbols': symbols,
		'media': media
	}
	return entities
	
def get_localtime(utc_time, offset):
	clean_timestamp = datetime.strptime(utc_time, '%a %b %d %H:%M:%S +0000 %Y')
	offset_hours = offset/3600   # offset: second -> hour
	local_timestamp = clean_timestamp + timedelta(hours=offset_hours)
	return local_timestamp.strftime('%Y-%m-%d %H:%M:%S')
	
def sim_tweet(data, tweet_keys, user_keys, entity_wanted = True):
	sim_tweets = []
	with open(data, 'r') as f:
		for line in f:
			tweet = check_valid(line)
			if tweet:
				sim_tweet = {}
				sim_user = {}
				user = tweet['user']
				for tweet_key in tweet_keys:
					sim_tweet[tweet_key] = tweet[tweet_key]
				for user_key in user_keys:
					sim_user[user_key] = user[user_key]
				sim_tweet['user'] = sim_user
				if entity_wanted:
					entities = extract_tweet_entities(tweet)
					sim_tweet['entities'] = entities
				# add local create time (if utc_offset is available)
				offset = user['utc_offset']
				if offset:
					sim_tweet['local_ctime'] = get_localtime(tweet['created_at'], offset)
				# add retweeted_status (if available)
				if tweet.has_key('retweeted_status'):
					sim_tweet['retweeted_status'] = tweet['retweeted_status']
				sim_tweets.append(sim_tweet)		
	return sim_tweets
			
# get simplified geo data for vis from sim_nlp_geo.json data (quick version)
def sim_geo(geo_data):
	sim_geo = []
	with open(geo_data, 'r') as f:
		for line in f:
			tweet = check_valid(line)
			if tweet:
				geo = tweet['tweet_geo']
				if geo['country_code']!='US':
					sim = {
						'country': geo['country'],
						'name': geo['name'],
						'sent': tweet['sentiment']['polarity']
					}
					sim_geo.append(sim)
		print len(sim_geo)
		return sim_geo
			
			
if __name__ == '__main__':
	'''
	# define customized list of keys for the reduced tweets
	tweet_keys_wanted = ['created_at', 'id', 'lang', 'text', 'in_reply_to_status_id', 'in_reply_to_user_id', 'coordinates', 'retweet_count', 'favorite_count', 'place']
	user_keys_wanted = ['id', 'screen_name', 'location', 'followers_count', 'friends_count', 'statuses_count', 'utc_offset', 'time_zone']
	sim_tweets = sim_tweet(data, tweet_keys_wanted, user_keys_wanted)
	
	
	print 'Processed and saved', len(sim_tweets), "tweets"
	# write to file line by line
	save_json_to_file(sim_tweets, '\n', outpath, filename+'_sim.json')
	'''
	
	s = sim_geo(geo_data)
	save_json_to_file(s, ',', outpath, filename+'_simgeo_others.json')
	