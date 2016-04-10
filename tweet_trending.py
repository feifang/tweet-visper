# coding=utf-8
# Written by Karen Fang - karen.feifang@gmail.com
# A tool for discovering trends in tweets 
# Inspired by Mining the Social Web, Second Edition(Chinese Edition), Page 41

# Revision history: 
# 2016/04/10 - 

import json
import string
from prettytable import PrettyTable

data = '../pro_data/Springbreak_0311All_sim.json'

# for sorting a list of tuples: sort by the first item
def getKey(item):
	return item[0]

def load_json_from_file(data):
	tweets = []
	with open(data, 'r') as f:
		for line in f:
			tweets.append(json.loads(line))
	return tweets

# print table facility
def print_cmd_table(data, fields, max_width_col):
	pt = PrettyTable(field_names = fields)
	[ pt.add_row(row) for row in data[:10]]
	pt.max_width[max_width_col] = 50
	pt.align = 'l'
	print pt

def get_top_retweets(tweets):
	retweets = [
				# store out a tuple of these three values ... 
				(tweet['retweeted_status']['retweet_count'],
				 tweet['retweeted_status']['user']['screen_name'],
				 tweet['retweeted_status']['text'])
				
				# ... for each tweet ...
				for tweet in tweets
				
				# ... so long as the status meets this condition.
					if tweet.has_key('retweeted_status')
				]
	#return sorted(retweets, reverse = True)
	return sorted(retweets, key = getKey, reverse = True)
	
def count_unique_users(tweets):
	user_set = set(tweet['user']['id']
					for tweet in tweets)
	print len(user_set)

def get_trends(tweets):
	trends = {}
	trends['tweets_count'] = len(tweets)
	trends['users_count'] = count_unique_users(tweets)
	

			

if __name__ == '__main__':
	tweets = load_json_from_file(data)
	top_retweets = get_top_retweets(tweets)
	#print top10_retweets
	print_cmd_table(top_retweets[:10], ['Count', 'Screen Name', 'Text'], 'Text')
	
	
	
	