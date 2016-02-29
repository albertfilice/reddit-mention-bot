from secrets import app_key, app_secret, access_token, refresh_token
import praw
import subprocess
import time
from collections import Counter
from prawoauth2 import PrawOAuth2Mini
import sys
import sqlite3
import requests

# Set up PRAW object and oauth stuff
r = praw.Reddit('UPDATE WITH UNIQUE AND DESCRIPTIVE STRING')
oauth_helper = PrawOAuth2Mini(r, app_key=app_key, app_secret=app_secret, access_token=access_token, scopes=['edit', 'privatemessages', 'history', 'save', 'identity', 'submit', 'read'], refresh_token=refresh_token)

# Connect to the database and make sure the table is properly set up
conn = sqlite3.connect('database.db')
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS mentions (id integer primary key autoincrement, mention_id text)")
c.execute("CREATE TABLE IF NOT EXISTS log (id integer primary key autoincrement, TS datetime default CURRENT_TIMESTAMP, message text)")

# Debugging flag
# Print to stdout if True
debug = True

# Set the user that you want to monitor the mentions of
user = 'yourUsernameHere'

# Function both print and log message to database
# Argument must be a list or a string
def log_message(message):
    if type(message) == str:
        if debug:
            print(message)
        c.execute("INSERT INTO log (message) VALUES (?)", (message,))
    elif type(message) == list:
        to_log = ""
        for part in message:
            to_log = str(to_log) + str(part) + " "
        to_log = to_log.strip()
        if debug:
            print(to_log)
        c.execute("INSERT INTO log (message) VALUES (?)", (to_log,))
    conn.commit()


# Attempt to post a reply
# If forbidden then skip and add to list of completed mentions
# If rate limit exception is thrown, wait a minute and try again
def post_reply(post, reply):
    post_successful = False
    while not post_successful:
        try:
            post.reply(reply)
            post_successful = True
        except praw.errors.RateLimitExceeded:
            log_message("Rate limit exceeded, trying again in 1 minute")
            time.sleep(60)
        except praw.errors.Forbidden:
            log_message(["Cannot post, FORBIDDEN", post.id])
            return "Forbidden"
    log_message(["Comment successful:", post.id])
    return True


# Look at mentions, skip any that have already been processed
def runner():
    log_message(["--------------------------------------", time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.localtime())])
    mentions = r.get_mentions(user)
    for mention in mentions:
        already_done = False
        for row in c.execute("SELECT mention_id FROM mentions"):
            if mention.id == row[0]:
                already_done = True
                break
        if not already_done:
            # Do whatever it is you like to do
            # This will show methods and properties for the mention object
            log_message(vars(mention))

            # THIS IS WHERE YOU CAN DO YOU MENTION REPLYING OR PROCESSING
            # FOR EXAMPLE:
            # YOU CAN POST A REPLY WITH THE FOLLOWING CODE

            # post_reply(mention, "Reply to mention")

            # AFTER YOU POST A REPLY OR PROCESS IT HOWEVER YOU LIKE YOU SHOULD
            # TRACK THAT IT HAS BEEN COMPLETED SO YOU DON'T PROCESS MENTIONS TWICE

            # CODE TO ENTER MENTION INTO DATABASE
            c.execute("INSERT INTO mentions (mention_id) VALUES (?)", (mention.id,))
            conn.commit()


def main():
    while True:
        try:
            runner()
        except praw.errors.OAuthInvalidToken:
            log_message("Token expired, refreshing...")
            oauth_helper.refresh()
        except requests.exceptions.ConnectionError:
            log_message("Connection exception, will retry in 5 minutes")
            time.sleep(240)
        except requests.exceptions.ReadTimeout:
            log_message("Read Timeout exception, will retry in 5 minutes")
            time.sleep(240)
        except Exception as e:
            log_message(["Some unexpected exception:", e])
            log_message("Waiting 5 minutes then trying again")
            time.sleep(240)
        time.sleep(60)


if __name__== '__main__':
    main()
