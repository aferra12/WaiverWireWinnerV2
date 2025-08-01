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


# import requests
# import json

# league_id = 760081598
# year = 2025
# #fantasy.espn.com/apis/v3/games/ffl/leagueHistory/:league_id?seasonId=:season
# url = "https://lm-api-reads.fantasy.espn.com/apis/v3/games/flb/seasons/2024/segments/0/leagues/760081598"# + \
#       #str(league_id) + "?seasonId=" + str(year)

# r = requests.get(url,
#                  cookies={"swid": "{DEF635BE-7DB6-462F-86E1-B1945753DC0A}",
#                           "espn_s2": "AECruZRCXn0BHlCv%2BynVzxJbda4zDpJrXCBeezjIqOWuh21G%2F0p7xB%2BDKjMiyCR7pPjlyXyJfir%2FpoHZmwao%2Bksyh%2FBdJ0oPelLZDl%2BP8CJcF7evYbcW3A0KIdsJaTfh1YZWv%2FfzuC1PTXw3b8pMFpRaXgm8z0uh0GWqOSlnPewLcoOEHYL9R2swj64sOJrX3a9e4YwsvyH93OnFyMpPX8FKVS3Yb%2Brfelo2s2qZG855rZkAzPc9tyVMnURUoJH%2FTFG8sTs%2Bd9D8cuHfcUbWyD0VTYP39LNOH3%2BLBxTBLsi7mw%3D%3D"})

# print(json.dumps(r.json(), indent=4))

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, roc_auc_score
import warnings
warnings.filterwarnings('ignore')

# Read the CSV file
data = {
    'gameDate': [
        '2025-07-11T00:00:00', '2025-07-12T00:00:00', '2025-07-13T00:00:00', 
        '2025-07-18T00:00:00', '2025-07-19T00:00:00', '2025-07-20T00:00:00',
        '2025-07-21T00:00:00', '2025-07-22T00:00:00', '2025-07-23T00:00:00',
        '2025-07-25T00:00:00', '2025-07-26T00:00:00', '2025-07-27T00:00:00', '2025-08-01T00:00:00', '2025-08-06T00:00:00', '2025-08-10T00:00:00', '2025-08-14T00:00:00'
    ],
    'playerName': [
        'Abner Uribe', 'Abner Uribe', 'Abner Uribe', 'Abner Uribe', 'Abner Uribe',
        'Abner Uribe', 'Abner Uribe', 'Abner Uribe', 'Abner Uribe', 'Abner Uribe',
        'Abner Uribe', 'Abner Uribe', 'Abner Uribe', 'Abner Uribe', 'Abner Uribe', 'Abner Uribe'
    ],
    'didPlay': [
        False, True, False, True, False, True, False, True, False, False, False, True, False, False, False, False
    ],
    'hilltopperPts': [
        None, -7, None, 9, None, 14, None, 2, None, None, None, 2, None, None, None, None
    ],
    'daysRest': [
        0, 1, 0, 5, 0, 1, 0, 1, 0, 2, 3, 4, 4, 4, 3, 3
    ]
}

df = pd.DataFrame(data)

# Convert daysRest to Int64 (nullable integer type)
df['daysRest'] = df['daysRest'].astype('Int64')

print("Raw Data Summary:")
print("=" * 50)
print(f"Total observations with rest data: {len(df)}")
print(f"Games played: {df['didPlay'].sum()}")
print(f"Games not played: {(~df['didPlay']).sum()}")

# Basic probability by days of rest (for comparison)
basic_probs = df.groupby('daysRest').agg({
    'didPlay': ['count', 'sum', 'mean']
}).round(4)
basic_probs.columns = ['opportunities', 'games_played', 'probability']

print("\nBasic Probability by Rest Days:")
print("=" * 50)
print(basic_probs)

# Advanced modeling with polynomial features to capture the curve
def create_pitcher_model(df, max_degree=4):
    """
    Create a logistic regression model with polynomial features
    to capture the non-linear relationship between rest days and playing probability
    """
    X = df[['daysRest']]
    y = df['didPlay']
    
    # Try different polynomial degrees to find the best fit
    best_model = None
    best_score = -1
    best_degree = 1
    
    for degree in range(1, max_degree + 1):
        # Create polynomial features
        poly_pipeline = Pipeline([
            ('poly', PolynomialFeatures(degree=degree, include_bias=False)),
            ('logistic', LogisticRegression(max_iter=1000))
        ])
        
        try:
            poly_pipeline.fit(X, y)
            
            # Calculate AUC score if we have both classes
            if len(np.unique(y)) > 1:
                y_pred_proba = poly_pipeline.predict_proba(X)[:, 1]
                score = roc_auc_score(y, y_pred_proba)
            else:
                score = poly_pipeline.score(X, y)
            
            if score > best_score:
                best_score = score
                best_model = poly_pipeline
                best_degree = degree
                
        except Exception as e:
            print(f"Warning: Could not fit degree {degree} model: {e}")
            continue
    
    return best_model, best_degree, best_score

# Create the model
model, best_degree, score = create_pitcher_model(df)

print(f"\nBest Model: Polynomial degree {best_degree}")
print(f"Model Score: {score:.4f}")

# Generate predictions for a range of rest days
rest_range = np.arange(0, 15).reshape(-1, 1)
predicted_probs = model.predict_proba(rest_range)[:, 1]

print("\nModel Predictions:")
print("=" * 50)
print("Rest Days | Predicted Probability | Interpretation")
print("-" * 50)

for i, prob in enumerate(predicted_probs):
    if prob < 0.1:
        interpretation = "Very Unlikely"
    elif prob < 0.3:
        interpretation = "Unlikely"
    elif prob < 0.7:
        interpretation = "Moderate"
    elif prob < 0.9:
        interpretation = "Likely"
    else:
        interpretation = "Very Likely"
    
    print(f"{i:8d} | {prob:18.1%} | {interpretation}")

# Advanced analysis: Find the optimal rest days
optimal_rest_day = np.argmax(predicted_probs)
max_probability = predicted_probs[optimal_rest_day]

print(f"\nOptimal Rest Pattern:")
print("=" * 50)
print(f"Peak probability occurs at {optimal_rest_day} days rest: {max_probability:.1%}")

# Find the "sweet spot" range (within 90% of peak probability)
sweet_spot_threshold = max_probability * 0.9
sweet_spot_days = np.where(predicted_probs >= sweet_spot_threshold)[0]

if len(sweet_spot_days) > 0:
    print(f"Sweet spot range: {sweet_spot_days[0]} to {sweet_spot_days[-1]} days rest")

# Compare actual vs predicted for available data
print("\nActual vs Predicted (for available data):")
print("=" * 50)
for rest_days in sorted(df['daysRest'].unique()):
    actual_data = df[df['daysRest'] == rest_days]
    actual_prob = actual_data['didPlay'].mean()
    predicted_prob = model.predict_proba([[rest_days]])[0, 1]
    
    print(f"Rest Days: {int(rest_days):2d} | "
          f"Actual: {actual_prob:.1%} | "
          f"Predicted: {predicted_prob:.1%} | "
          f"Difference: {abs(actual_prob - predicted_prob):.1%}")

# Feature importance (for polynomial features)
if hasattr(model.named_steps['logistic'], 'coef_'):
    coefficients = model.named_steps['logistic'].coef_[0]
    feature_names = model.named_steps['poly'].get_feature_names_out(['daysRest'])
    
    print(f"\nModel Coefficients (Polynomial Degree {best_degree}):")
    print("=" * 50)
    for name, coef in zip(feature_names, coefficients):
        print(f"{name}: {coef:.4f}")

# Create a function for easy probability lookup
def get_play_probability(days_rest):
    """Get the probability of the pitcher playing given days of rest"""
    if days_rest < 0:
        return 0.0
    
    prob = model.predict_proba([[days_rest]])[0, 1]
    return prob

print(f"\nUsage Examples:")
print("=" * 50)
print(f"Probability after 1 day rest: {get_play_probability(1):.1%}")
print(f"Probability after 3 days rest: {get_play_probability(3):.1%}")
print(f"Probability after 7 days rest: {get_play_probability(7):.1%}")

# Visualization code (optional)
print(f"\nVisualization Data (for plotting):")
print("=" * 50)
print("Rest Days, Predicted Probability")
for i, prob in enumerate(predicted_probs):
    print(f"{i}, {prob:.4f}")