import requests
from pprint import pprint
from datetime import datetime
import json

def test_game_rosters():
    # Test with a random 2023 regular season game
    game_pk = 718780
    
    # Get game data with roster hydration
    url = f"https://statsapi.mlb.com/api/v1/game/{game_pk}/boxscore"
    
    response = requests.get(url)
    data = response.json()

    with open("box.json", 'w') as file:
        json.dump(data, file, indent=4)
    
    # Track pitcher data
    pitcher_data = []
    
    # Process both teams
    for side in ["home", "away"]:
        team_boxscore = data["teams"][side]
        team_id = team_boxscore["team"]["id"]
        
        # Get all players and filter pitchers
        players = team_boxscore["players"]
        
        for player_key, player_info in players.items():
            # Check if player is a pitcher
            if player_info["position"]["code"] == "1":  # Pitcher position code
                player_id = player_info["person"]["id"]
                
                # Check if player pitched in this game
                stats = player_info.get("stats", {}).get("pitching", {})
                
                pitcher_data.append({
                    "team_id": team_id,
                    "player_id": player_id,
                    "player_name": player_info["person"]["fullName"],
                    "on_active_roster": True,
                    "pitched_in_game": bool(stats),
                    "strikeouts": stats.get("strikeOuts", 0) if stats else 0
                })
    
    print("\nAll Pitchers on Active Roster:")
    #pprint(pitcher_data)
    
    # Print some summary stats
    total_pitchers = len(pitcher_data)
    pitched_count = sum(1 for p in pitcher_data if p["pitched_in_game"])
    print(f"\nTotal pitchers on roster: {total_pitchers}")
    print(f"Pitchers who appeared in game: {pitched_count}")

if __name__ == "__main__":
    test_game_rosters()