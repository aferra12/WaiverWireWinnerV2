import pandas as pd
import pandas_gbq
import os
import json
from google.oauth2 import service_account

def write_to_big_query(game_logs: pd.DataFrame, replace_or_append: str):
    """
    Writes Pandas DataFrame of Game Logs to BigQuery Table
    """

    # Get GCP service account credentials
    creds_json = os.environ['GCP_SA_KEY']
    creds_dict = json.loads(creds_json)

    credentials = service_account.Credentials.from_service_account_info(creds_dict)


    pandas_gbq.to_gbq(
        game_logs,
        os.environ['BIG_QUERY_TABLE'],
        project_id=os.environ['PROJECT_ID'],
        chunksize=10000,
        if_exists=replace_or_append,
        credentials=credentials
    )