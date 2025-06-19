import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pandas as pd

def get_last_night_games(game_logs):

    top_starting_pitchers = game_logs[game_logs['isPitcher'] == True].nlargest(7, 'hilltopperPts')[['playerName', 'outs', 'hilltopperPts']]
    top_relief_pitchers = game_logs[game_logs['isPitcher'] == True and game_logs['isStarter'] == False].nlargest(7, 'hilltopperPts')[['playerName', 'outs', 'hilltopperPts']]
    top_batters = game_logs[game_logs['isPitcher'] == False].nlargest(7, 'hilltopperPts')[['playerName', 'homeRuns', 'hilltopperPts']]
        
    message = MIMEMultipart()
    message["From"] = "waiverwirewinner@gmail.com"
    message["To"] = "angeloferrara12@gmail.com"
    message["Subject"] = "Last Night's Games"

    # Convert DataFrames to HTML
    starting_pitchers_html = top_starting_pitchers.to_html(index=False, table_id="starting_pitchers")
    relief_pitchers_html = top_relief_pitchers.to_html(index=False, table_id="relief_pitchers")
    batters_html = top_batters.to_html(index=False, table_id="batters")

    html = f"""
    <html>
        <head>
            <style>
                table {{
                    border-collapse: collapse;
                    width: 100%;
                    margin-bottom: 20px;
                }}
                th, td {{
                    border: 1px solid #ddd;
                    padding: 8px;
                    text-align: left;
                }}
                th {{
                    background-color: #f2f2f2;
                }}
            </style>
        </head>
        <body>
            <h2>Last Night's Games</h2>
            
            <h3>Top 5 Pitchers</h3>
            {relief_pitchers_html}
            
            <h3>Top 5 Pitchers</h3>
            {starting_pitchers_html}
            
            <h3>Top 5 Batters</h3>
            {batters_html}
        </body>
    </html>
    """
        
    # Add body to email
    message.attach(MIMEText(html, "html"))
        
    # Connect to Gmail's SMTP server
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        # Secure the connection
        server.starttls()
            
        # Login to your account
        server.login("waiverwirewinner@gmail.com", "vkbq fepe grso ytzd")
            
        # Send email
        server.send_message(message)