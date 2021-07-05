import snscrape.modules.twitter as sntwitter
import json
import math

def sizeint(n):
    if n > 0:
        return int(math.log10(n))+1
    elif n == 0:
        return 1

class creator_index:

    def __init__(self) -> None:
        pass
    def make_new_index(self, keyword, maxTweets):
        # keyword = input('Enter a topic or keyword, please: ')
        # maxTweets = int(input('Enter the number of max tweets:  '))

        json_file = open('data.json', 'a', newline='\n', encoding='utf8')
        index_file = open('index.txt', 'a', newline='\n', encoding='utf8')
        json_file.truncate(0)
        index_file.truncate(0)
        cont = 0

        for i,tweet in enumerate(sntwitter.TwitterSearchScraper(keyword + ' lang:es until:2021-06-30 -filter:links -filter:replies').get_items())  :
                if i >= maxTweets:
                    index_file.write(str(format(cont, '09d')))
                    break 
                content = (tweet.content).replace("\n", " ").replace("\"","").replace("-"," ").replace('_'," ").replace('\\'," ").replace('\r'," ").replace('\t'," ")             
                my_details = {
                    
                    'id': tweet.id,
                    'username' : tweet.username,
                    'date' : tweet.date,
                    'content' : content,
                    'url' : tweet.url
                }
                index_file.write(str(format(cont, '09d')))
                cont += 2 + 19 + len(tweet.username) + len(str(tweet.date)) + len(content) + len (tweet.url) + 27 + 4*6 + 4*2 +11 -9
                json_file.write(json.dumps(my_details, ensure_ascii=False, default=str))
                index_file.write ('\n')
                json_file.write ('\n')
