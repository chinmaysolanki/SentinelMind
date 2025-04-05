# SentinelMind Threat Intelligence Pipeline

A comprehensive pipeline that collects threat data from multiple sources, classifies it using BERT, and saves the results in a standardized format.

## Features

- **Data Collection**:
  - Fetches latest CVE data from NVD API
  - Scrapes security-related posts from Reddit (r/netsec and r/cybersecurity)
  
- **Threat Classification**:
  - Uses BERT model to classify threats into categories
  - Provides confidence scores for classifications
  
- **Data Storage**:
  - Saves results in a standardized JSON format
  - Includes source, type, summary, and date for each threat

## Requirements

- Python 3.6+
- Dependencies listed in requirements.txt
- Reddit API credentials (for Reddit scraping)

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up Reddit API credentials in `.env` file:
```
REDDIT_CLIENT_ID=your_client_id
REDDIT_CLIENT_SECRET=your_client_secret
REDDIT_USER_AGENT=your_user_agent
```

## Usage

Run the pipeline with:
```bash
python pipeline.py
```

This will:
1. Collect threat data from NVD and Reddit
2. Classify the threats using BERT
3. Save the results to a JSON file in the `data` directory
4. Display a summary of the collected threats

## Output Format

The pipeline saves threats in the following JSON format:

```json
[
  {
    "source": "reddit",
    "type": "phishing",
    "summary": "Someone is using AWS S3 buckets to steal credentials",
    "date": "2023-04-05"
  },
  {
    "source": "nvd",
    "type": "vulnerability",
    "summary": "CVE-2023-1234: Critical SQL injection vulnerability",
    "date": "2023-04-04"
  }
]
```

## Project Structure

- `pipeline.py`: Main pipeline script
- `modules/`:
  - `cve_fetcher.py`: Fetches CVE data from NVD
  - `reddit_scraper.py`: Scrapes Reddit for security posts
  - `threat_classifier.py`: BERT-based threat classification
  - `data_storage.py`: Handles data persistence
- `data/`: Directory for storing output files 