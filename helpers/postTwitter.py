from requests_oauthlib import OAuth1Session
import json
import os
from datetime import datetime

def post_twitter(picks_to_post):

    print("Sending Twitter Post...")

    twitter = OAuth1Session(
        client_key=os.environ['TWITTER_API_KEY'],
        client_secret=os.environ['TWITTER_API_SECRET'],
        resource_owner_key=os.environ['TWITTER_ACCESS_TOKEN'],
        resource_owner_secret=os.environ['TWITTER_ACCESS_SECRET'],
    )

    url = "https://api.x.com/2/tweets"

    current_date = datetime.now().strftime("%-m/%-d")
    top_5_players = picks_to_post.head(5)['playerName'].tolist()
    player_names_str = "\n".join(top_5_players)

    tweet_text = f"Quick Picks for {current_date}:\n\n{player_names_str}"

    print(tweet_text)

    payload = {"text": tweet_text}

    try:

        response = twitter.post(url, json=payload)
        response.raise_for_status()  # Raises an HTTPError for bad responses

        print("Response code: {}".format(response.status_code))
        json_response = response.json()
        print(json.dumps(json_response, indent=4, sort_keys=True))

    except Exception as e:
        print(f"Request failed: {e}")

