import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()


SYSTEM_PROMPT = """
You are a helpful, knowledgable research assistant.

Answer the user's question using ONLY the
provided knowledge-base context.

Rules:

1. Do not invent information.
2. If the context does not contain the answer,
   say that you do not have enough information.
3. Keep answers concise and helpful.
4. Cite supporting documents using:
   [source: filename]
"""


class LLM:

    def __init__(self):

        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise RuntimeError(
                "GEMINI_API_KEY is not set."
            )

        self.client = genai.Client(
            api_key=api_key
        )

        self.model = os.getenv(
            "GEMINI_MODEL",
            "gemini-3.6-flash",
        )

    def generate(
        self,
        question: str,
        context: str,
    ):

        prompt = f"""
Knowledge base:

{context}

User question:

{question}
"""

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
            ),
        )

        return response.text