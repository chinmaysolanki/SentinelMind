import json
import os
from datetime import datetime
from typing import List, Dict, Any
import logging

class DataStorage:
    def __init__(self, output_dir: str = "data"):
        self.logger = logging.getLogger(__name__)
        self.output_dir = output_dir
        
        # Create output directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
    def save_threats(self, threats: List[Dict[str, Any]]) -> str:
        """
        Save threat data to JSON file
        
        Args:
            threats: List of threat entries to save
            
        Returns:
            Path to the saved file
        """
        try:
            # Generate filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"threats_{timestamp}.json"
            filepath = os.path.join(self.output_dir, filename)
            
            # Format threats to match the requested structure
            formatted_threats = []
            for threat in threats:
                formatted_threat = {
                    "source": threat.get("source", "unknown"),
                    "type": threat.get("type", "unknown"),
                    "summary": threat.get("summary", ""),
                    "date": threat.get("date", datetime.now().strftime("%Y-%m-%d"))
                }
                formatted_threats.append(formatted_threat)
            
            # Write to file
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(formatted_threats, f, indent=2, ensure_ascii=False)
                
            self.logger.info(f"Saved {len(formatted_threats)} threats to {filepath}")
            return filepath
            
        except Exception as e:
            self.logger.error(f"Error saving threats: {str(e)}")
            return ""
            
    def load_latest_threats(self) -> List[Dict[str, Any]]:
        """
        Load the most recent threat data file
        
        Returns:
            List of threat entries
        """
        try:
            # Get list of threat files
            files = [f for f in os.listdir(self.output_dir) 
                    if f.startswith("threats_") and f.endswith(".json")]
            
            if not files:
                return []
                
            # Get most recent file
            latest_file = max(files)
            filepath = os.path.join(self.output_dir, latest_file)
            
            # Load data
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
                
            return data
            
        except Exception as e:
            self.logger.error(f"Error loading threats: {str(e)}")
            return [] 