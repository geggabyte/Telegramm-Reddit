#!/bin/sh

echo "This will remove .db and subreddits file. I reccomend you to copy those first"
read -p "Continue (y/n)?" choice
case "$choice" in 
  y|Y ) git restore . & git pull;;
  n|N ) echo "Good";;
  * ) echo "Invalid";;
esac