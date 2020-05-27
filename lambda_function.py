import boto3
import os

from base64 import b64decode

from otd import onthisday, tweet

print('Loading function')



CONSUMER_KEY = boto3.client('kms').decrypt(CiphertextBlob=b64decode(os.environ['TWITTER_CONSUMER_KEY']))['Plaintext'].decode('utf-8')
CONSUMER_SECRET = boto3.client('kms').decrypt(CiphertextBlob=b64decode(os.environ['TWITTER_CONSUMER_SECRET']))['Plaintext'].decode('utf-8')
ACCESS_TOKEN = boto3.client('kms').decrypt(CiphertextBlob=b64decode(os.environ['TWITTER_ACCESS_TOKEN']))['Plaintext'].decode('utf-8')
ACCESS_TOKEN_SECRET = boto3.client('kms').decrypt(CiphertextBlob=b64decode(os.environ['TWITTER_ACCESS_TOKEN_SECRET']))['Plaintext'].decode('utf-8')



def lambda_handler(event, context):
    # event is a dictionary, e.g. event['key1'])
    headline = onthisday.get_otd_headline()
    print(headline)
    # if you don't want it to tweet then setup a key called test inside the event
    if "test" not in event and headline != onthisday.NO_MATCH_HEADLINE:
        print("tweeting the headline")
        tweet.tweet_headline(headline, 
                            consumer_key=CONSUMER_KEY,
                            consumer_secret=CONSUMER_SECRET,
                            access_token=ACCESS_TOKEN,
                            access_token_secret=ACCESS_TOKEN_SECRET)
    else:
        print("not tweeting")
    return headline
