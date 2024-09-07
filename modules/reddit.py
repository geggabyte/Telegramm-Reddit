import modules.telegram as telegram
import requests
import requests.auth
import logging
import sqlite3
import random
import time

logging.basicConfig(filename='logs/info.log', encoding='utf-8', level=logging.INFO, format='%(asctime)s %(message)s')
config = {"t" : 1}
subreddits = {}

old_time_to_reset = 1
old_remaining = 0

def setConfig():
    telegram.telegramBase = f'https://api.telegram.org/{config["telegramm_bot_id"]}/'
    telegram.chanelId = f'chat_id=@{config["telegramm_chat_id"]}' #this is PROD chanel id. change to test one for experementall purposes

def fetch():
    db = sqlite3.connect("modules/telegramm.db")
    dbcursor = db.cursor()

    posts = []
    headers = connect()

    for subreddit in subreddits:
        response = getPosts(subreddit, headers)
        logging.info(f'Reddit responded wih:\n{response}')
        for a in response.json()['data']['children'][:6]:
            posts.append(a)
            
        if 'X-Ratelimit-Remaining' in response.headers:
            remaining = response.headers['X-Ratelimit-Remaining']
            old_remaining = remaining
        else:
            logging.info('Response didn\'t contain \'X-Ratelimit-Remaining\' header. Using old one.')
            remaining = old_remaining - 1
        
        if 'X-Ratelimit-Reset' in response.headers:
            time_to_reset = response.headers['X-Ratelimit-Reset']
            old_time_to_reset = time_to_reset
        else:
            logging.info('Response didn\'t contain \'X-Ratelimit-Reset\' header. Using old one.')
            time_to_reset = old_time_to_reset

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
            logging.info(f'Post {id} already utilized. Continue')
            continue

        author = data['author'].replace("'", "''")
        title = data['title'].replace("'", "''")
        dbcursor.execute(f"INSERT INTO reddit_posts (post_id, subreddit, user, title) VALUES ('{id}', '{data['subreddit_name_prefixed']}', '{author}', '{title}')")

        text = '<a href="' + 'https://www.reddit.com' + data['permalink'] + '">' + data['subreddit_name_prefixed'] + '</a> by <i>' + data['author'] + '</i> with upvote ratio ' + str(data['upvote_ratio']) + ':\n<b>' + data['title'] + '</b>\n' + data['selftext'] + '\n' + 'Number of current subs: ' + str(data['subreddit_subscribers'])

        if not data['is_video']:
            telegram.postWithPhoto(text, data['url'])
        else:
            telegram.postText(text)
        sleep_time = random.randint(30, 90)
        logging.info(f'Sleeping {sleep_time} sec between posting')
        time.sleep(sleep_time)
    db.commit()
    logging.info('Cycle finished')


def connect():
    client_auth = requests.auth.HTTPBasicAuth(config["reddit_auth_username"], config["reddit_auth_password"])
    post_data = {"grant_type": "password", "username": config["reddit_username"], "password": config["reddit_password"]}
    headers = {"User-Agent": config["reddit_username"]}
    response = requests.post("https://www.reddit.com/api/v1/access_token", auth=client_auth, data=post_data, headers=headers)
    return {"Authorization": response.json()['token_type'] + ' ' + response.json()['access_token'], "User-Agent": "ThrusterTk"}

def getPosts(subreddit, headers):
    try:
        return requests.get(f"https://oauth.reddit.com/r/{subreddit}/top?t=hour&before:t5_{subreddit}", headers=headers)
    except Exception as error:
        logging.info(f"Error occured while trying to reach subbreddit {subreddit}:\n {error}")
        return getPosts(subreddit, headers)
