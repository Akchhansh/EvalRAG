import os
import google.generativeai as genai

from dotenv import load_dotenv

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model= genai.GenerativeModel("gemini-flash-latest")

def generate_answer(context,question):
    prompt= f"""You are a helpful assistant.Answer ONLY using the context below. If the answer is not present, reply:
    "I don't know."
    Context:{context}
    Question:{question}
    Answer:"""

    response= model.generate_content(prompt)
    return response.text


def judge_answer(question, expected, generated):
    prompt = f"""
You are an AI evaluator.

Question:
{question}

Expected Answer:
{expected}

Generated Answer:
{generated}

Are the expected answer and generated answer semantically equivalent?

Reply ONLY with YES or NO.
"""

    response = model.generate_content(prompt)

    return response.text.strip()