# coding=utf-8
# Written by Karen Fang - karen.feifang@gmail.com
# A tool for discovering trends in tweets 
# Inspired by Mining the Social Web, Second Edition(Chinese Edition), Page 41

# Revision history: 
# 2016/04/10 - 

from __future__ import print_function  
import json
import string
from prettytable import PrettyTable
from collections import Counter

data = '../pro_data/Springbreak_0311All_sim.json'
outfile = '../trends/%s'

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

#def save_list_to_csv(data, fields, file):
	

# print table facility
# e.g. print_cmd_table(get_top_retweets(tweets)[:10], ['Count', 'Screen Name', 'Text'], 'Text')
def print_cmd_table(data, fields, max_width_col):
	pt = PrettyTable(field_names = fields)
	[ pt.add_row(row) for row in data[:10]]
	pt.max_width[max_width_col] = 50
	pt.align = 'l'
	print (pt)

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
		with open(outfile%'top_retweets.csv','w') as out:
			# use print instead of write to avoid UnicodeEncodeError
			print("retweet_count,tweet_id,screen_name,text", file = out)
			for row in retweets:
				print(str(row)[1:-1], file = out)    # get rid of "(" and ")"
	return retweets
	
def get_top_entities(tweets, save_to_csv = True):
	screen_names = []
	for tweet in tweets:
		entities = tweet['entities']
		if entities['screen_names']: screen_names += entities['screen_names']
	c = Counter(screen_names)
	print (c.most_common()[:10])

def get_trends(tweets):
	trends = {}
	trends['tweets_count'] = len(tweets)
	trends['users_count'] = count_unique_users(tweets)
	trends['top_retweets'] = get_top_retweets(tweets)[:50]
	print (trends)
	

			

if __name__ == '__main__':
	tweets = load_json_from_file(data)
	#get_trends(tweets)
	#get_top_entities(tweets)
	get_top_retweets(tweets)
	
	
	
	
	