import string
import json


data = '../data/Springbreak_All_0303_0405.json'
outfile = "../pro_data/user_tweet_pair.json"

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

#inspired by http://blog.amir.rachum.com/blog/2013/01/02/python-the-dictionary-playbook/
def get_pair(data):
	count = 0
	dic = {}
	with open(data, 'r') as f:
		for line in f:
			tweet = check_valid(line)
			if tweet:
				count += 1
				tweetid = tweet['id']
				userid = tweet['user']['id']
				tweet_info = {
						'id': tweetid,
						'time': tweet['created_at']
					}
				if tweet['coordinates']:
					tweet_info['coordinates'] = tweet['coordinates']['coordinates']
				pair = dic.setdefault(userid, [])  #userid might exist already, otherwise []
				pair.append(tweet_info)
	print len(dic), "users with", count, "tweets"
	return dic
	
if __name__ == '__main__':
	json.dump(get_pair(data), open(outfile,'w'))