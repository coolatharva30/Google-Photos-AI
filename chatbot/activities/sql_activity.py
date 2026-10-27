
from magents.sql_agent import sql_agent
from services.sql_service import execute_query
import logging


def sql_activity(input_data: dict):
    question = input_data.get("question", "")
    user_id = input_data.get("user_id")
    planner_output = input_data.get("plan")

    # 1. Handle missing planner output.
    if not isinstance(planner_output, dict) or not planner_output:
        return {
            "status": "invalid_plan",
            "message": "Planner returned no usable plan.",
            "results": [],
        }

    # 2. Handle planner errors and unwrap its result.
    plan = planner_output.get("result", planner_output)

    if not isinstance(plan, dict) or not plan:
        planner_message = planner_output.get("message")

        return {
            "status": "planner_failed" if planner_message else "invalid_plan",
            "message": (
                planner_message
                or "Planner returned an empty or invalid plan."
            ),
            "results": [],
        }

    # 3. Handle planner statuses before calling the SQL agent.
    status = plan.get("status")

    if status == "unsupported":
        return {
            "status": "unsupported",
            "message": (
                "I can only access your own account information "
                "and photos. I cannot answer questions about other "
                "users or system-wide statistics."
            ),
            "results": [],
        }

    if status == "needs_clarification":
        return {
            "status": "needs_clarification",
            "message": plan.get(
                "clarification_question",
                "Could you clarify your question?"
            ),
            "results": [],
        }

    if status != "ready":
        return {
            "status": "invalid_plan",
            "message": "Planner did not return a valid ready plan.",
            "results": [],
        }

    # 4. Validate the authenticated user ID.
    # bool is a subclass of int in Python, so reject it explicitly.
    if (
        isinstance(user_id, bool)
        or not isinstance(user_id, int)
        or user_id <= 0
    ):
        return {
            "status": "invalid_input",
            "message": "A valid authenticated user ID is required.",
            "results": [],
        }

    # 5. Validate the plan's steps.
    steps = plan.get("steps")

    if not isinstance(steps, list) or not steps:
        return {
            "status": "invalid_plan",
            "message": "Planner returned no SQL steps.",
            "results": [],
        }

    if plan.get("n") != len(steps):
        return {
            "status": "invalid_plan",
            "message": "Planner query count does not match its steps.",
            "results": [],
        }

    results = []

    # 6. Execute only steps in a ready plan.
    for step in steps:
        if not isinstance(step, dict) or not step.get("step_id"):
            return {
                "status": "invalid_plan",
                "message": "Planner returned an invalid SQL step.",
                "results": results,
            }

        step_id = step["step_id"]

        # Only permit the two approved logical table references.
        table_refs = step.get("table_refs", [])

        if (
            not isinstance(table_refs, list)
            or not table_refs
            or any(
                table not in ("users_1", "USER_PHOTO_TABLE")
                for table in table_refs
            )
        ):
            return {
                "status": "invalid_plan",
                "message": f"Forbidden table reference in {step_id}.",
                "results": results,
            }

        # The SQL agent must receive the authenticated ID explicitly.
        agent_result = sql_agent(
            question,
            {
                "current_step": step,
                "plan": plan,
                "user_id": user_id,
                "conversation_history": input_data.get(
                    "conversation_history", []
                ),
            },
            results,
        )

        if not isinstance(agent_result, dict):
            return {
                "status": "sql_generation_failed",
                "message": f"SQL agent returned an invalid response for {step_id}.",
                "results": results,
            }

        agent_status = agent_result.get("status")

        # Never execute a query unless the SQL agent says ready.
        if agent_status != "ready":
            return {
                "status": agent_status or "sql_generation_failed",
                "message": (
                    agent_result.get("message")
                    or f"SQL agent did not generate a ready query for {step_id}."
                ),
                "results": results,
            }

        query = agent_result.get("query", "")
        parameters = agent_result.get("parameters", {})

        if not isinstance(query, str) or not query.strip():
            return {
                "status": "sql_generation_failed",
                "message": f"SQL agent returned an empty query for {step_id}.",
                "results": results,
            }

        if not isinstance(parameters, dict):
            return {
                "status": "sql_generation_failed",
                "message": f"Invalid SQL parameters for {step_id}.",
                "results": results,
            }

        logging.info("Executing SQL for step %s", step_id)

        try:
            # IMPORTANT:
            # execute_query / a trusted SQL validation layer must validate
            # the SELECT statement, enforce table restrictions, and resolve
            # USER_PHOTO_TABLE using this validated user_id before execution.
            rows = execute_query(
                query,
                parameters,
                # Add user_id to this call only if your execute_query
                # function has been updated to accept it.
            )
        except Exception:
            logging.exception("SQL execution failed for step %s", step_id)
            return {
                "status": "sql_execution_failed",
                "message": f"Database execution failed for {step_id}.",
                "results": results,
            }

        rows = rows or []

        step_result = {
            "step_id": step_id,
            "status": "success",
            "data": rows,
            "row_count": len(rows),
        }

        results.append(step_result)

        logging.info(
            "SQL step %s returned %d rows.",
            step_id,
            len(rows),
        )

    return {
        "status": "success",
        "results": results,
    }
