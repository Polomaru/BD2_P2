import json
from Backend import tw_proccesing as tw

def build_inverted_index():
    tp = tw.TweetProccesor()
    words = dict()
    for tweet_data in open("./data/data.json").readlines():
        tweet_data = json.loads(tweet_data)
        tokens = tp.tokenize_tweet(["content"])
        for token in tokens:
            if(words[token]
        words.update(tokens)


if __name__ == "__main__":
    build_inverted_index()