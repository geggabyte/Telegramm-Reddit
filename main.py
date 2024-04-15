import logging
import modules.reddit as reddit
import time
import json

#Documentations
#Telegramm:     https://core.telegram.org/bots/api#formatting-options
#Reddit:        https://www.reddit.com/dev/api/#listings

#Loading User settings
subreddits = open('subreddits.cfg', 'r').read().replace(' ', '').split('\n')
for a in subreddits:
    if a[0] == '#':
        subreddits.remove(a)
        
reddit.subreddits = subreddits
reddit.config = json.loads(open(".cfg", "r").read())
reddit.setConfig()
    

logging.basicConfig(filename='logs/info.log', encoding='utf-8', level=logging.INFO, format='%(asctime)s %(message)s')
timer = 60

while True:
    reddit.fetch()
    logging.info(f"Sleeping {timer} sec between fetching new posts")
    time.sleep(timer)