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
    def build(self, text: str) -> str:
        """
        Build and process a prompt with the given text content.
        
        Args:
            text (str): The text content to be processed by the prompt
            
        Returns:
            str: The processed result from the AI model
        """
        pass


    