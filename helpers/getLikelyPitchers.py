import pandas as pd
import requests
import pandas_gbq
import os
import json
from google.oauth2 import service_account

def get_likely_pitchers():

    # Run the query against the BQ Table to get ALL Likely Pitchers Back
    # creds_json = os.environ['GCP_SA_KEY']
    # creds_dict = json.loads(creds_json)

    # credentials = service_account.Credentials.from_service_account_info(creds_dict)

    # with open('todays_likely_pitchers.sql', 'r') as f:
    #     sql_query = f.read()

    # sql_pitchers = pandas_gbq.read_gbq(
    #     sql_query, 
    #     project_id=os.environ['PROJECT_ID'],
    #     credentials=credentials
    # )

    sql_pitchers = pd.read_csv('bquxjob_521f526a_19865cc6f59.csv')


    # Filter likely pitchers by who is available in ESPN

    base_url = f"https://lm-api-reads.fantasy.espn.com/apis/v3/games/flb/seasons/2025/players" # segments/0/leagues/760081598"

    params = {
        #"view": ["freeAgents"]
        "scoringPeriodId": 0,
        "view": ["players_wl", "kona_player_info"]
    }

    # headers = {'X-Fantasy-Filter': '{"filterActive":{"value":true}}'}
    headers = {}
    # player_ids = [3210625]
    # headers["X-Fantasy-Filter"] = f'{{"filterIds":{{"value":{player_ids}}}}}'
    headers['X-Fantasy-Filter'] = f'{{"filterActive":{{"value":true}}}}'


    cookies = {
        "swid": "{DEF635BE-7DB6-462F-86E1-B1945753DC0A}",
        "espn_s2": "AEC4nosSrWs828f6v9iRm13t2qunlcMxFh2HIveh9X4LzvWhWuJsC%2BNifv%2B8k05D2DHEIot6r6R3HZLfWyUbrjqcK9573ZhxM0PntvBa7WtFo9Qq08lL%2B2h4q5AiVqkNt1md7VrE413KHKYmTK6PthUQ8D7cDTVN7qUJ7Sx0MhRCqDQA2u3%2BKMjDwD6GnMN36YIpTQECCFW2yICjcm78YVAd9sJj5s42SgPN7DWraJ6ezfj93840H%2FcnZO%2FDEUBGovg7twE%2FxDm2iFMgf23gwn%2FqRlYOjeTixdcoKo5H00MWQA%3D%3D"
    }
    
    try:
        # Make the API request
        response = requests.get(
            base_url,
            params=params,
            headers=headers,
            cookies=cookies
        )
        response.raise_for_status()
            
        # Extract data from response
        data = response.json()

        espn_player_data = pd.DataFrame([{
            'id': player['id'],
            'name': player['fullName'],
            'position': player['defaultPositionId'],
            'team': player['proTeamId'],
            'ownership_pct': round(player['ownership']['percentOwned'], 2)
        } for player in data])

        low_owned_players = espn_player_data[espn_player_data['ownership_pct'] < 5]
        low_owned_pitchers = low_owned_players[low_owned_players['position'].isin([1, 11]) & low_owned_players['team'] != 0]

        merged_df = sql_pitchers.merge(low_owned_pitchers, left_on='playerName', right_on='name')

        print(merged_df)

    except Exception as e:
        print("Error pulling from ESPN API")

if __name__ == "__main__":
    get_likely_pitchers()