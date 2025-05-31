# import requests
# import json

# league_id = 760081598
# year = 2025
# url = "https://lm-api-reads.fantasy.espn.com/apis/v3/games/flb/seasons/2025/segments/0/leagues/760081598"# + \
#       #str(league_id) + "?seasonId=" + str(year)

# r = requests.get(url,
#                  cookies={"swid": "{DEF635BE-7DB6-462F-86E1-B1945753DC0A}",
#                           "espn_s2": "AECruZRCXn0BHlCv%2BynVzxJbda4zDpJrXCBeezjIqOWuh21G%2F0p7xB%2BDKjMiyCR7pPjlyXyJfir%2FpoHZmwao%2Bksyh%2FBdJ0oPelLZDl%2BP8CJcF7evYbcW3A0KIdsJaTfh1YZWv%2FfzuC1PTXw3b8pMFpRaXgm8z0uh0GWqOSlnPewLcoOEHYL9R2swj64sOJrX3a9e4YwsvyH93OnFyMpPX8FKVS3Yb%2Brfelo2s2qZG855rZkAzPc9tyVMnURUoJH%2FTFG8sTs%2Bd9D8cuHfcUbWyD0VTYP39LNOH3%2BLBxTBLsi7mw%3D%3D"})

# print(json.dumps(r.json(), indent=4))


# import requests
# import json
# from typing import Optional, Dict, Any
# from datetime import datetime

# def get_player_gamelogs(
#     player_id: str,
#     season: Optional[int] = None,
#     date_range: Optional[tuple[datetime, datetime]] = None
# ) -> Dict[Any, Any]:
#     """
#     Get game logs for a specific MLB player.
    
#     Args:
#         player_id (str): The MLB player ID
#         season (int, optional): Season year to get game logs for. Defaults to current season.
#         date_range (tuple[datetime, datetime], optional): Start and end dates to filter game logs
        
#     Returns:
#         Dict[Any, Any]: JSON response containing player game logs
        
#     Example:
#         >>> get_player_gamelogs("592450", 2023)  # Aaron Judge's 2023 game logs
#     """
#     # Base URL for MLB Stats API
#     base_url = "https://statsapi.mlb.com/api/v1"
    
#     # Construct the URL
#     url = f"{base_url}/people/{player_id}"
    
#     # Build hydration parameter for game logs
#     hydration = "stats(group=[hitting,pitching],type=gameLog"
    
#     # Add season parameter if provided
#     if season:
#         hydration += f",season={season}"
    
#     # Add date range if provided
#     if date_range:
#         start_date = date_range[0].strftime("%Y-%m-%d")
#         end_date = date_range[1].strftime("%Y-%m-%d")
#         hydration += f",startDate={start_date},endDate={end_date}"
    
#     hydration += ")"
    
#     # Parameters for the API request
#     params = {
#         "hydrate": hydration
#     }
    
#     try:
#         response = requests.get(url, params=params)
#         response.raise_for_status()  # Raise exception for bad status codes
#         return json.dumps(response.json(), indent=4)
        
#     except requests.exceptions.RequestException as e:
#         raise Exception(f"Error fetching game logs: {str(e)}")

# print(get_player_gamelogs("592450", 2023))


import requests
import json

league_id = 760081598
year = 2025
#fantasy.espn.com/apis/v3/games/ffl/leagueHistory/:league_id?seasonId=:season
url = "https://lm-api-reads.fantasy.espn.com/apis/v3/games/flb/seasons/2024/segments/0/leagues/760081598"# + \
      #str(league_id) + "?seasonId=" + str(year)

r = requests.get(url,
                 cookies={"swid": "{DEF635BE-7DB6-462F-86E1-B1945753DC0A}",
                          "espn_s2": "AECruZRCXn0BHlCv%2BynVzxJbda4zDpJrXCBeezjIqOWuh21G%2F0p7xB%2BDKjMiyCR7pPjlyXyJfir%2FpoHZmwao%2Bksyh%2FBdJ0oPelLZDl%2BP8CJcF7evYbcW3A0KIdsJaTfh1YZWv%2FfzuC1PTXw3b8pMFpRaXgm8z0uh0GWqOSlnPewLcoOEHYL9R2swj64sOJrX3a9e4YwsvyH93OnFyMpPX8FKVS3Yb%2Brfelo2s2qZG855rZkAzPc9tyVMnURUoJH%2FTFG8sTs%2Bd9D8cuHfcUbWyD0VTYP39LNOH3%2BLBxTBLsi7mw%3D%3D"})

print(json.dumps(r.json(), indent=4))