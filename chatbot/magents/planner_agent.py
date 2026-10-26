import json
import logging
import yaml
from pathlib import Path
from groq import Groq
import os

client = Groq(api_key=os.environ["GROQ_API_KEY"])

PROMPT_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "prompts",
    "planner_prompts.yaml"
)

def load_prompt():
    with open(
        PROMPT_PATH,
        "r",
        encoding="utf-8"
    ) as file:
        return file.read()

def planner_agent(input: dict) -> dict:
    question = input.get("question")
    conversation_history = input.get("conversation_history")

    system_prompt = load_prompt()

    user_prompt = {
        "question": question,
        "conversation_history": conversation_history
    }

    try:
        response = client.chat.completions.create(
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

        result = json.loads(
            response.choices[0].message.content
        )

        number_of_queries = result.get("n")

        return {
           "result": result,
            "number_of_queries":number_of_queries,
        }

    except Exception as exc:
        return {
            "message": f"Planner agent failed: {str(exc)}",
            "result": result
        }