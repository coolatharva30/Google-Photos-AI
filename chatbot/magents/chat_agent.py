import os

from services.groq_services import groq_service


PROMPT_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "prompts",
    "chat_agent.yaml"
)


def load_prompt():

    with open(
        PROMPT_PATH,
        "r",
        encoding="utf-8"
    ) as file:

        return file.read()


def route_question(question):

    system_prompt = load_prompt()

    schema = {
        "type": "object",
        "properties": {
            "use_sql": {
                "type": "boolean"
            },
            "reason": {
                "type": "string"
            }
        },
        "required": [
            "use_sql",
            "reason"
        ],
        "additionalProperties": False
    }

    return groq_service.generate_json(
        system_prompt,
        question,
        schema
    )