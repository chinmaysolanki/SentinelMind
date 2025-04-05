from faker import Faker
import random
import json
from datetime import datetime, timedelta

# Initialize Faker
fake = Faker()

# Define threat types and their templates
threat_types = {
    "phishing": [
        "A fake {company} login page is being used to steal user credentials.",
        "Suspicious email from {sender} attempting to collect {company} account information.",
        "Phishing campaign targeting {company} employees with fake {service} notifications.",
        "Malicious link in email purporting to be from {company} IT department.",
        "Fake {company} invoice attachment containing credential harvesting form.",
        "Suspicious domain {domain} mimicking {company} website for credential theft.",
        "Email campaign using {company} branding to trick users into revealing passwords.",
        "Fake {company} password reset request from {sender}.",
        "Suspicious {company} document sharing notification with malicious link.",
        "Phishing attempt using compromised {company} email address to target other employees."
    ],
    "malware": [
        "Malicious executable detected in {file_path} attempting to establish C2 connection.",
        "Suspicious PowerShell command execution detected from {ip_address}.",
        "Malware signature {signature} detected in file downloaded from {domain}.",
        "Suspicious process {process} attempting to modify system files.",
        "Malware attempting to disable security services and establish persistence.",
        "Suspicious network connection to known C2 server {ip_address}.",
        "Malware attempting to exfiltrate data to {domain}.",
        "Suspicious file {file_name} with high entropy indicating possible encryption.",
        "Malware attempting to create scheduled task for persistence.",
        "Suspicious DLL injection detected from process {process}."
    ],
    "ransomware": [
        "Ransomware activity detected encrypting files in {directory}.",
        "Suspicious file extensions being changed to {extension} indicating ransomware.",
        "Ransomware note {note_name} detected in multiple directories.",
        "Suspicious file operations detected in {directory} with high I/O rate.",
        "Ransomware attempting to delete shadow copies to prevent recovery.",
        "Suspicious process {process} accessing and modifying multiple files rapidly.",
        "Ransomware attempting to encrypt network shares from {ip_address}.",
        "Suspicious file operations detected with pattern matching known ransomware.",
        "Ransomware attempting to disable backup services to prevent recovery.",
        "Suspicious network connection to known ransomware C2 server {ip_address}."
    ],
    "ddos": [
        "DDoS attack detected targeting {service} from {ip_count} unique IP addresses.",
        "Unusual traffic spike detected from {ip_count} sources targeting {service}.",
        "DDoS attack using {attack_type} technique targeting {service}.",
        "Suspicious UDP flood detected from {ip_count} sources to {ip_address}.",
        "DDoS attack attempting to overwhelm {service} with {request_count} requests per second.",
        "Suspicious SYN flood detected from {ip_count} sources targeting {service}.",
        "DDoS attack using botnet with {ip_count} compromised hosts targeting {service}.",
        "Unusual traffic pattern detected from {ip_count} sources indicating DDoS preparation.",
        "DDoS attack targeting {service} with {bandwidth} bandwidth consumption.",
        "Suspicious HTTP flood detected from {ip_count} sources targeting {service}."
    ],
    "zero-day": [
        "Unusual process behavior detected that may indicate zero-day exploit.",
        "Suspicious memory access pattern detected that may indicate zero-day vulnerability.",
        "Unknown exploit attempting to gain elevated privileges on {system}.",
        "Suspicious network traffic pattern that may indicate zero-day exploit.",
        "Unusual system call sequence detected that may indicate zero-day attack.",
        "Suspicious file operation pattern that may indicate zero-day exploit.",
        "Unknown process attempting to access sensitive system resources.",
        "Suspicious network connection to {ip_address} using unknown protocol.",
        "Unusual system behavior detected that may indicate zero-day vulnerability.",
        "Suspicious process attempting to modify system configuration using unknown technique."
    ]
}

# Companies and services for generating realistic data
companies = [
    "Microsoft", "Google", "Amazon", "Apple", "Facebook", "Netflix", "Adobe", 
    "Salesforce", "Oracle", "IBM", "Intel", "Cisco", "HP", "Dell", "Samsung",
    "Sony", "Nintendo", "EA", "Ubisoft", "Activision", "Spotify", "Twitter",
    "LinkedIn", "Uber", "Lyft", "Airbnb", "PayPal", "Stripe", "Square", "Shopify"
]

services = [
    "email", "cloud storage", "document sharing", "password reset", "account verification",
    "invoice", "payment", "subscription", "security alert", "login", "authentication",
    "file sharing", "collaboration", "project management", "customer support", "billing",
    "account management", "profile update", "security settings", "notification"
]

# Generate a random threat summary
def generate_threat_summary(threat_type):
    template = random.choice(threat_types[threat_type])
    
    # Replace placeholders with realistic data
    summary = template.format(
        company=random.choice(companies),
        sender=fake.email(),
        service=random.choice(services),
        domain=fake.domain_name(),
        file_path=fake.file_path(),
        ip_address=fake.ipv4(),
        signature=fake.uuid4(),
        process=fake.word() + ".exe",
        file_name=fake.word() + ".exe",
        directory=fake.directory_path(),
        extension="." + fake.file_extension()[1:],
        note_name="README.txt",
        ip_count=random.randint(100, 10000),
        request_count=random.randint(1000, 100000),
        attack_type=random.choice(["UDP flood", "SYN flood", "HTTP flood", "ICMP flood", "Slowloris"]),
        bandwidth=str(random.randint(100, 1000)) + " Mbps",
        system=random.choice(["Windows", "Linux", "macOS", "iOS", "Android"])
    )
    
    return summary

# Generate multiple summaries for each threat type
def generate_all_summaries(count=5):
    all_summaries = {}
    
    for threat_type in threat_types:
        summaries = [generate_threat_summary(threat_type) for _ in range(count)]
        all_summaries[threat_type] = summaries
    
    return all_summaries

# Generate and print summaries
if __name__ == "__main__":
    summaries = generate_all_summaries()
    
    print("Realistic Threat Summaries Generated with Faker:")
    print("===============================================")
    
    for threat_type, threat_summaries in summaries.items():
        print(f"\n{threat_type.upper()} THREATS:")
        print("-" * 50)
        for i, summary in enumerate(threat_summaries, 1):
            print(f"{i}. {summary}")
    
    # Save to JSON file
    with open("threat_summaries.json", "w") as f:
        json.dump(summaries, f, indent=2)
    
    print("\nSummaries have been saved to 'threat_summaries.json'") 