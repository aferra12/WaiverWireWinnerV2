import pandas as pd
import requests
import pandas_gbq
import os
import json
from datetime import datetime
from google.oauth2 import service_account

def get_likely_pitchers():

    # Run the query against the BQ Table to get ALL Likely Pitchers Back
    creds_json = os.environ['GCP_SA_KEY']
    creds_dict = json.loads(creds_json)

    credentials = service_account.Credentials.from_service_account_info(creds_dict)

    with open('todays_likely_pitchers.sql', 'r') as f:
        sql_query = f.read()

    sql_pitchers = pandas_gbq.read_gbq(
        sql_query, 
        project_id=os.environ['PROJECT_ID'],
        credentials=credentials
    )

    # sql_pitchers = pd.read_csv('helpers/bquxjob_7c76f273_19865e463d2.csv')

    # Filter likely pitchers by who is available in ESPN

    espn_base_url = f"https://lm-api-reads.fantasy.espn.com/apis/v3/games/flb/seasons/2025/players" # segments/0/leagues/760081598"

    espn_params = {
        #"view": ["freeAgents"]
        "scoringPeriodId": 0,
        "view": ["players_wl", "kona_player_info"]
    }

    # headers = {'X-Fantasy-Filter': '{"filterActive":{"value":true}}'}
    espn_headers = {}
    # player_ids = [3210625]
    # headers["X-Fantasy-Filter"] = f'{{"filterIds":{{"value":{player_ids}}}}}'
    espn_headers['X-Fantasy-Filter'] = f'{{"filterActive":{{"value":true}}}}'

    cookies = {
        "swid": "{DEF635BE-7DB6-462F-86E1-B1945753DC0A}",
        "espn_s2": "AEC4nosSrWs828f6v9iRm13t2qunlcMxFh2HIveh9X4LzvWhWuJsC%2BNifv%2B8k05D2DHEIot6r6R3HZLfWyUbrjqcK9573ZhxM0PntvBa7WtFo9Qq08lL%2B2h4q5AiVqkNt1md7VrE413KHKYmTK6PthUQ8D7cDTVN7qUJ7Sx0MhRCqDQA2u3%2BKMjDwD6GnMN36YIpTQECCFW2yICjcm78YVAd9sJj5s42SgPN7DWraJ6ezfj93840H%2FcnZO%2FDEUBGovg7twE%2FxDm2iFMgf23gwn%2FqRlYOjeTixdcoKo5H00MWQA%3D%3D"
    }
    
    try:
        # Make the API request
        espn_response = requests.get(
            espn_base_url,
            params=espn_params,
            headers=espn_headers,
            cookies=cookies
        )
        espn_response.raise_for_status()
            
        # Extract data from response
        espn_data = espn_response.json()

        espn_player_data = pd.DataFrame([{
            'id': player['id'],
            'name': player['fullName'],
            'position': player['defaultPositionId'],
            'team': player['proTeamId'],
            'ownership_pct': round(player['ownership']['percentOwned'], 2)
        } for player in espn_data])

        low_owned_players = espn_player_data[espn_player_data['ownership_pct'] < 7.5]
        low_owned_pitchers = low_owned_players[low_owned_players['position'].isin([1, 11]) & low_owned_players['team'] != 0]

        merged_df = sql_pitchers.merge(low_owned_pitchers, left_on='playerName', right_on='name')

        # Select and rename relevant columns
        likely_pitchers_df = merged_df[['playerId', 'playerName', 'gamesRest', 'avgFantasyPts', 'boomFantasyPoints']]
        
        # Sort by fantasy potential (higher boom points first) and lower ownership
        likely_pitchers_df = likely_pitchers_df.sort_values(by='boomFantasyPoints', ascending=False)
        
        # NEED TO JOIN TO THE ACTIVE 26 MAN ROSTER

        mlb_team_ids = pd.read_csv("helpers/mlb_team_ids.csv")

        active_players = []

        for _, team in mlb_team_ids.iterrows():
            team_id = team['id']

            player_response = requests.get(f"https://statsapi.mlb.com/api/v1/teams/{team_id}/roster")
            roster_data = player_response.json()

            roster = roster_data.get("roster", [])
            
            # Extract just id and player_name
            for player in roster:
                person = player.get("person", {})
                active_players.append({
                    "id": person.get("id"),
                    "team_id": team_id
                })
        
        active_players_df = pd.DataFrame(active_players)

        active_likely_pitchers = likely_pitchers_df.merge(active_players_df, left_on='playerId', right_on='id')

        # FILTER FOR ONLY CURRENT DAYS GAMES

        todays_schedule_url = "https://statsapi.mlb.com/api/v1/schedule"
        schedule_params = {
            "sportId": 1,  # MLB
            "date": datetime.now().strftime("%Y-%m-%d")  # Today's date
        }

        schedule_response = requests.get(todays_schedule_url, params=schedule_params)

        schedule_data = schedule_response.json()
        dates = schedule_data.get("dates", [])
        
        if not dates:
            print("No games scheduled for today")
            return pd.DataFrame()
        
        todays_games = dates[0].get("games", [])
        
        teams_playing = []
        for game in todays_games:
            # Away team
            away_team = game.get("teams", {}).get("away", {}).get("team", {})
            teams_playing.append({
                "team_id": away_team.get("id")
            })
            
            # Home team
            home_team = game.get("teams", {}).get("home", {}).get("team", {})
            teams_playing.append({
                "team_id": home_team.get("id")
            })
        
        playing_today = pd.DataFrame(teams_playing)

        final_pitcher_picks = active_likely_pitchers.merge(playing_today, left_on='team_id', right_on='team_id')

        # Here are the final picks!

        return final_pitcher_picks

    except Exception as e:
        print("Error pulling from ESPN API")