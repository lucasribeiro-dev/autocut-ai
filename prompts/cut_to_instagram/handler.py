import os
from prompts.base_prompt import BasePrompt
from helpers import get_file_from_same_path

class CutViralPromptToInstagram(BasePrompt):
    def __init__(self, file='prompt.txt'):
        prompt_path = get_file_from_same_path(file)
        super().__init__(prompt_path)

cut_viral_prompt_to_instagram = CutViralPromptToInstagram()