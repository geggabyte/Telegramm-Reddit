Telegrammreddit

This is telegramm bot for reposting from reddit.

File `subreddits.cfg` should be filled with subreddits from which app will grab posts. Subreddists should be without `r/` and sepparated by new line. Additionally for "convenience" you can use # as a comments.

To run the programm you will need to create `.cfg` file near `main.py` with following content:

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

After you can run `main.py`. Logs with all relevant (or not) data will appear inside `logs/info.log` file.


```
-- Shows all posts sorted by subredit
select * from reddit_posts rp order by subreddit

-- Cleans history of posts
delete from reddit_posts
```

`telegramm.db` is SQLite data base containing history of all posts made. You can use [DBeaver](https://dbeaver.io/) to access it.


`start.sh` and `log.sh` are for running app with update & keeping eye on logs inside console.