import json
from openai import OpenAI
from utils.prompts import TRANSLATION_PROMPT

class Translator:
    def __init__(self, model="gpt-4o-mini"):
        self.client = OpenAI()
        self.model = model

    def translate(self, english_texts: dict):
        if not english_texts:
            return {}
        texts_list = "\n".join([f"{k}: {v}" for k, v in english_texts.items()])
        prompt = TRANSLATION_PROMPT.format(texts=texts_list)
        try:
            resp = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2,
                max_tokens=2000
            )
            content = resp.choices[0].message.content.strip()
            if content.startswith("```json"):
                content = content[7:-3]
            elif content.startswith("```"):
                content = content[3:-3]
            return json.loads(content)
        except Exception as e:
            print(f"Translation error: {e}")
            return english_texts
