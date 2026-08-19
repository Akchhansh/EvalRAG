import json
from app.services.rag_services import ask_question
from app.services.llm_services import judge_answer

def run_evaluation():
    with open("eval/golden_dataset.json","r") as file:
        dataset=json.load(file)

    results=[]
    correct=0

    for item in dataset:
        question= item["question"]
        expected= item["expected_answer"]

        response=ask_question(question)
        generated = response["answer"]

        judgement = judge_answer(
            question=question,
            expected=expected,
            generated=generated
        )

        is_correct = judgement.strip().upper().startswith("YES")      


        if is_correct:
            correct+=1
        results.append({
            "question": question,
            "expected": expected,
            "generated": generated,
            "judge":judgement,
            "correct": is_correct
        })

    accuracy = (correct / len(dataset)) * 100

    return {
        "total_questions": len(dataset),
        "correct_answers": correct,
        "accuracy": round(accuracy, 2),
        "results": results
    }