# quick_test.py (project root)
import os
from dotenv import load_dotenv, find_dotenv
import praw

load_dotenv(find_dotenv(usecwd=True), override=True)

print("ENV loaded:",
      bool(os.getenv("REDDIT_CLIENT_ID")),
      bool(os.getenv("REDDIT_CLIENT_SECRET")),
      bool(os.getenv("REDDIT_USERNAME")),
      bool(os.getenv("REDDIT_PASSWORD")),
      os.getenv("REDDIT_USER_AGENT"))

reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent=os.getenv("REDDIT_USER_AGENT"),
    username=os.getenv("REDDIT_USERNAME"),
    password=os.getenv("REDDIT_PASSWORD"),
)

# This call needs 'identity' scope; if creds are wrong, it 401s here.
print("Scopes:", reddit.auth.scopes())
print("Authenticated as:", reddit.user.me())
