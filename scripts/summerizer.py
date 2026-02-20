#just in case

import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_summary(text):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Summarize this podcast episode in 2 concise sentences in French."},
            {"role": "user", "content": text}
        ]
    )
    return response.choices[0].message.content.strip()