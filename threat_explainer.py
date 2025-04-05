import os
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv
import json

# Load environment variables from .env file
load_dotenv()

# Initialize the OpenAI LLM
# You can replace this with a HuggingFace model if preferred
llm = OpenAI(
    temperature=0.2,  # Lower temperature for more consistent outputs
    model_name="gpt-3.5-turbo"  # You can change to gpt-4 for better results
)

# Define the prompt template using the provided format
prompt_template = PromptTemplate.from_template(
    "A cybersecurity AI took the action: {action}.\n\n"
    "Threat type: {threat_type}\n"
    "Summary: {summary}\n"
    "Explain why this action is reasonable from a cybersecurity point of view."
)

# Create the LLM chain
chain = LLMChain(llm=llm, prompt=prompt_template)

def explain_threat_action(threat_dict, action_taken):
    """
    Explain why a specific action was taken in response to a cyber threat.
    
    Args:
        threat_dict (dict): A dictionary containing threat information
            {
                "type": "ransomware",
                "summary": "Detected encryption of multiple files in short time",
                "source": "reddit"
            }
        action_taken (str): The action taken in response to the threat
            e.g., "Blocked", "Monitored", "Quarantined"
            
    Returns:
        str: A 2-3 sentence explanation of why this action was taken
    """
    # Extract threat information from the dictionary
    threat_type = threat_dict.get("type", "unknown")
    threat_summary = threat_dict.get("summary", "No summary provided")
    
    # Run the chain to get the explanation
    explanation = chain.run(
        action=action_taken,
        threat_type=threat_type,
        summary=threat_summary
    )
    
    return explanation

# Example usage
if __name__ == "__main__":
    # Example threat
    example_threat = {
        "type": "ransomware",
        "summary": "Detected encryption of multiple files in short time",
        "source": "reddit"
    }
    
    # Example action
    example_action = "Blocked"
    
    # Get the explanation
    explanation = explain_threat_action(example_threat, example_action)
    
    # Print the result
    print("\nThreat Information:")
    print(f"Type: {example_threat['type']}")
    print(f"Summary: {example_threat['summary']}")
    print(f"Source: {example_threat['source']}")
    print(f"Action: {example_action}")
    print("\nExplanation:")
    print(explanation)
    
    # Example with different threat types and actions
    print("\n--- Additional Examples ---\n")
    
    # Phishing example
    phishing_threat = {
        "type": "phishing",
        "summary": "Suspicious email from unknown sender attempting to collect credentials",
        "source": "email_filter"
    }
    phishing_action = "Quarantined"
    print(f"Phishing Threat - Action: {phishing_action}")
    print(explain_threat_action(phishing_threat, phishing_action))
    print()
    
    # Malware example
    malware_threat = {
        "type": "malware",
        "summary": "Malicious executable detected attempting to establish C2 connection",
        "source": "endpoint_protection"
    }
    malware_action = "Blocked"
    print(f"Malware Threat - Action: {malware_action}")
    print(explain_threat_action(malware_threat, malware_action))
    print()
    
    # DDoS example
    ddos_threat = {
        "type": "ddos",
        "summary": "Unusual traffic spike detected from multiple sources",
        "source": "network_monitor"
    }
    ddos_action = "Mitigated"
    print(f"DDoS Threat - Action: {ddos_action}")
    print(explain_threat_action(ddos_threat, ddos_action)) 