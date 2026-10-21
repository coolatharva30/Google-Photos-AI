import azure.durable_functions as df
import logging

def orchestrator_function(context):
    
    request = context.get_input() or {}

    question = request.get("question", "")
    session_id = request.get("session_id")
    conversation_history = request.get("conversation_history", [])
    # task_state = request.get("task_state", {})
    latest_question = request.get("question", "")

    # -------------------------
    # STEP 1
    # Route the question
    # -------------------------
    if not question or not latest_question:
        return {
            "status": "failed",
            "session_id": session_id,
            "message": "Question cannot be empty."
        }
    logging.info("Before payload called")
    payload = {
            "original_question": question,
            "latest_question":latest_question,
            "conversation_history": conversation_history,
            # "task_state": {
            #     **task_state,        
            # },
            # "schema_context": request.get("schema_context", ""),
            
        }
    

    result = yield context.call_activity(
            "clarification_activity",
            payload
        )
   
    logging.info("clarification activity called")
    decision = result.get("decision")
    
    if decision not in {
            "clarification_required",
            "ready",
            "out_of_scope"
        }:
            return {
                "status": "failed",
                "session_id": session_id,
                "message": "Invalid response from clarification agent."
            }
        
    if decision == "out_of_scope":
            return {
                "status": "out_of_scope",
                "session_id": session_id,
                "reply": result.get(
                    "reason",
                    "Sorry, I cannot handle this request."
                )
            }

    if decision == "clarification_required":
            updated_history = conversation_history + [
                  {"role":"user", "content": latest_question },
                  {
                        "role": "assistant",
                        "content": result.get("clarification_question", "")
                  }
            ]
            return {
                "status": "waiting_clarification",
                "session_id": session_id,
                "original_question": question,
                "clarification_question": result.get(
                  "clarification_question", ""    
                ),
                "conversation_history": updated_history[-3:],
                # "task_state": {**task_state,}
            }

    
    
    if decision == "ready":

        route_result = yield context.call_activity(
                "router_activity",
                {
                    "question": question
                }
            )
       
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