# To run this code, first edit config.py with your configuration, then:
#
# mkdir data
# python twitter_stream_download.py -q Trump -d data
# 
# It will produce the list of tweets for the query "apple" 
# in the file data/stream_apple.json

import tweepy
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import urllib
import time
import argparse
import string
import config
import json
from time import localtime, strftime  #localtime could be replaced by gmtime

def get_parser():
    """Get parser for command line arguments."""
    parser = argparse.ArgumentParser(description="Twitter Downloader")
    parser.add_argument("-q",              #optional argument
                        "--query",
                        dest="query",      #the variable will be an attribute named "query" of the parser instance, in this case, args.query
                        help="Query/Filter",
                        default='-')
    parser.add_argument("-d",              #optional argument
                        "--data-dir",      
                        dest="data_dir",   #the variable will be an attribute named "data_dir" of the parser instance
                        help="Output/Data Directory")
    return parser


class MyListener(StreamListener):
    """Custom StreamListener for streaming data."""

    def __init__(self, data_dir, query):
        query_fname = format_filename(query)
        #get local current time
        c_time = strftime("%m%d%H%M", localtime())
        #filename = "/Users/karenfang/Documents/THESIS/fetch_twitter_data_demo1/%s/stream_%s_%s.json" % (data_dir, query_fname, c_time)
        filename = "%s/stream_%s_%s.json" % (data_dir, query_fname, c_time)
        #create a file at specified directory using the query string and current time    	
        self.outfile = filename 

    def on_data(self, data):
        try:
            with open(self.outfile, 'a') as f:
            	# filter invalid tweets
            	if len(data) > 100:
            		f.write(data)
            		# work around cleaning up tweets
            		#tweet = data.split(',"text":"')[1].split('","source')[0]
            		#encoded_text = urllib.quote(tweet)
            		#print "Tweet: ", tweet
            		print data
            		print " "
            		print "------------------------------"
                return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
            time.sleep(5)
        return True

    def on_error(self, status):
    	if status_code == 420:
            #returning False in on_data disconnects the stream
            return False
        print status
        return True
    
    def on_timeout(self):
		print >> sys.stderr, 'Timeout...'
		return True #Don't kill the stream


def format_filename(fname):
    """Convert file name into a safe string.

    Arguments:
        fname -- the file name to convert
    Return:
        String -- converted file name
    """
    return ''.join(convert_valid(one_char) for one_char in fname)


def convert_valid(one_char):
    """Convert a character into '_' if invalid.

    Arguments:
        one_char -- the char to convert
    Return:
        Character -- converted char
    """
    valid_chars = "-_.%s%s" % (string.ascii_letters, string.digits)
    if one_char in valid_chars:
        return one_char
    else:
        return '_'

@classmethod
def parse(cls, api, raw):
    status = cls.first_parse(api, raw)
    setattr(status, 'json', json.dumps(raw))
    return status

if __name__ == '__main__':
    parser = get_parser()
    args = parser.parse_args()
    auth = OAuthHandler(config.consumer_key, config.consumer_secret)
    auth.set_access_token(config.access_token, config.access_secret)
    api = tweepy.API(auth)

	# Bounding boxes for geolocations
	# Online-Tool to create boxes (c+p as raw CSV): http://boundingbox.klokantech.com/
    GEOBOX_HONGKONG = [113.835078,22.1533884,114.4069573,22.561968]
    twitter_stream = Stream(auth, MyListener(args.data_dir, args.query))
    #twitter_stream.filter(locations = GEOBOX_HONGKONG, async = True)
    
    # filter by keyword
    
    twitter_stream.filter(track=[args.query], async = True)
