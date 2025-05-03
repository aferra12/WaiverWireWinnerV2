import requests
import pandas as pd
import json

from getGameDetails import get_game_details

def get_player_game_logs(game_pks):
    """
    Extract player game logs from MLB Stats API for specified games.
    
    Args:
        game_pks (list): List of MLB game IDs to retrieve data for
        
    Returns:
        pandas.DataFrame: DataFrame containing player statistics
    """

    # Grab all of the game details first, will be joined to the player logs later
    try:
        game_details = get_game_details(game_pks)
    except requests.exceptions.RequestException as e:
        print(f"Error retrieving data for game {game_pk}: {e}")

    # Track player game logs
    player_data = []
    
    for game_pk in game_pks:

        try:
            # MLB Stats API endpoint for game details with boxscore
            url = f"https://statsapi.mlb.com/api/v1/game/{game_pk}/boxscore"
    
            response = requests.get(url)
            data = response.json()
            
            # Process both home and away teams
            for team_type in ['home', 'away']:
                team_name = data['teams'][team_type]['team']['name']
                # team_id = data['teams'][team_type]['team']['id']
                
                # Process each player on the team
                for player_id, player_info in data['teams'][team_type]['players'].items():

                    with open(f'player_info_{player_id}.json', 'w', encoding='utf-8') as f:
                        json.dump(player_info, f, ensure_ascii=False, indent=4)

                    # I've decided that I'm just going to make one massive table for both pitchers, hitters, and game data #
                    # SHOULD I DO BATTERS HERE TOO WITH IS_PITCHER FLAG? PROBABLY #

                    # Check if player is a pitcher (position code "1")
                    if "position" in player_info and player_info["position"]["code"] == "1":
                        
                        ### STOPPED HERE LAST TIME. NEED TO ADD IN FiELDS TO PULL ###
                        # Initialize player record with basic info
                        player_record = {
                            'game_pk': game_pk,
                            'player_id': player_id.replace('ID', ''),
                            'player_name': player_info['person']['fullName'],
                            'team_name': team_name,
                            'is_home': True if team_type == 'home' else False,
                            'did_start': None,
                            'did_pitch': None,  # Default value
                            'num_pitches': None,
                            'num_strikes': None,
                            # IMPLEMENT ~API~ Calls to Statcast to Grab these and parse out of CSV
                            # Run Value: https://baseballsavant.mlb.com/leaderboard/swing-take?year=2025&team=&leverage=Neutral&group=Pitcher&type=All&sub_type=null&min=10&csv=True
                            # xwOBA: https://baseballsavant.mlb.com/leaderboard/expected_statistics?type=pitcher&year=2025&position=&team=&filterType=bip&min=1
                            # res = requests.get(url, timeout=None).content
                            # data = pd.read_csv(io.StringIO(res.decode('utf-8')))
                            # data = sanitize_statcast_columns(data)
                            'run_value': None,
                            'xwOBA': None
                        }

                        # Check if player has pitching stats for this game
                        if 'stats' in player_info and 'pitching' in player_info['stats'] and player_info['stats']['pitching']:
                            player_record['did_pitch'] = True
                            
                            # Extract game pitching stats
                            pitching_stats = player_info['stats']['pitching']
                            
                            # Add relevant pitching stats to player record
                            pitching_fields = [
                                'inningsPitched', 'hits', 'runs', 'earnedRuns', 'baseOnBalls', 
                                'strikeOuts', 'homeRuns', 'pitchesThrown', 'strikes', 'balls',
                                'era', 'battersFaced', 'outs', 'gamesPitched', 'gamesStarted',
                                'completeGames', 'shutouts', 'holds', 'saves', 'blownSaves',
                                'inheritedRunners', 'inheritedRunnersScored', 'wildPitches',
                                'hitBatsmen', 'balks', 'wins', 'losses', 'note'
                            ]
                            
                            for stat in pitching_fields:
                                player_record[stat] = pitching_stats.get(stat, None)
                        
                        # Add player record to dataset
                        pitcher_data.append(player_record)
                    else:
                        print("hi")
            
        except requests.exceptions.RequestException as e:
            print(f"Error retrieving data for game {game_pk}: {e}")
    
    # Convert to DataFrame
    df = pd.DataFrame(pitcher_data)
    
    # Convert numeric columns from strings to appropriate types
    numeric_columns = [
        'earnedRuns', 'runs', 'hits', 'strikeOuts', 'baseOnBalls', 'homeRuns',
        'pitchesThrown', 'strikes', 'balls', 'battersFaced', 'outs', 'wildPitches',
        'hitBatsmen', 'balks', 'inheritedRunners', 'inheritedRunnersScored',
        'wins', 'losses', 'saves', 'holds', 'blownSaves'
    ]
    
    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    return df

if __name__ == "__main__":
    # Test with a sample game
    game_pks = [718780]
    pitcher_df = get_player_game_logs(game_pks)
    
    # Display the results
    print(f"Found {len(pitcher_df)} pitcher records")
    print(f"Pitchers who pitched: {pitcher_df['did_pitch'].sum()}")
    
    # Show pitchers who actually pitched in this game
    print("\nPitchers who pitched in this game:")
    if 'inningsPitched' in pitcher_df.columns:
        print(pitcher_df[pitcher_df['did_pitch']][['player_name', 'team', 'inningsPitched', 'earnedRuns', 'strikeOuts', 'baseOnBalls']])
    else:
        print(pitcher_df[pitcher_df['did_pitch']][['player_name', 'team']])
    
    # Save to CSV for further analysis
    pitcher_df.to_csv(f"pitcher_game_logs_{game_pks[0]}.csv", index=False)