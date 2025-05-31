import os
from fastapi import FastAPI, HTTPException
import uvicorn
# Import your helper modules as needed
# from helpers.data_processor import process_data
# from helpers.api_client import fetch_data

app = FastAPI()

@app.get("/")
async def run_script():
    try:
        # Your dataframe building logic goes here
        # df = build_dataframe()
        # process_and_save_data(df)
        
        print("Script completed successfully")
        return {"message": "Script completed successfully"}
    except Exception as e:
        print(f"Script failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Script failed: {str(e)}")

def build_dataframe():
    # Your actual dataframe building code
    # This is where you'll call your helper files
    pass

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))