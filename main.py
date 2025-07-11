import os
from fastapi import FastAPI, HTTPException
import uvicorn
import datetime
# Import your helper modules as needed
# from helpers.data_processor import process_data
# from helpers.api_client import fetch_data
from helpers.getLastNightGames import get_last_night_games
from helpers.getPlayerGameLogs import get_player_game_logs
from helpers.sendEmail import send_email
from helpers.getGames import get_games
from helpers.writeBigQuery import write_to_big_query

app = FastAPI()

@app.get("/")
async def run_script():
    try:
        # Your dataframe building logic goes here
        #df = build_dataframe()
        ## I SHOULD DELETE THIS FUNCTION AND PASS IN THE MOST RECENT DATES
        ## TO GETGAMES.PY - THEN HAVE A SEPARATE EMAIL SENDING FUNCTION

        last_nights_game_pks = get_last_night_games()
        game_logs = get_player_game_logs(last_nights_game_pks)
        send_email(game_logs)
        
        print("Nightly Game Script completed successfully")
        return {"message": "Nightly GameScript completed successfully"}
    except Exception as e:
        print(f"Script failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Script failed: {str(e)}")
    
@app.get("/run_backfill")
async def run_backfill(start_date: str, end_date: str):
    try:

        game_pks = get_games(start_date, end_date)
        game_logs = get_player_game_logs(game_pks)

        print("Game Logs Completed...")
        
        write_to_big_query(game_logs)

        print("Game Logs Backfill Script completed successfully")
        return {"message": "Game Logs BackfillScript completed successfully"}
    except Exception as e:
        print(f"Script failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Script failed: {str(e)}")

def build_dataframe():
    # Your actual dataframe building code
    # This is where you'll call your helper files
    pass

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))