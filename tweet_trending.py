# coding=utf-8
# Written by Karen Fang - karen.feifang@gmail.com
# A tool for discovering trends in tweets 
# Inspired by Mining the Social Web, Second Edition(Chinese Edition), Page 41

# Revision history: 
# 2016/04/10 - 

import json
import string

data = '../pro_data/Springbreak_0311All_sim.json'

def top_retweets(tweets):
	retweets = [
				# store out a tuple of these three values ... 
				(tweet['retweet_count'],
				 tweet['retweeted_status']['user']['screen_name'],
				 tweet['text'])
				
				# ... for each tweet ...
				for tweet in tweets
				
				# ... so long as the status meets this condition.
					if status.has_key('retweeted_status')
				]
				
	return sorted(retweets, reverse = True)


def load_json_from_file(data):
	tweets = []
	with open(data, 'r') as f:
		for line in f:
			tweets.append(json.loads(line))
	return tweets

			

if __name__ == '__main__':
	tweets = load_json_from_file(data)
	
	