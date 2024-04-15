Telegrammreddit

This is telegramm bot for reposting from reddit.

To properly utilize you will need to create `.cfg` file near `main.py` with following content:

```
{
    "telegramm_chat_id" : "",
    "telegramm_bot_id" : "",
    "reddit_auth_username" : "",
    "reddit_auth_password" : "",
    "reddit_username" : "",
    "reddit_password" : ""
}
```

After you can run `main.py`. Logs with all relevant (or not) data will appear inside `logs/debug.log` file.

File `usefull.sql` provides with all the querries that you will need to use bot. You can use [DBeaver](https://dbeaver.io/) to run those.