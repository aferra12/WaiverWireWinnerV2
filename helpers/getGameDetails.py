# MAKE SURE TO IMPLEMENT A RETURN FUNCTION

import requests
import pandas as pd
from datetime import datetime
import pytz

def get_game_details(game_pks):
    """
    Retrieve detailed information about MLB games given their game PKs.
    
    Parameters:
    -----------
    game_pks : list
        List of game PKs (integers)
        
    Returns:
    --------
    pandas.DataFrame
        DataFrame containing detailed information about each game
    """
    game_details = []
    
    for game_pk in game_pks:
        try:
            # MLB Stats API endpoint for game details
            url = f"https://statsapi.mlb.com/api/v1.1/game/{game_pk}/feed/live"
            
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            
            # Extract game data
            game_data = data.get('gameData', {})
            # live_data = data.get('liveData', {})
            
            # Get teams info
            teams = game_data.get('teams', {})
            home_team = teams.get('home', {})
            away_team = teams.get('away', {})
            
            # Get venue info
            # venue = game_data.get('venue', {})
            
            # Get datetime info
            datetime_info = game_data.get('datetime', {})
            
            # Get weather info
            # weather = game_data.get('weather', {})
            
            # Get field info
            # field_info = venue.get('fieldInfo', {})
            
            # Get umpire info
            # umpires = live_data.get('boxscore', {}).get('officials', [])
            # for ump in umpires:
            #     if ump.get('officialType') == 'Home Plate':
            #         hp_umpire = ump.get('official', {}).get('fullName')
            
            # Compile game details
            game_detail = {
                'gamePk': game_pk,
                'homeTeam': home_team.get('name'),
                # 'homeTeamId': home_team.get('id'),
                'awayTeam': away_team.get('name'),
                # 'awayTeamId': away_team.get('id'),
                # 'venue': venue.get('name'),
                # 'venueId': venue.get('id'),
                'gameDate': datetime_info.get('originalDate'),
                #'gameTime': datetime.strptime(f"{datetime_info.get('time')} {datetime_info.get('ampm')}", "%I:%M %p").strftime("%H:%M"),
                'dayNight': datetime_info.get('dayNight'),
                
                # Weather information
                # 'temperature': weather.get('temp'),
                # 'windSpeed': weather.get('wind'),
                # 'windDirection': weather.get('windDirection'),
                # 'condition': weather.get('condition'),
                # 'precipitation': weather.get('precipitation'),
                # 'humidity': weather.get('humidity'),
                # 'pressure': weather.get('pressure'),
                # 'visibility': weather.get('visibility'),
                
                # Field information
                # 'fieldType': field_info.get('type'),
                # 'roofType': venue.get('roofType'),
                # 'leftField': field_info.get('leftLine'),
                # 'leftCenterField': field_info.get('leftCenter'),
                # 'centerField': field_info.get('center'),
                # 'rightCenterField': field_info.get('rightCenter'),
                # 'rightField': field_info.get('rightLine'),
                
                # Umpire information
                # 'homePlateUmpire': hp_umpire,
                
                'gameDuration': game_data.get('gameInfo', {}).get('gameDurationMinutes'),
            }
            
            game_details.append(game_detail)
            print(f"Retrieved details for game {game_pk}")
            
        except requests.exceptions.RequestException as e:
            print(f"Error retrieving data for game {game_pk}: {e}")
    
    # Create DataFrame from collected data
    if game_details:
        return pd.DataFrame(game_details)
    else:
        return pd.DataFrame()

# Example usage
if __name__ == "__main__":
    # Example list of game PKs
    #game_pks = [718780]  # Replace with actual game PKs
    game_pks = [777712, 777720, 777715, 777716, 777721, 777718, 777717, 777719, 777709, 777711, 777714, 777710, 777707, 777713, 777708]
    
    # Get game details
    details_df = get_game_details(game_pks)
    
    # Display the DataFrame
    if not details_df.empty:
        print("\nGame Details:")
        # Display a subset of columns for readability
        display_columns = [
            'gamePk', 'homeTeam', 'awayTeam', 'gameDate', 
            'dayNight', 'gameDuration'
        ]
        print(details_df[display_columns])
        
        # Save to CSV (optional)
        details_df.to_csv("mlb_game_details.csv", index=False)
        print("Game details saved to mlb_game_details.csv")
    else:
        print("No game details retrieved.")