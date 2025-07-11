import pandas as pd
from pandas_gbq import to_gbq
import os
import json
import tempfile

def write_to_big_query(game_logs: pd.DataFrame):
    """
    Writes Pandas DataFrame of Game Logs to BigQuery Table
    """

    # Create temporary credentials file
    creds_json = os.environ['GCP_SA_KEY']
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        f.write(creds_json)
        creds_path = f.name

    game_logs.to_gbq(
        os.environ['BIG_QUERY_TABLE'],
        project_id=os.environ['PROJECT_ID'],
        chunksize=10000,
        if_exists='replace',
        credentials=creds_path
    )