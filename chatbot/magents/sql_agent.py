import os

from services.groq_services import groq_service


PROMPT_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "prompts",
    "sql_prompt.yaml"
)


def load_prompt():

    with open(
        PROMPT_PATH,
        "r",
        encoding="utf-8"
    ) as file:

        return file.read()


def generate_sql(question, schema):

    system_prompt = load_prompt()

    user_prompt = f"""
User question:

{question}

Database schema:

{schema}
"""

    sql = groq_service.generate(
        system_prompt,
        user_prompt
    )

    return sql.strip()