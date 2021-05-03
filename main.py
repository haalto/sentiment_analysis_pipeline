import json
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

def enrich_data(price, sentiment):
  time = price['time']['updatedISO']
  current_price = price['bpi']['USD']['rate']

  return {  
            "time": time, 
            "price": current_price, 
            "positive_avg": sentiment['positive_avg'],
            "neutral_avg": sentiment['neutral_avg'] ,
            "negative_avg": sentiment['negative_avg'],
            "compund_avg": sentiment['compound_avg']  
          }  

def get_bitcoin_price():
  response = requests.get("https://api.coindesk.com/v1/bpi/currentprice.json")
  return response.json()

def analyze_sentiment(posts):
  sia = SentimentIntensityAnalyzer()
  scores = list(map(lambda post: sia.polarity_scores(post), posts)) 

  filteredScores = list(filter(lambda score: score['compound'] != 0 and score['pos'] != 0 and score['neg'] != 0 and score['neu'] != 0, scores))
  length = len(filteredScores)

  positive_avg = sum(p['pos'] for p in scores) / length
  neutral_avg = sum(p['neu'] for p in scores) / length
  negative_avg = sum(p['neg'] for p in scores) / length
  compound_avg = sum(p['compound'] for p in scores) / length
  
  return { "positive_avg": positive_avg, "neutral_avg":neutral_avg, "negative_avg":negative_avg, "compound_avg":compound_avg }

def main():
  #Get Bitcoin price
  price = get_bitcoin_price()

  #Get sentiment
  SUBREDDIT = '/r/cryptocurrency/top?limit=100'
  access_token = authenticate()
  data = api_call(access_token, SUBREDDIT)
  posts = (d['data']['selftext'] for d in data['data']['children']) 
  sentiment = analyze_sentiment(posts)

  #Combine data
  transformed_data = enrich_data(price, sentiment)
  print(transformed_data)

if __name__ == '__main__':
  main()