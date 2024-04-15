import requests
import logging

logging.basicConfig(filename='logs/debug.log', encoding='utf-8', level=logging.DEBUG, format='%(asctime)s %(message)s')
telegramBase = ""
chanelId = ""
html = "&parse_mode=HTML"

def postText(text):
    response = requests.get(
        telegramBase + "sendMessage?" + chanelId + "&text=" + text + html
    )
    logging.info(response.json())


def postWithPhoto(text, image_link):
    response = requests.get(
        telegramBase
        + "sendPhoto?"
        + chanelId
        + "&photo="
        + image_link
        + "&caption="
        + text
        + html
    )
    if response.json()["ok"] is False:
        if response.json()["error_code"] == 400:
            postText(text + "\n(Image failure)")
    logging.info(str(response.json()) + "\n\n")
