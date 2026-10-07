from magents.sql_agent import generate_sql
from services.sql_service import execute_query


DATABASE_SCHEMA = """
DATABASE: kdac_db


TABLE: users_1

Columns:
id INT
name VARCHAR
email VARCHAR
password VARCHAR
mobile VARCHAR

TABLE: products

Columns:
pid INT
name VARCHAR
price DECIMAL



Dynamic user photo tables:

Table pattern:
    user_{user_id}_photos

Each registered user has one table following this pattern.

Example:
    user_1_photos
    user_2_photos
    user_3_photos
    ...
    user_N_photos

Columns in every user photo table:

    id              INT
    filename        VARCHAR
    content_type    VARCHAR
    image_data      VARBINARY
    latitude        FLOAT
    longitude       FLOAT
    created_at      DATETIME

IMPORTANT:
- {user_id} must come from the authenticated application user.
- Never allow the LLM to choose another user's ID.
- The LLM must only query the current authenticated user's table.

"""


def sql_activity(input_data):

    question = input_data["question"]

    sql_query = generate_sql(
        question,
        DATABASE_SCHEMA
    )

    data = execute_query(
        sql_query
    )

    return {
        "source": "SQL_SERVER",
        "query": sql_query,
        "data": data
    }
