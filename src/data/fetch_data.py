import json
from src.utils.twitter_api import (
    authenticate_oauth, 
    authenticate_bearer_token, 
    fetch_followers_oauth, 
    fetch_user_timeline_oauth, 
    fetch_followers_bearer_token, 
    fetch_user_tweets_bearer_token,
    get_user_id_bearer  # 使用 Bearer Token 認證獲取用戶 ID
)

def main(auth_method='bearer'):  # 使用 bearer 作為默認認證方式
    screen_name = 'bluwhaleai'
    
    if auth_method == 'oauth':
        api = authenticate_oauth()
        # 獲取用戶ID
        user_id = api.get_user(screen_name=screen_name).id_str
        # 抓取粉絲資料
        followers = fetch_followers_oauth(api, screen_name, max_followers=1000)
        with open('data/raw/followers_oauth.json', 'w') as f:
            json.dump([follower._json for follower in followers], f)
        
        # 抓取推文資料
        tweets = fetch_user_timeline_oauth(api, screen_name, max_tweets=1000)
        with open('data/raw/tweets_oauth.json', 'w') as f:
            json.dump(tweets, f)
    elif auth_method == 'bearer':
        client = authenticate_bearer_token()
        # 獲取用戶ID
        user_id = get_user_id_bearer(client, screen_name)
        # 抓取粉絲資料
        followers = fetch_followers_bearer_token(client, user_id, max_results=1000)
        with open('data/raw/followers_bearer.json', 'w') as f:
            json.dump([follower for follower in followers], f)
        
        # 抓取推文資料
        tweets = fetch_user_tweets_bearer_token(client, user_id, max_results=100)
        with open('data/raw/tweets_bearer.json', 'w') as f:
            json.dump([tweet for tweet in tweets], f)
    else:
        print("Invalid authentication method. Use 'oauth' or 'bearer'.")

if __name__ == '__main__':
    # 可以在這裡選擇使用哪種認證方式，'oauth' 或 'bearer'
    main(auth_method='bearer')
