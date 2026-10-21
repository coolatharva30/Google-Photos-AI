import logging
from magents.clarification_agent import clarification_agent


def clarification_activity(payload: dict) -> dict:
    logging.info("Clarification activity started")

    try:
        result = clarification_agent(payload)

        logging.info(
            "Clarification activity completed. Decision: %s",
            result.get("decision")
        )

        return result

    except Exception:
        logging.exception("Clarification activity failed")

        return {
            "decision": "error",
            "clarification_question": "",
            # "task_state": payload.get("task_state", {}),
            "message": "Failed to execute clarification agent."
        }