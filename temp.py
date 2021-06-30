from bsi_sentiment.twitter import search_tweets_sn

tweets = search_tweets_sn(
  q="dosis diaria Amita",
#   since="2020-08-01",
#   until="2020-11-30",
  max_tweets=100
)

tweets.get_sentiment(method="vader")
tweets.to_csv("./results.csv")