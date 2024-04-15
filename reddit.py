import telegram
import requests
import requests.auth
import logging
import sqlite3
import random
import time

logging.basicConfig(filename='logs/info.log', encoding='utf-8', level=logging.INFO, format='%(asctime)s %(message)s')
config = {"t" : 1}

def setConfig(c):
    telegram.telegramBase = f'https://api.telegram.org/{c["telegramm_bot_id"]}/'
    telegram.chanelId = f'chat_id=@{c["telegramm_chat_id"]}' #this is PROD chanel id. change to test one for experementall purposes

def fetch():
    db = sqlite3.connect("telegramm.db")
    dbcursor = db.cursor()

    posts = []

    res = dbcursor.execute("SELECT name FROM subreddits")
    subreddits = res.fetchall()
    headers = connect()

    for subreddit in subreddits:
        
        response = getPosts(subreddit, headers)

        for a in response.json()['data']['children'][:6]:
            posts.append(a)
        
        remaining = response.headers['X-Ratelimit-Remaining']
        time_to_reset = response.headers['X-Ratelimit-Reset']
        if float(remaining) < 2:
            logging.info(f'I have {remaining} requests left for {time_to_reset} seconds, waiting for it')
            time.sleep(float(time_to_reset))
            logging.info('Good morning!')
            headers = connect()
        else:
            logging.info(f'I have {remaining} requests left for {time_to_reset} seconds')

    random.shuffle(posts)
    for post in posts:
        url = ''
        data = post['data']
        id = data['id']
        res = dbcursor.execute(f"SELECT post_id FROM reddit_posts WHERE post_id = '{id}'")
        if res.fetchone() is not None:
            logging.info('Post already utilized. Continue')
            continue

        author = data['author'].replace("'", "''")
        title = data['title'].replace("'", "''")
        dbcursor.execute(f"INSERT INTO reddit_posts (post_id, subreddit, user, title) VALUES ('{id}', '{data['subreddit_name_prefixed']}', '{author}', '{title}')")

        text = '<a href="' + 'https://www.reddit.com' + data['permalink'] + '">' + data['subreddit_name_prefixed'] + '</a> by <i>' + data['author'] + '</i> with upvote ratio ' + str(data['upvote_ratio']) + ':\n<b>' + data['title'] + '</b>\n' + data['selftext'] + '\n' + 'Number of current subs: ' + str(data['subreddit_subscribers'])

        if not data['is_video']:
            telegram.postWithPhoto(text, data['url'])
        else:
            telegram.postText(text)
        sleep_time = random.randint(20, 40)
        logging.info(f'Sleeping {sleep_time} sec between posting')
        time.sleep(sleep_time)
    db.commit()


def connect():
    client_auth = requests.auth.HTTPBasicAuth(config["reddit_auth_username"], config["reddit_auth_password"])
    post_data = {"grant_type": "password", "username": config["reddit_username"], "password": config["reddit_password"]}
    headers = {"User-Agent": config["reddit_username"]}
    response = requests.post("https://www.reddit.com/api/v1/access_token", auth=client_auth, data=post_data, headers=headers)
    return {"Authorization": response.json()['token_type'] + ' ' + response.json()['access_token'], "User-Agent": "ThrusterTk"}

def getPosts(subreddit, headers):
    try:
        return requests.get(f"https://oauth.reddit.com/r/{subreddit[0]}/top?t=hour&before:t5_{subreddit[0]}", headers=headers)
    except Exception as error:
        logging.info(f"Error occured while trying to reach subbreddit:\n {error}")
        return getPosts(subreddit, headers)
