# db.py
from databricks import sql
from os import environ
from dotenv import load_dotenv
from typing import Any, Dict, List, Tuple

# Load .env variables
load_dotenv()

def get_connection():
    """
    Returns a Databricks SQL connection using environment variables.
    """
    return sql.connect(
        server_hostname=environ.get("DATABRICKS_SERVER"),
        http_path=environ.get("DATABRICKS_HTTP_PATH"),
        access_token=environ.get("DATABRICKS_TOKEN")
    )

def run_dbquery(query: str, params: Dict[str, Any] = {}) -> List[Tuple]:
    """
    Executes a SQL query with optional named parameters and returns all rows.

    Args:
        query: SQL query string using optional named parameters e.g. %(param)s
        params: Dictionary of parameter values, e.g. {'customer_id': 42}

    Returns:
        List of tuples representing rows.
    """
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, params)
            columns = [col[0] for col in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]
