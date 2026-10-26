
from magents.sql_agent import sql_agent
from services.sql_service import execute_query
import logging


def sql_activity(input_data: dict):
    question = input_data["question"]
    planner_output = input_data["plan"]

    # Support the planner structure shown in your earlier logs.
    plan = planner_output.get("result", planner_output)

    steps = plan.get("steps", [])
    results = []

    if not steps:
        raise ValueError("Planner returned no SQL steps.")

    # Run steps in the order supplied by the planner.
    for step in steps:
        step_id = step.get("step_id")

        # Pass the current step and previously executed results.
        agent_result = sql_agent(
        question,
            {
                "current_step": step,
                "plan": plan,
            },
            results,
        )

        query = agent_result["query"]
        parameters = agent_result.get("parameters", {})

        if not query:
            raise ValueError(
                f"SQL agent returned an empty query for {step_id}."
            )

        logging.info(
            "Executing SQL for step %s: %s",
            step_id,
            query,
        )

        # This assumes execute_query accepts a validated query string.
        rows = execute_query(query, parameters)
        if not rows and step_id == "step_1":
            return {
                "status": "not_found",
                "message": "No user found with the provided name.",
                "results": results,
            }
        step_result = {
            "step_id": step_id,
            "status": "success",
            "query": query,
            "data": rows,
            "row_count": len(rows),
        }

        results.append(step_result)

        logging.info(
            "SQL step %s returned %d rows.",
            step_id,
            len(rows),
        )

    return {"result": results}
