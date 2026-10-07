import azure.durable_functions as df
import logging

def orchestrator_function(context):

    request = context.get_input()

    question = request["question"]

    # -------------------------
    # STEP 1
    # Route the question
    # -------------------------

    route_result = yield context.call_activity(
        "router_activity",
        {
            "question": question
        }
    )
    logging.info("Activity called", route_result)
    # -------------------------
    # STEP 2
    # Check whether SQL is required
    # -------------------------

    if not route_result["use_sql"]:

        return {
            "answer": (
                "I currently only have access to "
                "the SQL Server data source, and "
                "your question does not appear to "
                "require SQL data."
            )
        }
        
    # -------------------------
    # STEP 3
    # Retrieve SQL data
    # -------------------------

    sql_result = yield context.call_activity(
        "sql_activity",
        {
            "question": question
        }
    )
    logging.info("SQL Activity called")
    # -------------------------
    # STEP 4
    # Generate final answer
    # -------------------------

    answer_result = yield context.call_activity(
        "answer_activity",
        {
            "question": question,
            "sql_result": sql_result
        }
    )

    return answer_result


main = df.Orchestrator.create(
    orchestrator_function
)