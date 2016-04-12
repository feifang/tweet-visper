# coding=utf-8
# Written by Karen Fang - karen.feifang@gmail.com
# A tool for generating full geo information of both tweets and users

# Revision history: 
# 2016/04/12 - 

import json
import string
import us
from pygeocoder import Geocoder
from tweet_reducer import save_json_to_file
from tweet_trending import load_json_from_file

filename = 'Springbreak_0311All_sim_nlp'
data = '../pro_data/Springbreak_0311All_sim_nlp.json'
outpath = '../pro_data/'

def get_geo_from_place(place):
	geo = {
		'name': place['name'],
		'full_name': place['full_name'],
		'country': place['country'],
		'country_code': place['country_code']
	}
	print place['place_type']
	# get state name for places in US 
	if place['country_code'] == 'US':
		if place['place_type'] == 'city':
			geo['state_code'] = place['full_name'][-2:]
			geo['state'] = us.states.lookup(geo['state_code']).name
		elif place['place_type'] == 'admin':
			geo['state'] = unicode(place['name'])
			geo['state_code'] = us.states.lookup(geo['state']).abbr
		# geocode, place name should be long enough (>14) to be significant
		elif place['place_type'] == 'poi' and len(place['full_name']) > 14:  
			print place['full_name']
			try: 
				g = Geocoder.geocode(place['full_name'])
				if g.country == 'United States':
					geo['state'] = g.state
					geo['state_code'] = g.state__short_name
					print geo
			except Exception, error:
				print "Not Found:",error
				pass
	return geo
	

# standalone function: input a tweet(JSON) and output a tweet(JSON) with nlp data 
def add_geo_data(tweet):
	# copy tweet data
	geo_tweet = tweet
	if geo_tweet['place']:
		geo_tweet['tweet_geo'] = get_geo_from_place(geo_tweet['place'])
	return geo_tweet
	
# process tweets in batch 
def geo_tweet(tweets):
	for tweet in tweets:
		tweet = add_geo_data(tweet)
	return tweets

# process tweets from file to file
def get_geo_tweet(data):
	tweets = load_json_from_file(data)
	geo_tweets = geo_tweet(tweets)
	save_json_to_file(geo_tweets, '\n', outpath, filename+'_geo.json')
	
	

if __name__ == '__main__':
	get_geo_tweet(data)

