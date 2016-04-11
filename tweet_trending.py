# coding=utf-8
# Written by Karen Fang - karen.feifang@gmail.com
# A tool for discovering trends in tweets 
# Inspired by Mining the Social Web, Second Edition(Chinese Edition), Page 41

# Revision history: 
# 2016/04/11 - get trends (including tweets and users number, top retweets and entities)

from __future__ import print_function  
import json
import string
from prettytable import PrettyTable
from collections import Counter

filename = 'Springbreak_All_0303_0405_sim'
data = '../pro_data/Springbreak_All_0303_0405_sim.json'
outpath = '../trends/'

# for sorting a list of tuples
def getKey(item):
	return item[0]    #sort by the first item
	
def count_unique_users(tweets):
	user_set = set(tweet['user']['id']
					for tweet in tweets)
	return len(user_set)

def load_json_from_file(data):
	tweets = []
	with open(data, 'r') as f:
		for line in f:
			tweets.append(json.loads(line))
	return tweets

def save_list_to_csv(data, fields, filename):    #fields - String
	with open(outpath+filename,'w') as out:
		# use print instead of write to avoid UnicodeEncodeError
		print(fields, file = out)
		for row in data:
				print(str(row)[1:-1], file = out)    # get rid of "(" and ")"
	

# print table facility for command line
# e.g. print_cmd_table(get_top_retweets(tweets)[:10], ['Count', 'Screen Name', 'Text'], 'Text')
def print_cmd_table(data, fields, max_width_col):   #fields - List
	pt = PrettyTable(field_names = fields)
	[ pt.add_row(row) for row in data[:10]]   # top 10
	pt.max_width[max_width_col] = 50
	pt.align = 'l'
	print (pt)

def tweets_stat(tweets):
	with_media_count = 0
	with_url_count = 0
	with_mention_count = 0
	retweet_count = 0
	re_with_media_count = 0
	re_with_url_count = 0
	re_with_mention_count = 0
	ori_with_media_count = 0
	ori_with_url_count = 0
	ori_with_mention_count = 0
	tweet_count = len(tweets)
	for tweet in tweets:
		entities = tweet['entities']
		if entities['media'] != [] : with_media_count += 1
		if entities['screen_names'] != [] : with_mention_count += 1
		if entities['urls'] != [] : with_url_count +=1
		if tweet.has_key('retweeted_status'): 
			retweet_count += 1
			if entities['media'] != [] : re_with_media_count += 1
			if entities['screen_names'] != [] : re_with_mention_count += 1
			if entities['urls'] != [] : re_with_url_count +=1
		else:
			if entities['media'] != [] : ori_with_media_count += 1
			if entities['screen_names'] != [] : ori_with_mention_count += 1
			if entities['urls'] != [] : ori_with_url_count +=1
	return {'total': {'type':'tweet', 'count': tweet_count, 'has_media': with_media_count, 'has_link': with_url_count, 'has_mention': with_mention_count}, 'original': {'type':'original', 'count':tweet_count - retweet_count,  'has_media': ori_with_media_count, 'has_link': ori_with_url_count, 'has_mention': ori_with_mention_count}, 'retweet': {'type':'retweet', 'count': retweet_count, 'has_media': re_with_media_count, 'has_link': re_with_url_count, 'has_mention': re_with_mention_count}}
		


def get_top_retweets(tweets, save_to_csv = True):
	# Bug To Fix: ids are not unique, should only leave the tweets with largest count if duplicated. 
	retweets = sorted(
				[
				# store out a tuple of these three values ... 
				(tweet['retweeted_status']['retweet_count'],
				 tweet['retweeted_status']['id'],
				 tweet['retweeted_status']['user']['screen_name'],
				 tweet['retweeted_status']['text'])
				# ... for each tweet ...
				for tweet in tweets
				# ... so long as the status meets this condition.
					if tweet.has_key('retweeted_status')
				], key = getKey, reverse = True)
	if save_to_csv:
		header = "retweet_count,tweet_id,screen_name,text"    
		save_list_to_csv(retweets, header, "top_retweets.csv")
	return retweets
	
def get_top_entities(tweets, save_to_csv = True, print_to_cmd = True):
	screen_names = []
	hashtags = []
	urls = []
	symbols = []
	media = []
	for tweet in tweets:
		entities = tweet['entities']
		if entities['screen_names']: screen_names += entities['screen_names']
		if entities['hashtags']: hashtags += entities['hashtags']
		if entities['urls']: urls += entities['urls']
		if entities['symbols']: symbols += entities['symbols']
		if entities['media']: media += entities['media']
	top_entities = {
		'top_screen_names': Counter(screen_names).most_common(),
		'top_hashtags': Counter(hashtags).most_common(),
		'top_urls': Counter(urls).most_common(),
		'top_symbols': Counter(symbols).most_common(),
		'top_media': Counter(media).most_common()
	}
	for key, value in top_entities.iteritems():
		if save_to_csv:    # save Top 50
			save_list_to_csv(value[:50], "%s,count"%key, "%s.csv"%key)
		if print_to_cmd:    # print Top 10
			print_cmd_table(value, [key, "count"], key)
	return top_entities

def get_trends(data, filename = None):
	tweets = load_json_from_file(data)
	trends = {
		'users_count': count_unique_users(tweets), 
		'top_retweets': get_top_retweets(tweets),
		'top_entities': get_top_entities(tweets),
		'tweets_stat': tweets_stat(tweets)
	}
	if filename:
		with open(outpath+filename, 'w') as out:
			out.write(json.dumps(trends, indent=4))
		

if __name__ == '__main__':
	get_trends(data, "trends.json")
	
	
	
	
	
	
	
	