import csv
import snscrape.modules.twitter as sntwitter
import json
import math

def sizeint(n):
    if n > 0:
        return int(math.log10(n))+1
    elif n == 0:
        return 1

keyword = input('Enter a topic or keyword, please: ')
maxTweets = int(input('Enter the number of max tweets:  '))

json_file = open('temp.json', 'a', newline='\n', encoding='utf8')
json_file.truncate(0)
cont = 0
for i,tweet in enumerate(sntwitter.TwitterSearchScraper(keyword + ' lang:es until:2021-06-30 -filter:links -filter:replies').get_items())  :
        if i >= maxTweets :
            break 
        content = (tweet.content).replace("\n", " ").replace("\"","'")          
        my_details = {
            
            'id': tweet.id,
            'username' : tweet.username,
            'date' : tweet.date,
            'content' : content,
            'url' : tweet.url,
            'pos' : cont
        }
        cont += 2 + 19 + len(tweet.username) + len(str(tweet.date)) + len(content) + len (tweet.url) + 27 + sizeint(cont) + 4*6 + 4*2 +11
        json_file.write(json.dumps(my_details, ensure_ascii=False, default=str))
        json_file.write ('\n')
