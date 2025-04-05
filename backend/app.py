from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import os
import json
from datetime import datetime, timedelta
import random

# Import the blueprints
from routes.explain import explain_bp

# Initialize the Flask app
app = Flask(__name__, static_folder='../frontend/build', static_url_path='')

# Enable CORS
CORS(app)

# Register the blueprints
app.register_blueprint(explain_bp, url_prefix='/api')

# Sample data files
THREATS_FILE = 'data/threats.json'
ACTIONS_FILE = 'data/actions.json'

# Ensure the data directory exists
os.makedirs('data', exist_ok=True)

# Create sample data files if they don't exist
def create_sample_data():
    """Create sample data files if they don't exist."""
    if not os.path.exists(THREATS_FILE):
        threats = []
        threat_types = ['ransomware', 'phishing', 'malware', 'ddos', 'zero-day']
        for i in range(20):
            threat_type = random.choice(threat_types)
            if threat_type == 'ransomware':
                summary = "Detected encryption of multiple files in short time"
            elif threat_type == 'phishing':
                summary = "Suspicious email from unknown sender attempting to collect credentials"
            elif threat_type == 'malware':
                summary = "Malicious executable detected attempting to establish C2 connection"
            elif threat_type == 'ddos':
                summary = "Unusual traffic spike detected from multiple sources"
            else:  # zero-day
                summary = "Unusual process behavior detected that may indicate zero-day exploit"
            
            threats.append({
                'id': f'threat_{i+1}',
                'type': threat_type,
                'summary': summary,
                'source': random.choice(['endpoint_protection', 'email_filter', 'network_monitor', 'firewall', 'ids']),
                'timestamp': (datetime.now() - timedelta(minutes=random.randint(1, 60))).isoformat(),
                'severity': random.choice(['low', 'medium', 'high', 'critical'])
            })
        
        with open(THREATS_FILE, 'w') as f:
            json.dump(threats, f, indent=2)
    
    if not os.path.exists(ACTIONS_FILE):
        actions = []
        action_types = ['Blocked', 'Quarantined', 'Monitored', 'Ignored', 'Mitigated']
        for i in range(20):
            action = random.choice(action_types)
            if action == 'Blocked':
                reward = random.uniform(0.7, 1.0)
            elif action == 'Quarantined':
                reward = random.uniform(0.6, 0.9)
            elif action == 'Monitored':
                reward = random.uniform(0.4, 0.7)
            elif action == 'Ignored':
                reward = random.uniform(0.1, 0.4)
            else:  # Mitigated
                reward = random.uniform(0.5, 0.8)
            
            actions.append({
                'id': f'action_{i+1}',
                'threat_id': f'threat_{random.randint(1, 20)}',
                'action': action,
                'confidence': random.uniform(0.5, 1.0),
                'reward': reward,
                'timestamp': (datetime.now() - timedelta(minutes=random.randint(1, 60))).isoformat()
            })
        
        with open(ACTIONS_FILE, 'w') as f:
            json.dump(actions, f, indent=2)

# Create sample data on startup
create_sample_data()

# Routes
@app.route('/api/threats', methods=['GET'])
def get_threats():
    """Get the latest threats."""
    try:
        with open(THREATS_FILE, 'r') as f:
            threats = json.load(f)
        
        # Sort by timestamp (newest first) and return the latest 20
        threats.sort(key=lambda x: x['timestamp'], reverse=True)
        return jsonify(threats[:20])
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/actions', methods=['GET'])
def get_actions():
    """Get the latest actions."""
    try:
        with open(ACTIONS_FILE, 'r') as f:
            actions = json.load(f)
        
        # Sort by timestamp (newest first) and return the latest 20
        actions.sort(key=lambda x: x['timestamp'], reverse=True)
        return jsonify(actions[:20])
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get statistics about threats and actions."""
    try:
        with open(THREATS_FILE, 'r') as f:
            threats = json.load(f)
        
        with open(ACTIONS_FILE, 'r') as f:
            actions = json.load(f)
        
        # Count threats by type
        threat_types = {}
        for threat in threats:
            threat_type = threat['type']
            if threat_type in threat_types:
                threat_types[threat_type] += 1
            else:
                threat_types[threat_type] = 1
        
        # Count actions by type
        action_types = {}
        for action in actions:
            action_type = action['action']
            if action_type in action_types:
                action_types[action_type] += 1
            else:
                action_types[action_type] = 1
        
        # Calculate average reward
        total_reward = sum(action['reward'] for action in actions)
        avg_reward = total_reward / len(actions) if actions else 0
        
        # Calculate average confidence
        total_confidence = sum(action['confidence'] for action in actions)
        avg_confidence = total_confidence / len(actions) if actions else 0
        
        return jsonify({
            'threat_types': threat_types,
            'action_types': action_types,
            'total_threats': len(threats),
            'total_actions': len(actions),
            'avg_reward': avg_reward,
            'avg_confidence': avg_confidence
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({'status': 'ok'})

# Serve the React app for any other routes
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True) 