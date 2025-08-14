import json
from dotenv import load_dotenv
import os
from openai import OpenAI

from utils.prompts import EXTRACTION_PROMPT

load_dotenv()
class CSHTMLExtractor:
    def __init__(self, model="gpt-4o-mini"):
        self.client = OpenAI()
        self.model = model

    def extract_and_generate_keys(self, cshtml_content: str, filename: str):
        prompt = EXTRACTION_PROMPT.format(filename=filename, content=cshtml_content)
        try:
            resp = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1,
                max_tokens=3000
            )
            content = resp.choices[0].message.content.strip()
            if content.startswith("```json"):
                content = content[7:-3]
            elif content.startswith("```"):
                content = content[3:-3]
            return json.loads(content)
        except Exception as e:
            print(f"Error extracting from {filename}: {e}")
            return {"extracted_items": []}
