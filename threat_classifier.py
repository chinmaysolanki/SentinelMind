from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
from typing import Dict, Any, List
import logging

class ThreatClassifier:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
        # Load pre-trained model and tokenizer
        self.model_name = "bert-base-uncased"
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(
            self.model_name,
            num_labels=5  # Adjust based on your threat categories
        ).to(self.device)
        
        self.threat_categories = {
            0: "Malware",
            1: "Vulnerability",
            2: "Attack",
            3: "Data Breach",
            4: "Other"
        }
        
    def classify_text(self, text: str) -> Dict[str, Any]:
        """
        Classify text using BERT model
        
        Args:
            text: Text to classify
            
        Returns:
            Dictionary with classification results
        """
        try:
            # Tokenize and prepare input
            inputs = self.tokenizer(
                text,
                truncation=True,
                padding=True,
                max_length=512,
                return_tensors="pt"
            ).to(self.device)
            
            # Get model predictions
            with torch.no_grad():
                outputs = self.model(**inputs)
                probabilities = torch.softmax(outputs.logits, dim=1)
                predicted_class = torch.argmax(probabilities, dim=1).item()
                confidence = probabilities[0][predicted_class].item()
            
            return {
                "threat_category": self.threat_categories[predicted_class],
                "confidence": confidence,
                "raw_probabilities": probabilities[0].tolist()
            }
            
        except Exception as e:
            self.logger.error(f"Error classifying text: {str(e)}")
            return {
                "threat_category": "Unknown",
                "confidence": 0.0,
                "raw_probabilities": []
            }
            
    def classify_batch(self, texts: List[str]) -> List[Dict[str, Any]]:
        """
        Classify a batch of texts
        
        Args:
            texts: List of texts to classify
            
        Returns:
            List of classification results
        """
        return [this.classify_text(text) for text in texts] 