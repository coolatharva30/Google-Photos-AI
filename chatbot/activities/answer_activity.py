from magents.answer_agent import generate_answer


def answer_activity(input_data):

    question = input_data["question"]

    sql_result = input_data["sql_result"]

    answer = generate_answer(
        question,
        sql_result
    )

    return {
        "answer": answer
    }