import os
from string import Template
from typing import Dict
from .prompt_interface import IPrompt
from managers.ai_manager import ai_manager

class BasePrompt(IPrompt):
    def __init__(self, prompt_path):
        self.prompt_path = prompt_path
        self.ai_manager = ai_manager


    def get(self, variables: Dict[str, str]) -> str:
        with open(self.prompt_path, 'r', encoding='utf-8') as f:
            template = Template(f.read())
        return template.safe_substitute(variables)

    def send_prompt(self, text: str) -> str:
        prompt_variables = {
            "srt_content": text
        }

        prompt = self.get(prompt_variables)

        return ai_manager.create_chat(prompt)


            

