# MAKE SURE TO IMPLEMENT A RETURN FUNCTION

import requests
from datetime import datetime, timedelta

def get_games(start_date, end_date):
    """
    Retrieve MLB game PKs for a given date range.
    
    Parameters:
    -----------
    start_date : str
        Start date in 'YYYY-MM-DD' format
    end_date : str
        End date in 'YYYY-MM-DD' format
        
    Returns:
    --------
    list
        List containing game PKs
    """
    # Convert string dates to datetime objects
    start_dt = datetime.strptime(start_date, '%Y-%m-%d')
    end_dt = datetime.strptime(end_date, '%Y-%m-%d')
    
    # Initialize empty list to store game PKs
    game_pks = []
    
    # Iterate through each date in the range
    current_dt = start_dt
    while current_dt <= end_dt:
        # Format date for API request
        date_str = current_dt.strftime('%Y-%m-%d')
        
        # MLB Stats API endpoint for schedule
        # Add gameType=R parameter to only get regular season games
        url = f"https://statsapi.mlb.com/api/v1/schedule?sportId=1&date={date_str}&gameType=R"
        
        try:
            # Make API request
            response = requests.get(url)
            response.raise_for_status()  # Raise exception for HTTP errors
            data = response.json()
            
            # Extract game PKs from the response
            if 'dates' in data and len(data['dates']) > 0:
                for date_data in data['dates']:
                    if 'games' in date_data:
                        for game in date_data['games']:
                            if 'gamePk' in game and game.get('status', {}).get('detailedState') == 'Final':
                                game_pks.append(game['gamePk'])
            
        except requests.exceptions.RequestException as e:
            print(f"Error retrieving data for {date_str}: {e}")
        
        # Move to next day
        current_dt += timedelta(days=1)
    
    return game_pks

# Example usage
# if __name__ == "__main__":
#     # Example date range (2023 regular season opening week)
#     start_date = "2025-03-22"
#     end_date = "2025-03-27"
    
#     game_pks = get_games(start_date, end_date)
    
#     # Display the list of game PKs
#     print(f"\nRetrieved {len(game_pks)} games between {start_date} and {end_date}")
#     print(game_pks)
    
    # Save to text file (optional)
    # with open(f"mlb_game_pks_{start_date}_to_{end_date}.txt", "w") as f:
    #     for pk in game_pks:
    #         f.write(f"{pk}\n")
    # print(f"Game PKs saved to mlb_game_pks_{start_date}_to_{end_date}.txt")