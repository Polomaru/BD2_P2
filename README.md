# BD2_P2

Segunda parte proyecto base de datos 2.

## Enlaces

* [Página](https://tweetsretrieval.herokuapp.com)
* [Enlace público vídeo](https://drive.google.com/drive/folders/1cyDiACOwIBVAhRcoOxHjgOYv4-o3cUG0?usp=sharing)

## Autors

* [Paul Rios](https://github.com/Polomaru)
* [Efraín Córdova](https://github.com/ecordovaa)
* [David Soto](https://github.com/vid58)

## Built With

* python 
* pip
* flask(?)
* [snscrape](https://github.com/JustAnotherArchivist/snscrape) 

## Prerequisites

We need snscrape.
```sh
sudo apt-get update
pip install --upgrade git+https://github.com/JustAnotherArchivist/snscrape
```

## Get N Json's

```sh
  python data/tweets.py
  Enter a topic or keyword, please: covid 19
  Enter the number of max tweets: 200
```
Then this will get all 200 first tweets with the word "covid 19" until 30-06-21.

### If you want to change the query 

In the line 11 in data/tweets.py, is the specific query in the search in twitter, if you want to change the parameters of the search, like the language or if you want only the retweets, got to that line. An example is:

If I want to only search in a range of dates:


```py
for i,tweet in enumerate(sntwitter.TwitterSearchScraper(keyword + ' lang:es since:2021-06-25 until:2021-06-30  -filter:links -filter:replies').get_items())  :
```
This will get the tweets with the keyword, between 2021-06-25 and 2021-06-30. 

Reference [here.](https://www.tweetbinder.com/blog/twitter-advanced-search/)
Or [here.](https://twitter.com/search-advanced?lang=en-GB)




## Reference

How to use snscrape.

* https://medium.datadriveninvestor.com/how-to-build-a-twitter-scraping-app-with-python-b3fc069a19c6

Use of snscrape

* https://github.com/JustAnotherArchivist/snscrape

