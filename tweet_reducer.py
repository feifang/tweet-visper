import json
import string

data = '../data/Springbreak_0311All.json'

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

		
#def change_timezone(time, localtime):

def extract_tweet_entities(tweet):
	# extract the entities in text
	screen_names = [ user_mention['screen_name']
						for user_mention in tweet['entities']['user_mentions']]
	hashtags = [ hashtag['text']
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
	
def sim_tweet(data, tweet_keys, user_keys, entity_wanted = True):
	sim_tweets = []
	sim_tweet = {}
	with open(data, 'r') as f:
		for line in f:
			tweet = check_valid(line)
			if tweet:
				user = tweet['user']
				for tweet_key in tweet_keys:
					sim_tweet[tweet_key] = tweet[tweet_key]
				for user_key in user_keys:
					sim_tweet['user_%s'%user_key] = user[user_key]
				if entity_wanted:
					entities = extract_tweet_entities(tweet)
					sim_tweet['entities'] = entities
			sim_tweets.append(sim_tweet)			
	return sim_tweets
			
			
			
if __name__ == '__main__':
	tweet_keys_wanted = ['created_at', 'id', 'text', 'in_reply_to_status_id', 'in_reply_to_user_id', 'coordinates', 'retweet_count', 'favorite_count', 'retweeted', 'place']
	user_keys_wanted = ['id']
	sim_tweets = sim_tweet(data, tweet_keys_wanted, user_keys_wanted)[:5]
	print sim_tweets
