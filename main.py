'''
Post to a bot account instead
Handle multiple lines of input
Handle emojiis/unicode characters
Add reddit api to randomly grab from r/copyPasta x
Add reddit api to default config file
add requirments.txt x?
    python-twitter
    praw
'''

import twitter
import configparser
import os, sys
import time
import praw
from random import randint
def parse_config():
    config = configparser.ConfigParser()
    if not os.path.exists('config.ini'):
        print("[!]Config file does not exists, creating now...")
        print("[*]Starting twitter api configuration...")
        config['Twitter'] = {'con_key' : input("[*]Enter consumer key: "),
                            'con_sec' : input("[*]Enter consumer secret: "),
                            'access_token_key' : input("[*]Enter access token key: "),
                            'access_token_secret' : input("[*]Enter access token secret: ")}

        ##Make reddit api a read only
        print("[*]Starting reddit api configuration...")
        config['Reddit'] = {'cli_id' : input('[*]Enter client ID: '),
                            'cli_sec' : input('[*]Enter client secret: '),
                            'pass' : input('[*]Enter password to reddit account: '),
                            'user_agent' : 'copyPasta twitter/reddit bot create by http://github.com/C0ntra99',
                            'username' : input('[*]Enter username of the reddit account: ')}

        with open('config.ini', 'w') as configfile:
            config.write(configfile)

    config.read('config.ini')
    con_key = config['Twitter']['con_key']
    con_sec = config['Twitter']['con_sec']
    acc_tok_key = config['Twitter']['access_token_key']
    acc_tok_sec = config['Twitter']['access_token_secret']

    cli_id = config['Reddit']['cli_id']
    cli_sec = config['Reddit']['cli_sec']
    passwd = config['Reddit']['pass']
    user_agent = config['Reddit']['user_agent']
    username = config['Reddit']['username']

    try:
        t_api = twitter.Api(consumer_key=con_key,
                            consumer_secret=con_sec,
                            access_token_key=acc_tok_key,
                            access_token_secret=acc_tok_sec,
                            sleep_on_rate_limit=True)
    except Exception as e:
        print("[!]ERROR: ", e)

    try:
        r_api = praw.Reddit(client_id=cli_id,
                            client_secret=cli_sec,
                            password=passwd,
                            user_agent=user_agent,
                            username=username)

    except Exception as e:
        print("[!]ERROR: ", e)

    return t_api, r_api

def twitter_post(r_title, r_body):

    ##Change this to reddit post
    o_tweet = r_body

    if len(o_tweet) > 280:
        lastTweet = o_tweet
        newTweet = []
        newTweet.append("Title: "+r_title)

        ##Change the way to cut the tweet into several ones
        while len(lastTweet) > 265:
            tweet = lastTweet[:265]
            newTweet.append(tweet)
            lastTweet = lastTweet[265:]
            if len(lastTweet) < 265:
                newTweet.append(lastTweet)

        print("[*]Total tweets: {}".format(len(newTweet)))
        print(newTweet)
'''
        if len(newTweet) > 15:
            a = input("[!]This will be over 15 tweets, due to twitter API limit there must be a 15 minute wait after 15 tweets. would you like to continue?[Y/n]: ")
            if a == '':
                a = 'Y'
                for num, tweet in enumerate(newTweet):
                    if num == 0:
                        post = t_api.PostUpdate(tweet)
                        #print(len(n_tweet[num]))
                    else:
                        post = t_api.PostUpdate(tweet,in_reply_to_status_id=lastTweetId)
                        #print(len(n_tweet[num]))
                    lastTweetId = post.id
                    print("Tweet: {} \nTweetID: {}".format(tweet,lastTweetId))
                    #if num+1 == 15:
                    #    print("[!]15 tweets hit, sleeping 15 minutes...")
            else:
                sys.exit()
    else:
        newTweet = "Title: " + r_title
        newTweet += o_tweet
        post = t_api.PostUpdate(newTweet)
        print("Tweet: {} \nTweetID: {}".format(o_tweet,post.id))
'''


def get_reddit_post():

    submissions = []
    for sub in r_api.subreddit('copypasta').hot(limit=100):
        submissions.append(sub)

    post = submissions[randint(0,len(submissions))]
    title = post.title
    for top_comment in post.comments:
        body = top_comment.body

    return title, body


def main():

    r_title, r_body = get_reddit_post()
    twitter_post(r_title, r_body)


if __name__ == "__main__":
    global t_api
    global r_api
    t_api, r_api = parse_config()
    main()
