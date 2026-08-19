from app.services.search_services import search_documents
from app.services.llm_services import generate_answer


def ask_question(question: str):
    results = search_documents(question)

    context = ""

    for result in results:
        context += result.payload["text"] + "\n\n"

    answer = generate_answer(
        context=context,
        question=question
    )

    return {
        "question": question,
        "answer": answer
    }