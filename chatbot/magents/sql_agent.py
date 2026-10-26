
import os
import logging
import json
from groq import Groq

client = Groq(api_key=os.environ["GROQ_API_KEY"])

PROMPT_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "prompts",
    "sql_prompt.yaml",
)


def load_prompt():
    with open(PROMPT_PATH, "r", encoding="utf-8") as file:
        return file.read()


def sql_agent(question, plan, results):
    system_prompt = load_prompt()

    user_prompt = {
        "question": question,
        "plan": plan,
        "results": results,
    }

    try:
        response = client.chat.completions.create(
                model="openai/gpt-oss-20b",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            system_prompt
                            + "\nReturn only a valid JSON object with these keys: "
                            + "status, query, parameters. "
                            + "The query must contain exactly one SQL SELECT statement. "
                            + "Do not return results or a final answer."
                        ),
                    },
                    {
                        "role": "user",
                        "content": json.dumps(user_prompt),
                    },
                ],
                temperature=0,
                response_format={"type": "json_object"},
            )

        content = response.choices[0].message.content

        if not content or not content.strip():
            raise ValueError("The SQL agent returned an empty response.")

        query = content.strip()

        if query.startswith("```"):
            raise ValueError(
                "The SQL agent returned Markdown instead of plain SQL."
            )

        logging.info("SQL agent generated query: %s", query)

        return json.loads(content)

    except Exception as exc:
        logging.exception("SQL agent failed.")
        raise RuntimeError(f"SQL agent failed: {exc}") from exc
