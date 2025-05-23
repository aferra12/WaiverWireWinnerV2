import requests
import pandas as pd

def get_pitcher_game_logs(game_pks):
    """
    Extract pitcher game logs from MLB Stats API for specified games.
    
    Args:
        game_pks (list): List of MLB game IDs to retrieve data for
        
    Returns:
        pandas.DataFrame: DataFrame containing pitcher statistics
    """
    # Track pitcher data
    pitcher_data = []
    
    for game_pk in game_pks:
        try:
            # MLB Stats API endpoint for game details with boxscore
            url = f"https://statsapi.mlb.com/api/v1/game/{game_pk}/boxscore"
    
            response = requests.get(url)
            data = response.json()
            
            # Process both home and away teams
            for team_type in ['home', 'away']:
                team_name = data['teams'][team_type]['team']['name']
                team_id = data['teams'][team_type]['team']['id']
                
                # Process each player on the team
                for player_id, player_info in data['teams'][team_type]['players'].items():
                    # Check if player is a pitcher (position code "1")
                    if "position" in player_info and player_info["position"]["code"] == "1":
                        # Initialize player record with basic info

                        quit()
                        # SET BASE RECORD WITH GAME DETAILS #
                        # SHOULD I DO BATTERS HERE TOO WITH IS_PITCHER FLAG? PROBABLY #

                        player_record = {
                            'game_pk': game_pk,
                            'player_id': player_id.replace('ID', ''),
                            'player_name': player_info['person']['fullName'],
                            'team': team_name,
                            'team_id': team_id,
                            'did_pitch': False  # Default value
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
    pitcher_df = get_pitcher_game_logs(game_pks)
    
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