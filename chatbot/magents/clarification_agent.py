
import json
import os
from groq import Groq
from pathlib import Path
import yaml
import logging

client = Groq(api_key=os.environ["GROQ_API_KEY"])

PROMPT_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "prompts",
    "clarification.yaml"
)


def load_prompt():

    with open(
        PROMPT_PATH,
        "r",
        encoding="utf-8"
    ) as file:

        return file.read()

def clarification_agent(payload: dict) -> dict:
    original_question = payload.get("original_question", "")
    latest_question = payload.get("latest_question", "")
    conversation_history = payload.get("conversation_history", [])[-3:]
    

    system_prompt = load_prompt()

    user_prompt = {
        "original_question": original_question,
        "latest_message": latest_question,
        "conversation_history": conversation_history,
        # "task_state": task_state,
        # "schema_context": schema_context+
    }
    logging.info("Before calling the agent")
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

        decision = result.get("decision")
        if decision not in {
            "clarification_required",
            "ready",
            "out_of_scope"
        }:
            return {
                "decision": "error",
                "clarification_question": "",
                # "task_state": task_state,
                "message": "Invalid decision returned by the model."
            }

        # if not isinstance(result.get("task_state"), dict):
        #     result["task_state"] = task_state

        result.setdefault("clarification_question", "")
        result.setdefault("message", "")

        return result

    except Exception as exc:
        # Fail safely rather than treating an LLM error as "ready".
        return {
            "decision": "error",
            "clarification_question": "",
            # "task_state": task_state,
            "message": f"Clarification agent failed: {str(exc)}"
        }
