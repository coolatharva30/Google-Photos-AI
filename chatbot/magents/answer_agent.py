import os
import json

from services.groq_services import groq_service


PROMPT_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "prompts",
    "answer_prompt.yaml"
)


def load_prompt():

    with open(
        PROMPT_PATH,
        "r",
        encoding="utf-8"
    ) as file:

        return file.read()

def generate_answer(question, sql_result, conversation_history=None):
    system_prompt = load_prompt()

    user_prompt = f"""
User's original question:
{question}

Conversation history, including clarification:
{json.dumps(conversation_history or [], indent=2)}

SQL result:
{json.dumps(sql_result, indent=2, default=str)}
"""

    return groq_service.generate(system_prompt, user_prompt)