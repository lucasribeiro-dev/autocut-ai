from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

class AIManager():
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_KEY"))

    def create_chat(self, prompt, model='gpt-4.1-mini'):
        
        response = self.client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "Você receberá a transcrição completa de um vídeo no formato .SRT (com timestamps). Analise o conteúdo e siga as instruções abaixo."},
                {"role": "user", "content": prompt}
            ]
        )
        
        return response.choices[0].message.content 


ai_manager = AIManager()