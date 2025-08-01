from requests_oauthlib import OAuth1Session
import json
import os

def post_twitter():

    print("Testing Twitter Posts")

    twitter = OAuth1Session(
        client_key=os.environ['TWITTER_API_KEY'],
        client_secret=os.environ['TWITTER_API_SECRET'],
        resource_owner_key=os.environ['TWITTER_ACCESS_TOKEN'],
        resource_owner_secret=os.environ['TWITTER_ACCESS_SECRET'],
    )

    url = "https://api.x.com/2/tweets"

    payload = json.dumps({
    "text": "I love Tyler Alexander (test 2)"
    })

    try:

        response = twitter.post(url, json=payload)
        response.raise_for_status()  # Raises an HTTPError for bad responses

        print("Response code: {}".format(response.status_code))
        json_response = response.json()
        print(json.dumps(json_response, indent=4, sort_keys=True))

    except Exception as e:
        print(f"Request failed: {e}")

