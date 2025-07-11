import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
from datetime import date, timedelta

def get_last_night_games():
    
    # build a blank array to store the game PKs
    game_pks = []

    # grab the most recent day and hit the MLB API with it
    start_dt = date.today() - timedelta(days=1)
    date_str = start_dt.strftime('%Y-%m-%d')
    url = f"https://statsapi.mlb.com/api/v1/schedule?sportId=1&date={date_str}&gameType=R"

    # grab the response and pull the JSON data to then parse
    response = requests.get(url)
    response.raise_for_status()  # Raise exception for HTTP errors
    data = response.json()
                
    # if the dates are in the date, work through the games and find all the game PKs
    if 'dates' in data and len(data['dates']) > 0:
        for date_data in data['dates']:
            if 'games' in date_data:
                for game in date_data['games']:
                    if 'gamePk' in game and game.get('status', {}).get('detailedState') == 'Final':
                        game_pks.append(game['gamePk'])
    return game_pks
        
    # message = MIMEMultipart()
    # message["From"] = "waiverwirewinner@gmail.com"
    # message["To"] = "angeloferrara12@gmail.com"
    # message["Subject"] = "Last Night's Games"

    # html = f"""
    # <html>
    #     <body>
    #     <p>Last Night's Games:</p>
    #     {game_pks}
    #     </body>
    # </html>
    # """
        
    # # Add body to email
    # message.attach(MIMEText(html, "plain"))
        
    # # Connect to Gmail's SMTP server
    # with smtplib.SMTP("smtp.gmail.com", 587) as server:
    #     # Secure the connection
    #     server.starttls()
            
    #     # Login to your account
    #     server.login("waiverwirewinner@gmail.com", "vkbq fepe grso ytzd")
            
    #     # Send email
    #     server.send_message(message)

