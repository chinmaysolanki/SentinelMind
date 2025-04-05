import random
import ipaddress
from typing import Dict, List, Tuple, Optional
import hashlib
import json
from datetime import datetime

# Define threat severity levels
THREAT_SEVERITY = {
    "critical": 1.0,
    "high": 0.8,
    "medium": 0.6,
    "low": 0.4,
    "info": 0.2
}

# Define threat types and their associated protocols
THREAT_PROTOCOLS = {
    "phishing": 80,  # HTTP
    "malware": 443,  # HTTPS
    "ransomware": 443,  # HTTPS
    "data_exfiltration": 443,  # HTTPS
    "brute_force": 22,  # SSH
    "ddos": 53,  # DNS
    "sql_injection": 3306,  # MySQL
    "xss": 80,  # HTTP
    "credential_theft": 3389,  # RDP
    "apt": 443,  # HTTPS
    "zero_day": 443,  # HTTPS
    "default": 0  # Unknown protocol
}

# Define threat sources and their associated IP ranges
THREAT_SOURCES = {
    "reddit": "10.0.0.0/8",
    "twitter": "172.16.0.0/12",
    "github": "192.168.0.0/16",
    "darkweb": "10.10.0.0/16",
    "default": "0.0.0.0/0"
}

def _determine_threat_severity(threat_type: str, summary: str) -> float:
    """
    Determine the severity of a threat based on its type and summary.
    
    Args:
        threat_type: The type of threat
        summary: A summary of the threat
        
    Returns:
        A severity score between 0.0 and 1.0
    """
    # Check for critical keywords in summary
    critical_keywords = ["critical", "emergency", "immediate", "severe", "exploit", "zero-day"]
    high_keywords = ["high", "urgent", "important", "significant", "breach", "compromise"]
    medium_keywords = ["medium", "moderate", "potential", "suspicious", "anomaly"]
    low_keywords = ["low", "minor", "possible", "unusual"]
    
    # Check threat type severity
    if threat_type in ["apt", "ransomware", "zero_day"]:
        return THREAT_SEVERITY["critical"]
    elif threat_type in ["malware", "data_exfiltration", "credential_theft"]:
        return THREAT_SEVERITY["high"]
    elif threat_type in ["phishing", "brute_force", "sql_injection"]:
        return THREAT_SEVERITY["medium"]
    elif threat_type in ["ddos", "xss"]:
        return THREAT_SEVERITY["low"]
    
    # Check summary keywords
    summary_lower = summary.lower()
    for keyword in critical_keywords:
        if keyword in summary_lower:
            return THREAT_SEVERITY["critical"]
    
    for keyword in high_keywords:
        if keyword in summary_lower:
            return THREAT_SEVERITY["high"]
    
    for keyword in medium_keywords:
        if keyword in summary_lower:
            return THREAT_SEVERITY["medium"]
    
    for keyword in low_keywords:
        if keyword in summary_lower:
            return THREAT_SEVERITY["low"]
    
    # Default to medium if no specific indicators
    return THREAT_SEVERITY["medium"]

def _generate_ip_from_range(ip_range: str) -> str:
    """
    Generate a random IP address from a given CIDR range.
    
    Args:
        ip_range: A CIDR notation IP range (e.g., "192.168.0.0/16")
        
    Returns:
        A random IP address from the range
    """
    network = ipaddress.ip_network(ip_range)
    return str(random.choice(list(network.hosts())))

def _determine_packet_size(threat_type: str, severity: float) -> int:
    """
    Determine a realistic packet size based on threat type and severity.
    
    Args:
        threat_type: The type of threat
        severity: The severity of the threat (0.0 to 1.0)
        
    Returns:
        A packet size in bytes
    """
    # Base packet sizes for different threat types
    base_sizes = {
        "phishing": 1500,
        "malware": 2000,
        "ransomware": 2500,
        "data_exfiltration": 3000,
        "brute_force": 100,
        "ddos": 500,
        "sql_injection": 800,
        "xss": 1200,
        "credential_theft": 1000,
        "apt": 3500,
        "zero_day": 4000,
        "default": 1000
    }
    
    # Get base size for the threat type
    base_size = base_sizes.get(threat_type, base_sizes["default"])
    
    # Adjust size based on severity (higher severity = larger packets)
    adjusted_size = int(base_size * (0.5 + severity))
    
    # Add some randomness (±20%)
    variation = random.uniform(0.8, 1.2)
    final_size = int(adjusted_size * variation)
    
    # Ensure size is within reasonable bounds
    return max(64, min(final_size, 9000))

def _determine_protocol(threat_type: str) -> int:
    """
    Determine the protocol number based on threat type.
    
    Args:
        threat_type: The type of threat
        
    Returns:
        A protocol number
    """
    return THREAT_PROTOCOLS.get(threat_type, THREAT_PROTOCOLS["default"])

def _determine_source_ip(source: str) -> str:
    """
    Determine a source IP based on the threat source.
    
    Args:
        source: The source of the threat
        
    Returns:
        A source IP address
    """
    ip_range = THREAT_SOURCES.get(source, THREAT_SOURCES["default"])
    return _generate_ip_from_range(ip_range)

def _determine_destination_ip(threat_type: str) -> str:
    """
    Determine a destination IP based on the threat type.
    
    Args:
        threat_type: The type of threat
        
    Returns:
        A destination IP address
    """
    # For internal network simulation
    internal_ranges = [
        "192.168.1.0/24",  # Internal network
        "10.0.0.0/8",      # Corporate network
        "172.16.0.0/12"    # DMZ
    ]
    
    # Select a range based on threat type
    if threat_type in ["phishing", "malware", "ransomware"]:
        # These typically target end users
        return _generate_ip_from_range("192.168.1.0/24")
    elif threat_type in ["brute_force", "sql_injection"]:
        # These typically target servers
        return _generate_ip_from_range("10.0.0.0/8")
    elif threat_type in ["ddos", "apt"]:
        # These typically target infrastructure
        return _generate_ip_from_range("172.16.0.0/12")
    else:
        # Default to a random internal range
        return _generate_ip_from_range(random.choice(internal_ranges))

def convert_threat_to_env_input(threat: Dict) -> List[float]:
    """
    Convert a threat dictionary from the Threat Intelligence Engine into a state vector
    for the RL environment.
    
    Args:
        threat: A dictionary containing threat information
        
    Returns:
        A list representing the state vector [src_ip, dst_ip, protocol, packet_size, is_threat]
    """
    # Extract threat information
    source = threat.get("source", "unknown")
    threat_type = threat.get("type", "unknown").lower()
    summary = threat.get("summary", "")
    date = threat.get("date", datetime.now().strftime("%Y-%m-%d"))
    
    # Determine threat severity
    severity = _determine_threat_severity(threat_type, summary)
    
    # Determine if this is a threat (severity > 0.3)
    is_threat = severity > 0.3
    
    # Generate IP addresses
    src_ip = _determine_source_ip(source)
    dst_ip = _determine_destination_ip(threat_type)
    
    # Convert IP addresses to numeric format (first octet)
    src_ip_numeric = float(src_ip.split('.')[0])
    dst_ip_numeric = float(dst_ip.split('.')[0])
    
    # Determine protocol and packet size
    protocol = _determine_protocol(threat_type)
    packet_size = _determine_packet_size(threat_type, severity)
    
    # Create the state vector
    state_vector = [
        src_ip_numeric,
        dst_ip_numeric,
        float(protocol),
        float(packet_size),
        1.0 if is_threat else 0.0
    ]
    
    return state_vector

def convert_threats_batch(threats: List[Dict]) -> List[List[float]]:
    """
    Convert a batch of threat dictionaries to environment state vectors.
    
    Args:
        threats: A list of threat dictionaries
        
    Returns:
        A list of state vectors
    """
    return [convert_threat_to_env_input(threat) for threat in threats]

# Example usage
if __name__ == "__main__":
    # Example threat
    example_threat = {
        "source": "reddit",
        "type": "phishing",
        "summary": "Attempted S3 credential theft",
        "date": "2025-04-05"
    }
    
    # Convert to environment input
    state_vector = convert_threat_to_env_input(example_threat)
    
    print("Example Threat:")
    print(json.dumps(example_threat, indent=2))
    print("\nConverted State Vector:")
    print(f"[src_ip, dst_ip, protocol, packet_size, is_threat] = {state_vector}")
    
    # Example batch conversion
    example_threats = [
        {
            "source": "reddit",
            "type": "phishing",
            "summary": "Attempted S3 credential theft",
            "date": "2025-04-05"
        },
        {
            "source": "darkweb",
            "type": "ransomware",
            "summary": "Critical zero-day exploit detected",
            "date": "2025-04-06"
        },
        {
            "source": "github",
            "type": "sql_injection",
            "summary": "Potential SQL injection attempt",
            "date": "2025-04-07"
        }
    ]
    
    state_vectors = convert_threats_batch(example_threats)
    
    print("\nBatch Conversion Results:")
    for i, (threat, vector) in enumerate(zip(example_threats, state_vectors)):
        print(f"\nThreat {i+1}: {threat['type']} from {threat['source']}")
        print(f"State Vector: {vector}") 