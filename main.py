import requests
from requests.auth import HTTPBasicAuth
import nltk
nltk.download('vader_lexicon')
from nltk.sentiment import SentimentIntensityAnalyzer
import config

def authenticate():
  data = {
    "grant_type": "password", 
    "username": config.REDDIT_USERNAME, 
    "password": config.REDDIT_PASSWORD
  }
  auth = HTTPBasicAuth(config.REDDIT_APP_ID, config.REDDIT_APP_SECRET)
  headers = {"User-Agent": config.USER_AGENT}

  response = requests.post(config.API_URL_AUTH,
                  auth=auth,
                  data=data,
                  headers=headers          
              )

  response_data = response.json()
  return response_data["access_token"]

def api_call(token, resource=''):
  bearer = f'bearer {token}'
  headers = {'Authorization': bearer, 'User-Agent': config.USER_AGENT}
  response = requests.get(f'{config.API_URL}{resource}', headers=headers)
  return response.json()

def analyze_sentiment(posts):
  sia = SentimentIntensityAnalyzer()
  scores = list(map(lambda post: sia.polarity_scores(post['data']['selftext']), posts))

  print(scores)

  positive_sum = sum(p['pos'] for p in scores)
  neutral_sum = sum(p['neu'] for p in scores)
  negative_sum = sum(p['neg'] for p in scores)
  
  print(f'positive sum: {positive_sum}')
  print(f'neutral sum: {neutral_sum}')
  print(f'negative sum: {negative_sum}')

def main():
  access_token = authenticate()
  data = api_call(access_token, '/r/bitcoin/top?limit=100')
  posts = data['data']['children']
  analyze_sentiment(posts)

if __name__ == '__main__':
  main()