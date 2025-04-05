from flask import Blueprint, request, jsonify
import json
import os
import sys

# Add the parent directory to the path so we can import the explainer
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from explainability.llm_explainer import ThreatActionExplainer

# Create the blueprint
explain_bp = Blueprint('explain', __name__)

# Initialize the explainer
explainer = ThreatActionExplainer()

@explain_bp.route('/explain', methods=['POST'])
def explain():
    """
    Generate an explanation for a single threat-action pair.
    
    Expected JSON payload:
    {
        "threat": {
            "id": "threat_1",
            "type": "ransomware",
            "summary": "Detected encryption of multiple files in short time",
            "source": "endpoint_protection",
            "timestamp": "2023-11-01T12:00:00",
            "severity": "high"
        },
        "action": "Blocked"
    }
    """
    try:
        data = request.get_json()
        threat = data.get('threat')
        action = data.get('action')
        
        if not threat or not action:
            return jsonify({"error": "Missing threat or action"}), 400
        
        explanation = explainer.explain_action(threat, action)
        return jsonify({
            "explanation": explanation,
            "threat": threat,
            "action": action
        })
    except Exception as e:
        print(f"Error generating explanation: {str(e)}")
        return jsonify({"error": str(e)}), 500

@explain_bp.route('/batch_explain', methods=['POST'])
def batch_explain():
    """
    Generate explanations for multiple threat-action pairs.
    
    Expected JSON payload:
    {
        "pairs": [
            {
                "threat": {
                    "id": "threat_1",
                    "type": "ransomware",
                    "summary": "Detected encryption of multiple files in short time",
                    "source": "endpoint_protection",
                    "timestamp": "2023-11-01T12:00:00",
                    "severity": "high"
                },
                "action": "Blocked"
            },
            {
                "threat": {
                    "id": "threat_2",
                    "type": "phishing",
                    "summary": "Suspicious email from unknown sender attempting to collect credentials",
                    "source": "email_filter",
                    "timestamp": "2023-11-01T12:05:00",
                    "severity": "medium"
                },
                "action": "Quarantined"
            }
        ]
    }
    """
    try:
        data = request.get_json()
        pairs = data.get('pairs', [])
        
        if not pairs:
            return jsonify({"error": "Missing pairs"}), 400
        
        explanations = explainer.batch_explain(pairs)
        
        # Create a response with explanations and original data
        result = []
        for i, pair in enumerate(pairs):
            result.append({
                "explanation": explanations[i],
                "threat": pair['threat'],
                "action": pair['action']
            })
        
        return jsonify({"results": result})
    except Exception as e:
        print(f"Error generating batch explanations: {str(e)}")
        return jsonify({"error": str(e)}), 500 