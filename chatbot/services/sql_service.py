import os
import pyodbc
from sqlalchemy import create_engine, text

def get_connection():

    connection_string = os.getenv(
        "SQL_CONNECTION_STRING"
    )

    if not connection_string:
        raise ValueError(
            "SQL_CONNECTION_STRING is missing"
        )

    engine = create_engine(
        connection_string,
        pool_pre_ping=True
    )

    return engine.connect()



def validate_query(query):

    query = query.strip()

    if not query.lower().startswith("select"):
        raise ValueError(
            "Only SELECT queries are allowed"
        )

    forbidden_keywords = [
        "insert",
        "update",
        "delete",
        "drop",
        "alter",
        "truncate",
        "create",
        "exec",
        "execute"
    ]

    query_lower = query.lower()

    for keyword in forbidden_keywords:

        if keyword in query_lower:

            raise ValueError(
                f"Forbidden SQL operation: {keyword}"
            )


def execute_query(query, parameters=None, user_id=None):
    if (
        isinstance(user_id, bool)
        or not isinstance(user_id, int)
        or user_id <= 0
    ):
        raise ValueError("A valid authenticated user_id is required")

    if "USER_PHOTO_TABLE" in query:
        query = query.replace(
            "USER_PHOTO_TABLE",
            f"user_{user_id}_photos"
        )

    validate_query(query)
    connection = get_connection()

    try:
        result = connection.execute(
            text(query),
            parameters or {},
        )
        return [dict(row) for row in result.mappings().all()]
    finally:
        connection.close()