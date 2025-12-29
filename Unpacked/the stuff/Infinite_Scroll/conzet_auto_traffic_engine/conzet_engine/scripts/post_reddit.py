# Requires praw (pip install praw)
import os, praw
from dotenv import load_dotenv
load_dotenv()

client_id=os.getenv("REDDIT_CLIENT_ID")
client_secret=os.getenv("REDDIT_CLIENT_SECRET")
username=os.getenv("REDDIT_USERNAME")
password=os.getenv("REDDIT_PASSWORD")
user_agent=os.getenv("REDDIT_USER_AGENT","conzet-engine-script/0.1")
PAYMENT_URL=os.getenv("PAYMENT_URL")

def post(subreddit_name: str, title: str, body: str):
    reddit = praw.Reddit(client_id=client_id, client_secret=client_secret,
                         username=username, password=password, user_agent=user_agent)
    sub = reddit.subreddit(subreddit_name)
    sub.submit(title=title, selftext=body)

if __name__ == "__main__":
    # Example usage:
    # python3 scripts/post_reddit.py
    print("Fill credentials and call post(subreddit, title, body) with your message containing PAYMENT_URL.")
