import os
import json
from services.groq_services import groq_service
from groq import Groq

client = Groq(api_key=os.environ["GROQ_API_KEY"])

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


def sql_agent(question,plan,result):
    system_prompt = load_prompt()
    user_prompt = {
            "question": question,
            "plan": plan,
            "result": result
        }

    try:
        response= client.chat.completions.create(
                model="openai/gpt-oss-20b",
                messages=[
                        {"role": "system", "content": system_prompt},
                        {
                                "role": "user",
                                "content": json.dumps(user_prompt)
                        }
                ],
                    temperature=0,
                    response_format={"type": "json_object"}
        )
        result = json.loads(response.choices[0].message.content)

        return result

    except Exception as exc:
        return {
                "message": f"SQL agent failed: {str(exc)}",
                "result": result,
            }