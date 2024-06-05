import os
from pathlib import Path

import psycopg2

def getRootFolder() -> Path:
    return Path(__file__).parent.parent


def get_db_connection(username, password):
    try:
        conn = psycopg2.connect(
            host='instance-name-cluster-prod.cluster-c2mg79iwhd6d.us-east-1.rds.amazonaws.com',
            database='instance-nameprod',  # Specify your database name
            user=username,
            password=password,
            port='5432'
        )
        return conn
    except Exception as e:
        print(f"Unable to connect to the database: {str(e)}")
        return None