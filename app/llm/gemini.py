import os

from google import genai


client = genai.Client(
    api_key=os.environ["GEMINI_API_KEY"]
)


def generate_answer(
    question: str,
    chunks: list,
) -> str:

    context = "\n\n".join(
        f"""
SOURCE {i + 1}

Page: {chunk.page_start}

{chunk.text}
"""
        for i, chunk in enumerate(chunks)
    )

    prompt = f"""
You are an AI research assistant.

Answer the user's question using ONLY the provided
research-paper context.

If the context does not contain enough information
to answer the question, say that you don't have
enough information.

Cite the relevant sources using [SOURCE N].

Question:
{question}

Research context:
{context}
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt,
    )

    return response.text