# Generic Reddit Mention Bot

## General
This is a skeleton for a Reddit bot.
The bot will look at the mentions for a user, and then can reply to those mentions, or do whatever you like.
Reading mentions requires authorization by the user, so you'll have to go through a oauth process to get some secret information relating to your user.

#### Quick Instructions
1. Make sure you have Python 3
2. Install requirements: `pip install --requirement /path/to/requirements.txt`
3. Create a database file next to mentionBot.py `touch /path/to/database.db`
4. Optionally seed the database with mention IDs you don't want to act on
5. Create a `secrets.py` file
6. Add the fowling variables to the secrets.py file `app_key`, `app_secret`, `access_token`, `refresh_token`
7. Assign to those variables the values you get in the next step
8. Instructions for getting your oauth secrets: [Reddit Tutorial](https://www.reddit.com/r/redditdev/comments/3lotxj/tutorial_how_to_migrate_your_existing_bots_from/)
9. Run the script: `python analyzeHistory.py`


#### Tips
- You can run it in a screen or tmux, so you can see the output and come back to it later to check on it
- You can turn output to stdout off by making `debug = False` in the script. This will still write logs to the database