import os
from langchain_community.llms import OpenAI
from dotenv import load_dotenv
from typing import List, Dict, Any

# Load environment variables from .env file
load_dotenv()

class ThreatActionExplainer:
    """
    A class that uses LangChain and OpenAI to generate explanations for cybersecurity decisions.
    """
    
    def __init__(self):
        """Initialize the explainer with OpenAI LLM."""
        self.llm = OpenAI(
            temperature=0.7,
            model_name="gpt-3.5-turbo-instruct"
        )
        
    def explain_action(self, threat: Dict[str, Any], action: str) -> str:
        """
        Generate an explanation for a single threat-action pair.
        
        Args:
            threat (Dict[str, Any]): A dictionary containing threat information
                {
                    "type": str,
                    "summary": str,
                    "source": str,
                    "severity": str
                }
            action (str): The action taken in response to the threat
                e.g., "Blocked", "Monitored", "Quarantined"
                
        Returns:
            str: A clear explanation of why this action was taken
        """
        prompt = self._create_prompt(threat, action)
        return self.llm.predict(prompt)
    
    def batch_explain(self, pairs: List[Dict[str, Any]]) -> List[str]:
        """
        Generate explanations for multiple threat-action pairs.
        
        Args:
            pairs (List[Dict[str, Any]]): A list of dictionaries, each containing:
                {
                    'threat': Dict[str, Any],  # Threat information
                    'action': str              # Action taken
                }
                
        Returns:
            List[str]: A list of explanations for each threat-action pair
        """
        explanations = []
        for pair in pairs:
            explanation = self.explain_action(pair['threat'], pair['action'])
            explanations.append(explanation)
        return explanations
    
    def _create_prompt(self, threat: Dict[str, Any], action: str) -> str:
        """
        Create a prompt for the LLM to explain the action.
        
        Args:
            threat (Dict[str, Any]): The threat information
            action (str): The action taken
            
        Returns:
            str: A formatted prompt string
        """
        return f"""Given the following cybersecurity threat and action taken, explain why this action was appropriate or not:

Threat Details:
- Type: {threat['type']}
- Summary: {threat['summary']}
- Source: {threat['source']}
- Severity: {threat['severity']}

Action Taken: {action}

Provide a clear and concise explanation of why this action was taken and its potential effectiveness:""" 