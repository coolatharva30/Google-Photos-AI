import azure.functions as func
import azure.durable_functions as df


app = df.DFApp(
    http_auth_level=func.AuthLevel.ANONYMOUS
)


# =========================================================
# HTTP TRIGGER
# =========================================================

@app.route(
    route="chat",
    methods=["POST"]
)
@app.durable_client_input(
    client_name="client"
)
async def chat(
    req: func.HttpRequest,
    client
):

    body = req.get_json()

    instance_id = await client.start_new(
        "chat_orchestrator",
        None,
        body
    )

    return client.create_check_status_response(
        req,
        instance_id
    )


# =========================================================
# ORCHESTRATOR
# =========================================================

@app.orchestration_trigger(
    context_name="context"
)
def chat_orchestrator(context):

    from orchestrators.chat_orchestrator import (
        orchestrator_function
    )

    return orchestrator_function(context)


# =========================================================
# ROUTER ACTIVITY
# =========================================================

@app.activity_trigger(
    input_name="input_data"
)
def router_activity(input_data):

    from activities.router_activity import (
        router_activity as execute_router_activity
    )

    return execute_router_activity(input_data)


# =========================================================
# SQL ACTIVITY
# =========================================================

@app.activity_trigger(
    input_name="input_data"
)
def sql_activity(input_data):

    from activities.sql_activity import (
        sql_activity as execute_sql_activity
    )

    return execute_sql_activity(input_data)


# =========================================================
# ANSWER ACTIVITY
# =========================================================

@app.activity_trigger(
    input_name="input_data"
)
def answer_activity(input_data):

    from activities.answer_activity import (
        answer_activity as execute_answer_activity
    )

    return execute_answer_activity(input_data)


@app.activity_trigger(input_name="payload")
def clarification_activity(payload: dict) -> dict:

    from activities.clarification_activity import clarification_activity
   
    return clarification_activity(payload)

# =========================================================
# PLANNER ACTIVITY
# =========================================================

@app.activity_trigger(input_name="input_data")
def planner_activity(input_data: dict):

    from activities.planner_activity import (
        planner_activity as execute_planner_activity
    )

    return execute_planner_activity(input_data)