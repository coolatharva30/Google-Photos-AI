
from magents.answer_agent import generate_answer
import logging


def answer_activity(input_data: dict):
    question = input_data.get("question", "")
    sql_result = input_data.get("sql_result", {})
    conversation_history = input_data.get("conversation_history", [])

    logging.info("Answer activity started")

    if not question:
        return {
            "answer": "I couldn't identify your question."
        }

    if not isinstance(sql_result, dict):
        return {
            "answer": "I couldn't retrieve valid data to answer your question."
        }

    try:
        answer = generate_answer(
            question=question,
            sql_result=sql_result,
            conversation_history=conversation_history
        )

        logging.info("Answer activity completed")

        return {
            "answer": answer
        }

    except Exception:
        logging.exception("Answer generation failed")

        return {
            "answer": "Sorry, I couldn't generate an answer right now."
        }
