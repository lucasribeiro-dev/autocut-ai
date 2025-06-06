from abc import ABC, abstractmethod
from typing import Dict

class IPrompt(ABC):
    """Interface for prompt classes that handle template-based prompts."""
    
    @abstractmethod
    def get(self, variables: Dict[str, str]) -> str:
        """
        Get the processed prompt with substituted variables.
        
        Args:
            variables (Dict[str, str]): Dictionary containing variables to substitute in the prompt template
            
        Returns:
            str: The processed prompt with all variables substituted
        """
        pass 
    
    @abstractmethod
    def send_prompt(self, text: str, model='gpt-4.1-mini') -> str:
        """
        Send a prompt to the OpenAI API and return the response.
        
        Args:
            text (str): The text to send to the OpenAI API
            model (str): The model to use for the API call
            
        Returns:
            str: The response from the OpenAI API
        """
        pass 