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


def execute_query(query):

    validate_query(query)

    connection = get_connection()

    try:

        result = connection.execute(
            text(query)
        )

        rows = result.mappings().all()

        return [dict(row) for row in rows]

    finally:

        connection.close()