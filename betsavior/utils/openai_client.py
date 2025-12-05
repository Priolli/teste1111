import os
from typing import List, Optional

from openai import OpenAI

CLIENT = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
MODEL = os.getenv("OPENAI_MODEL", "gpt-4o")

def ask_gpt(user_message: str, history: Optional[List[dict]] = None, *, temperature: float = 0.7) -> str:
    if CLIENT.api_key is None:
        raise ValueError("OPENAI_API_KEY is not configured.")

    messages = history or []
    messages = [*messages, {"role": "user", "content": user_message}]

    response = CLIENT.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=temperature,
    )
    return response.choices[0].message.content or ""
