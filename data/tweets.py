import csv
import snscrape.modules.twitter as sntwitter
import json

keyword = input('Enter a topic or keyword, please: ')
maxTweets = int(input('Enter the number of max tweets:  '))

json_file = open('data.json', 'a', newline='\n', encoding='utf8')
json_file.truncate(0)

for i,tweet in enumerate(sntwitter.TwitterSearchScraper(keyword + ' lang:es until:2021-06-30 -filter:links -filter:replies').get_items())  :
        if i >= maxTweets :
            break           
        my_details = {
            
            'id': tweet.id,
            'username' : tweet.user.username,
            'date' : tweet.date,
            'content' : (tweet.content).replace("\n", " "),
            'url' : tweet.url
        }
        json_file.write(json.dumps(my_details, ensure_ascii=False, default=str))
        json_file.write ('\n')
