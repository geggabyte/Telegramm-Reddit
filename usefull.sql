-- Shows all subredits
select * from subreddits s 

-- Inserts new subreddit to lookup table
INSERT into subreddits (name) values ("memes")

-- Removes subreddit from lookup table
delete from subreddits where name = "memes"

-- Shows all posts sorted by subredit
select * from reddit_posts rp order by subreddit

-- Cleans history of posts
delete from reddit_posts