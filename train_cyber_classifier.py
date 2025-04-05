import torch
from torch.utils.data import Dataset, DataLoader
from transformers import AutoTokenizer, AutoModelForSequenceClassification, AdamW
from transformers import get_linear_schedule_with_warmup
import numpy as np
from tqdm import tqdm
import json
import os
from typing import List, Dict, Any
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Define cybersecurity categories
CATEGORIES = {
    0: "Vulnerability",
    1: "Malware",
    2: "Phishing",
    3: "Info",
    4: "Zero-day"
}

class CyberSecurityDataset(Dataset):
    def __init__(self, texts: List[str], labels: List[int], tokenizer, max_length: int = 512):
        this.texts = texts
        this.labels = labels
        this.tokenizer = tokenizer
        this.max_length = max_length

    def __len__(self):
        return len(this.texts)

    def __getitem__(self, idx):
        text = this.texts[idx]
        label = this.labels[idx]

        # Tokenize text
        encoding = this.tokenizer(
            text,
            truncation=True,
            padding="max_length",
            max_length=this.max_length,
            return_tensors="pt"
        )

        return {
            "input_ids": encoding["input_ids"].flatten(),
            "attention_mask": encoding["attention_mask"].flatten(),
            "labels": torch.tensor(label, dtype=torch.long)
        }

def create_dummy_data() -> tuple:
    """
    Create dummy training data for demonstration purposes.
    In a real scenario, you would load your actual training data.
    """
    # Dummy examples for each category
    dummy_data = [
        # Vulnerability examples
        ("Critical SQL injection vulnerability found in popular CMS", 0),
        ("Buffer overflow in network protocol implementation", 0),
        ("Cross-site scripting (XSS) vulnerability in web application", 0),
        
        # Malware examples
        ("New ransomware variant targeting healthcare sector", 1),
        ("Trojan horse discovered in software supply chain", 1),
        ("Botnet using IoT devices for DDoS attacks", 1),
        
        # Phishing examples
        ("Phishing campaign impersonating financial institutions", 2),
        ("Credential harvesting attack via fake login page", 2),
        ("Spear phishing targeting executive staff", 2),
        
        # Info examples
        ("Security best practices for remote work", 3),
        ("How to implement multi-factor authentication", 3),
        ("Guide to secure password management", 3),
        
        # Zero-day examples
        ("New zero-day exploit in Windows kernel", 4),
        ("Unpatched vulnerability in critical infrastructure", 4),
        ("Zero-day attack vector discovered in web servers", 4),
    ]
    
    # Split into texts and labels
    texts = [item[0] for item in dummy_data]
    labels = [item[1] for item in dummy_data]
    
    return texts, labels

def train_model(
    model_name: str = "bert-base-uncased",
    num_epochs: int = 5,
    batch_size: int = 8,
    learning_rate: float = 2e-5,
    max_length: int = 512
):
    """
    Train the BERT model on cybersecurity text classification
    """
    # Set device
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    logger.info(f"Using device: {device}")
    
    # Load tokenizer and model
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(
        model_name,
        num_labels=len(CATEGORIES)
    ).to(device)
    
    # Create dummy dataset
    texts, labels = create_dummy_data()
    dataset = CyberSecurityDataset(texts, labels, tokenizer, max_length)
    dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)
    
    # Setup optimizer and scheduler
    optimizer = AdamW(model.parameters(), lr=learning_rate)
    total_steps = len(dataloader) * num_epochs
    scheduler = get_linear_schedule_with_warmup(
        optimizer,
        num_warmup_steps=0,
        num_training_steps=total_steps
    )
    
    # Training loop
    logger.info("Starting training...")
    model.train()
    
    for epoch in range(num_epochs):
        logger.info(f"Epoch {epoch + 1}/{num_epochs}")
        
        for batch in tqdm(dataloader, desc=f"Training epoch {epoch + 1}"):
            # Move batch to device
            input_ids = batch["input_ids"].to(device)
            attention_mask = batch["attention_mask"].to(device)
            labels = batch["labels"].to(device)
            
            # Forward pass
            outputs = model(
                input_ids=input_ids,
                attention_mask=attention_mask,
                labels=labels
            )
            
            loss = outputs.loss
            logits = outputs.logits
            
            # Backward pass
            loss.backward()
            
            # Clip gradients
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            
            # Update weights
            optimizer.step()
            scheduler.step()
            optimizer.zero_grad()
            
        logger.info(f"Epoch {epoch + 1} completed. Loss: {loss.item():.4f}")
    
    # Save the model
    output_dir = "cyber_classifier_model"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    model.save_pretrained(output_dir)
    tokenizer.save_pretrained(output_dir)
    
    # Save category mapping
    with open(os.path.join(output_dir, "categories.json"), "w") as f:
        json.dump(CATEGORIES, f)
        
    logger.info(f"Model saved to {output_dir}")
    
    return model, tokenizer

if __name__ == "__main__":
    train_model() 