import os
import json
from groq import Groq

class GroqServices:

    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")

        if not api_key:
            raise ValueError("GROQ_API_KEY is issing")

        self.client = Groq(api_key=api_key)

    def generate(self, system_prompt, user_prompt):
        response  = self.client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {
                    "role":"system",
                    "content":system_prompt
                },
                {
                    "role": "user",
                    "content": user_prompt
                }
                
            ],
            temperature=0
        )

        return response.choices[0].message.content


    def generate_json(
            self,
            system_prompt,
            user_prompt,
            schema
    ):
        response = self.client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {
                   "role": "system",
                    "content": system_prompt 
                },
                {
                    "role": "user",
                    "content": user_prompt
                }
            ],

            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": "response",
                    "strict": True,
                    "schema": schema
                }
            },
            temperature=0
        )

        return json.loads(
            response.choices[0].message.content
        )


groq_service = GroqServices()
