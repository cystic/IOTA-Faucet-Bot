#!/usr/bin/python
import praw
import pdb
import re
import os
import time
import sys

if len(sys.argv) > 1:
    timestamp = sys.argv[1]
else:
    timestamp = time.time()

# Create the Reddit instance
reddit = praw.Reddit('bot1')

# and login
#reddit.login(REDDIT_USERNAME, REDDIT_PASS)

# Have we run this code before? If not, create an empty list
if not os.path.isfile("posts_replied_to.txt"):
    posts_replied_to = []

# If we have run the code before, load the list of posts we have replied to
else:
    # Read the file into a list and remove any empty values
    with open("posts_replied_to.txt", "r") as f:
        posts_replied_to = f.read()
        posts_replied_to = posts_replied_to.split("\n")
        posts_replied_to = list(filter(None, posts_replied_to))

# Get the top stream of values from our subreddit
subreddit = reddit.subreddit('iotafaucet')
for submission in subreddit.stream.submissions():
    #print(submission.title)

    # If we haven't replied to this post before
    if submission.id not in posts_replied_to and submission.created_utc > timestamp:

        # Do a case insensitive search
        if re.search("iota", submission.title, re.IGNORECASE):
            # Reply to the post
            submission.reply("Welcome to IOTA. +200 IOTA")
            print("Bot replying to : ", submission.title)

            # Append the current id into our list
            posts_replied_to.append(submission.id)
            with open("posts_replied_to.txt", "a") as f:
                f.write('\n' + submission.id)
            # rate limit is 30 requests per minute, so just to stay on the safe side, we limit to 60/3 = 20 requests
            time.sleep(3)
