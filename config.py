from dotenv import dotenv_values
env_values = dotenv_values(".env")

API_URL = "https://oauth.reddit.com"
API_URL_AUTH = "https://www.reddit.com/api/v1/access_token"
REDDIT_APPNAME=env_values["REDDIT_APPNAME"]
REDDIT_APP_ID=env_values["REDDIT_APP_ID"]
REDDIT_APP_SECRET=env_values["REDDIT_APP_SECRET"]
REDDIT_USERNAME=env_values["REDDIT_USERNAME"]
REDDIT_PASSWORD=env_values["REDDIT_PASSWORD"]
USER_AGENT=f'{REDDIT_APPNAME}:1.0 by (/u/{REDDIT_USERNAME})'
