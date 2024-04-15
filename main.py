import logging
import reddit
import time
import json

#Documentations
#Telegramm:     https://core.telegram.org/bots/api#formatting-options
#Reddit:        https://www.reddit.com/dev/api/#listings

#Loading User settings
config = json.loads(open(".cfg", "r").read())
reddit.config = config
reddit.setConfig(config)
    

logging.basicConfig(filename='logs/info.log', encoding='utf-8', level=logging.INFO, format='%(asctime)s %(message)s')
timer = 60

while True:
    reddit.fetch()
    logging.info(f"Sleeping {timer} sec between fetching new posts")
    time.sleep(timer)