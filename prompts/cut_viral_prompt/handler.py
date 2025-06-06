import os
from prompts.base_prompt import BasePrompt

class CutViralPrompt(BasePrompt):
    def __init__(self, file=None):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.prompt_path = file if file is not None else os.path.join(base_dir, 'prompt.txt')

cut_viral_prompt = CutViralPrompt()