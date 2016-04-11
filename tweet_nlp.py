# coding=utf-8
# Written by Karen Fang - karen.feifang@gmail.com
# A tool for parsing tweets, part-of-speech tagging and performing sentiment analysis on tweets

# Revision history: 
# 2016/04/11 - tokenization, extract some Emoji and save as entities

import json
import string
from twokenize import normalizeTextForTagger, tokenizeRawTweetText
from tweet_reducer import save_json_to_file
from tweet_trending import load_json_from_file

filename = 'Springbreak_0311All_sim'
data = '../pro_data/Springbreak_0311All_sim.json'
outpath = '../pro_data/'

# emoji retrieved from https://www.piliapp.com/twitter-symbols/
people1 = u"😄😃😀😊😉😍😘😚😗😙😜😝😛😳😁😔😌😒😞😣😢😂😭😪😥😰😅😓😩😫😨😱😠😡😤😖😆😋😷😎😴😵😲😟😦😧😈👿😮😬😐😕😯😶😇😏😑"
people2 = u"👲👳👮👷💂👶👦👧👨👩👴👵👱👼👸😺😸😻😽😼🙀😿😹😾👹👺🙈🙉🙊💀👽💩"
people3 = u"🔥💫💥💢💦💧💤💨👂👀👃👅👄👍👎👌👊✊✋👐👆👇👉👈🙌🙏👏💪🚶🏃💃👫👪👬👭💏💑👯🙆🙅💁🙋💆💇💅👰🙎🙍🙇🎩👑👒👟👞👡"
people4 = u"👠👢👕👔👚👗🎽👖👘👙💼👜👝👛👓🎀🌂💄💛💙💜💚💔💗💓💕💖💞💘💌💋💍💎👤👥💬👣💭"


combined = [u"🌟", u"✨", u"👋"]

people1_u = [u'\U0001f604', u'\U0001f603', u'\U0001f600', u'\U0001f60a', u'\U0001f609', u'\U0001f60d', u'\U0001f618', u'\U0001f61a', u'\U0001f617', u'\U0001f619', u'\U0001f61c', u'\U0001f61d', u'\U0001f61b', u'\U0001f633', u'\U0001f601', u'\U0001f614', u'\U0001f60c', u'\U0001f612', u'\U0001f61e', u'\U0001f623', u'\U0001f622', u'\U0001f602', u'\U0001f62d', u'\U0001f62a', u'\U0001f625', u'\U0001f630', u'\U0001f605', u'\U0001f613', u'\U0001f629', u'\U0001f62b', u'\U0001f628', u'\U0001f631', u'\U0001f620', u'\U0001f621', u'\U0001f624', u'\U0001f616', u'\U0001f606', u'\U0001f60b', u'\U0001f637', u'\U0001f60e', u'\U0001f634', u'\U0001f635', u'\U0001f632', u'\U0001f61f', u'\U0001f626', u'\U0001f627', u'\U0001f608', u'\U0001f47f', u'\U0001f62e', u'\U0001f62c', u'\U0001f610', u'\U0001f615', u'\U0001f62f', u'\U0001f636', u'\U0001f607', u'\U0001f60f', u'\U0001f611']
people2_u = [u'\U0001f472', u'\U0001f473', u'\U0001f46e', u'\U0001f477', u'\U0001f482', u'\U0001f476', u'\U0001f466', u'\U0001f467', u'\U0001f468', u'\U0001f469', u'\U0001f474', u'\U0001f475', u'\U0001f471', u'\U0001f47c', u'\U0001f478', u'\U0001f63a', u'\U0001f638', u'\U0001f63b', u'\U0001f63d', u'\U0001f63c', u'\U0001f640', u'\U0001f63f', u'\U0001f639', u'\U0001f63e', u'\U0001f479', u'\U0001f47a', u'\U0001f648', u'\U0001f649', u'\U0001f64a', u'\U0001f480', u'\U0001f47d', u'\U0001f4a9']
people3_u = [u'\U0001f525', u'\U0001f4ab', u'\U0001f4a5', u'\U0001f4a2', u'\U0001f4a6', u'\U0001f4a7', u'\U0001f4a4', u'\U0001f4a8', u'\U0001f442', u'\U0001f440', u'\U0001f443', u'\U0001f445', u'\U0001f444', u'\U0001f44d', u'\U0001f44e', u'\U0001f44c', u'\U0001f44a', u'\u270a\u270b', u'\U0001f450', u'\U0001f446', u'\U0001f447', u'\U0001f449', u'\U0001f448', u'\U0001f64c', u'\U0001f64f', u'\U0001f44f', u'\U0001f4aa', u'\U0001f6b6', u'\U0001f3c3', u'\U0001f483', u'\U0001f46b', u'\U0001f46a', u'\U0001f46c', u'\U0001f46d', u'\U0001f48f', u'\U0001f491', u'\U0001f46f', u'\U0001f646', u'\U0001f645', u'\U0001f481', u'\U0001f64b', u'\U0001f486', u'\U0001f487', u'\U0001f485', u'\U0001f470', u'\U0001f64e', u'\U0001f64d', u'\U0001f647', u'\U0001f3a9', u'\U0001f451', u'\U0001f452', u'\U0001f45f', u'\U0001f45e', u'\U0001f461']
people4_u = [u'\U0001f460', u'\U0001f462', u'\U0001f455', u'\U0001f454', u'\U0001f45a', u'\U0001f457', u'\U0001f3bd', u'\U0001f456', u'\U0001f458', u'\U0001f459', u'\U0001f4bc', u'\U0001f45c', u'\U0001f45d', u'\U0001f45b', u'\U0001f453', u'\U0001f380', u'\U0001f302', u'\U0001f484', u'\U0001f49b', u'\U0001f499', u'\U0001f49c', u'\U0001f49a', u'\U0001f494', u'\U0001f497', u'\U0001f493', u'\U0001f495', u'\U0001f496', u'\U0001f49e', u'\U0001f498', u'\U0001f48c', u'\U0001f48b', u'\U0001f48d', u'\U0001f48e', u'\U0001f464', u'\U0001f465', u'\U0001f4ac', u'\U0001f463', u'\U0001f4ad']

Emoji_list = people1_u + people2_u + people3_u + people4_u + combined


def extract_emoji(tweet, Emoji_list):
	text = normalize(tweet['text'])
	#print "Before:", text
	emojis = []
	for emoji in Emoji_list:
		if emoji in text:
			text = text.replace(emoji, "")
			emojis.append(emoji)
			print "Extracted", emoji
	print "After:", text
	tweet['text'] = text
	tweet['entities']['emoji'] = emojis
	return tweet

def sep_emoji(str):
	emoji_list = []
	i = 0
	while i < len(str):
		emoji_list.append(str[i:i+2])
		i += 2
	print emoji_list
	return emoji_list
    
def tokenize(text):
	return tokenizeRawTweetText(text)

def normalize(text):
	return normalizeTextForTagger(text)
	
def add_nlp_data(tweet):
	nlp_tweet = extract_emoji(tweet, Emoji_list)
	nlp_tweet['tokens'] = tokenize(nlp_tweet['text'])
	
	return nlp_tweet

def nlp_tweet(tweets):
	for tweet in tweets:
		tweet = add_nlp_data(tweet)
	return tweets

def get_nlp_tweet(data):
	tweets = load_json_from_file(data)
	nlp_tweets = nlp_tweet(tweets)
	save_json_to_file(nlp_tweets, '\n', outpath, filename+'_nlp.json')
	
	
if __name__ == '__main__':
	get_nlp_tweet(data)

	
	