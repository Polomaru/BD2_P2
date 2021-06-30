import tweepy
import csv
import pandas as pd
import GetOldTweets3 as got
import time

credentials_df = pd.read_csv('credentials.csv',header=None,names=['name','key'])

consumer_key = credentials_df.loc[credentials_df['name']=='consumer_key','key'].iloc[0]
consumer_secret = credentials_df.loc[credentials_df['name']=='consumer_secret','key'].iloc[0]
access_token = credentials_df.loc[credentials_df['name']=='access_token','key'].iloc[0]
access_token_secret = credentials_df.loc[credentials_df['name']=='access_secret','key'].iloc[0]

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth,wait_on_rate_limit=True)

HashValue = input("Enter the hashtag you want the tweets to be downloaded for: ")

# Open/Create a file to append data
csvFile = open('result.csv', 'a')

#Use csv Writer
csvWriter = csv.writer(csvFile)

for tweet in tweepy.Cursor(api.search,q=HashValue).items():
    print (tweet.created_at, tweet.full_text)
    csvWriter.writerow([tweet.created_at, tweet.full_text.encode('utf-8')])

print ("Scraping finished and saved to "+HashValue+".csv")
#sys.exit()