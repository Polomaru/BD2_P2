import csv
import snscrape.modules.twitter as sntwitter
import json

keyword = input('Enter a topic or keyword, please: ')

maxTweets = 100

# csvFile = open('search.csv', 'a', newline='', encoding='utf8')

# csvWriter = csv.writer(csvFile)
# csvWriter.writerow(['n','id','username','date','content','url'])


json_file = open('data.json', 'a', newline='\n', encoding='utf8')
for i,tweet in enumerate(sntwitter.TwitterSearchScraper(keyword + ' lang:es until:2021-06-30 -filter:links -filter:replies').get_items())  :
        if i > maxTweets :
            break
        my_details = {
            'n': i,
            'id': tweet.id,
            'username' : tweet.username,
            'date' : tweet.date,
            'content' : tweet.content,
            'url' : tweet.url
        }
        json.dump(my_details, json_file, default=str, ensure_ascii=False, separators=(',', ':'))
        json_file.write('\n')

        # csvWriter.writerow([i,tweet.id, tweet.username ,tweet.date, tweet.content, tweet.url])
# csvFile.close()