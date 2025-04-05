# SentinelMind Threat Intelligence Engine

A comprehensive threat intelligence system that aggregates and analyzes security threats from multiple sources.

## Features

- Fetches latest CVE data from NVD API
- Scrapes security-related posts from Reddit (r/netsec and r/cybersecurity)
- Classifies threats using BERT model
- Stores results in JSON format

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file with your credentials:
```
REDDIT_CLIENT_ID=your_client_id
REDDIT_CLIENT_SECRET=your_client_secret
REDDIT_USER_AGENT=your_user_agent
```

3. Run the main script:
```bash
python main.py
```

## Project Structure

- `main.py`: Entry point of the application
- `modules/`
  - `cve_fetcher.py`: Handles NVD API interactions
  - `reddit_scraper.py`: Manages Reddit data collection
  - `threat_classifier.py`: BERT-based threat classification
  - `data_storage.py`: Handles data persistence
- `data/`: Directory for storing output files 

# Reddit Security Scraper

A Python tool to scrape security-related posts from Reddit subreddits (r/netsec and r/cybersecurity).

## Features

- Fetches recent posts from r/netsec and r/cybersecurity
- Extracts key information: title, body, subreddit, author, date, etc.
- Configurable post limit
- Time-based filtering option
- Saves results to JSON

## Requirements

- Python 3.6+
- PRAW (Python Reddit API Wrapper)
- python-dotenv

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd <repository-directory>
```

2. Install dependencies:
```bash
pip install praw python-dotenv
```

3. Set up Reddit API credentials:
   - Go to https://www.reddit.com/prefs/apps
   - Click "Create another app..."
   - Select "script" as the application type
   - Fill in the required information
   - Copy the client ID and client secret

4. Create a `.env` file based on the `.env.example` template:
```bash
cp .env.example .env
```

5. Edit the `.env` file with your Reddit API credentials:
```
REDDIT_CLIENT_ID=your_client_id_here
REDDIT_CLIENT_SECRET=your_client_secret_here
REDDIT_USER_AGENT=your_app_name:v1.0 (by /u/your_username)
```

## Usage

### Basic Usage

```python
from reddit_scraper import RedditScraper

# Create scraper instance
scraper = RedditScraper()

# Get recent posts (default limit is 50)
posts = scraper.get_recent_posts()

# Print the number of posts fetched
print(f"Fetched {len(posts)} posts")
```

### Specify Post Limit

```python
# Get 20 recent posts
posts = scraper.get_recent_posts(limit=20)
```

### Get Posts by Timeframe

```python
# Get posts from the last 12 hours
posts = scraper.get_posts_by_timeframe(hours=12)
```

### Run the Example Script

```bash
python reddit_example.py
```

This will:
1. Fetch recent posts from both subreddits
2. Save them to a JSON file with a timestamp
3. Display a summary and example posts

## Output Format

Each post is returned as a dictionary with the following fields:

```python
{
    "title": "Post title",
    "body": "Post content",
    "subreddit": "netsec or cybersecurity",
    "author": "Username or [deleted]",
    "date": "ISO format date string",
    "url": "URL of the post",
    "score": 42,  # Upvotes
    "num_comments": 10,
    "permalink": "https://reddit.com/permalink/to/post"
}
```

## License

MIT 

# Cyber Security RL API

This API provides endpoints to access threat intelligence data and reinforcement learning agent decisions for a cyber security system.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the Flask app:
```bash
python app.py
```

The API will be available at `http://localhost:5000`.

## API Endpoints

### 1. Get Latest Threats

```
GET /threats
```

Returns the latest 20 threats from the threat intelligence data.

**Response:**
```json
{
  "status": "success",
  "count": 20,
  "total": 100,
  "threats": [
    {
      "source": "reddit",
      "type": "phishing",
      "summary": "Attempted S3 credential theft",
      "date": "2025-04-05"
    },
    ...
  ],
  "timestamp": "2023-11-15T12:34:56.789Z"
}
```

### 2. Get Latest Actions

```
GET /actions
```

Returns the last 20 RL agent decisions.

**Response:**
```json
{
  "status": "success",
  "count": 20,
  "total": 100,
  "actions": [
    {
      "timestamp": "2025-04-05T10:15:30",
      "threat_id": "threat_001",
      "action": "block",
      "confidence": 0.92,
      "reward": 1.0
    },
    ...
  ],
  "timestamp": "2023-11-15T12:34:56.789Z"
}
```

### 3. Get Statistics

```
GET /stats
```

Returns statistics about threats and actions.

**Response:**
```json
{
  "status": "success",
  "stats": {
    "threats": {
      "count": 100,
      "by_type": {
        "phishing": 30,
        "ransomware": 20,
        "sql_injection": 15,
        ...
      },
      "by_source": {
        "reddit": 25,
        "darkweb": 15,
        "github": 10,
        ...
      }
    },
    "actions": {
      "count": 100,
      "by_type": {
        "block": 40,
        "log": 35,
        "ignore": 25
      }
    },
    "timestamp": "2023-11-15T12:34:56.789Z"
  }
}
```

### 4. Health Check

```
GET /health
```

Simple health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2023-11-15T12:34:56.789Z"
}
```

## Data Files

The API uses two JSON files:

1. `intel_data.json` - Contains threat intelligence data
2. `actions_log.json` - Contains RL agent decisions

If these files don't exist, the API will create sample data files when started.

## CORS Support

CORS is enabled for all routes, allowing cross-origin requests from any domain.

## Error Handling

All endpoints return appropriate HTTP status codes and error messages in case of issues:

- 404: Resource not found
- 500: Server error

Error responses include a message and timestamp:

```json
{
  "status": "error",
  "message": "Error message here",
  "timestamp": "2023-11-15T12:34:56.789Z"
}
```

# Cyber Threat Action Explainer

This project uses LangChain and OpenAI to generate explanations for cybersecurity decisions. It provides clear, technical reasoning for why specific actions were taken in response to cyber threats.

## Features

- Explains why specific actions (Block, Quarantine, Monitor, etc.) were taken in response to cyber threats
- Uses LangChain's prompt templating for consistent, high-quality explanations
- Supports multiple threat types (ransomware, phishing, malware, DDoS, zero-day)
- Provides technical reasoning based on security best practices

## Setup

1. Clone this repository
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the project root with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

## Usage

### Running the Example

To run the example with predefined threats and actions:

```
python threat_explainer.py
```

Or simply double-click the `run_threat_explainer.bat` file.

### Using in Your Own Code

```python
from threat_explainer import explain_threat_action

# Define a threat
threat = {
    "type": "ransomware",
    "summary": "Detected encryption of multiple files in short time",
    "source": "endpoint_protection"
}

# Define an action
action = "Blocked"

# Get the explanation
explanation = explain_threat_action(threat, action)
print(explanation)
```

## Customization

### Using a Different LLM

You can modify the script to use a HuggingFace model instead of OpenAI:

```python
from langchain.llms import HuggingFaceHub

llm = HuggingFaceHub(
    repo_id="google/flan-t5-large",
    model_kwargs={"temperature": 0.2, "max_length": 512}
)
```

### Modifying the Prompt

The prompt template can be customized by modifying the `PromptTemplate.from_template()` call in the script:

```python
prompt_template = PromptTemplate.from_template(
    "A cybersecurity AI took the action: {action}.\n\n"
    "Threat type: {threat_type}\n"
    "Summary: {summary}\n"
    "Explain why this action is reasonable from a cybersecurity point of view."
)
```

## Example Output

```
Threat Information:
Type: ransomware
Summary: Detected encryption of multiple files in short time
Source: reddit
Action: Blocked

Explanation:
Blocking this ransomware activity was the appropriate immediate response to prevent further file encryption and potential data loss. The rapid encryption of multiple files is a clear indicator of active ransomware execution, which requires immediate containment to limit the scope of the attack. This action follows the principle of least privilege and the security best practice of isolating compromised systems to prevent lateral movement and protect unaffected resources.
```

# Cyber Brain Dashboard

A modern cybersecurity dashboard that displays threats and actions taken by the system, with AI-powered explanations.

![Dashboard Screenshot](dashboard/screenshots/dashboard.png)

## Features

- Real-time threat monitoring
- AI-powered action explanations
- Interactive threat visualization
- Standalone and server-based versions
- Modern, responsive UI
- RESTful API backend

## Prerequisites

- Python 3.8 or higher
- Node.js 14 or higher
- npm (comes with Node.js)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/cyber-brain.git
cd cyber-brain
```

2. Set up the Python environment:
```bash
cd dashboard
py -m venv venv
.\venv\Scripts\activate  # On Windows
source venv/bin/activate  # On Unix/MacOS
py -m pip install -r requirements.txt
```

3. Set up the frontend:
```bash
cd frontend
npm install
```

4. Create environment files:
```bash
# In the dashboard directory
cp .env.example .env
# Edit .env with your OpenAI API key
```

## Running the Application

### Option 1: Standalone Version (No Server Required)

1. Open `dashboard/standalone_dashboard.html` in your browser
2. No setup required - works immediately!

### Option 2: Full Interactive Version

1. Start the backend server:
```bash
cd dashboard
.\venv\Scripts\activate  # On Windows
source venv/bin/activate  # On Unix/MacOS
py backend/app.py
```

2. In a new terminal, start the frontend:
```bash
cd dashboard/frontend
npm start
```

3. Open your browser and navigate to:
```
http://localhost:3001
```

## Project Structure

```
cyber-brain/
├── dashboard/
│   ├── backend/
│   │   ├── app.py
│   │   └── ...
│   ├── frontend/
│   │   ├── src/
│   │   ├── package.json
│   │   └── ...
│   ├── standalone_dashboard.html
│   ├── requirements.txt
│   └── .env.example
├── README.md
└── .gitignore
```

## API Documentation

The backend API is available at `http://localhost:5000/api/` with the following endpoints:

- `GET /api/health` - Check API health
- `GET /api/threats` - Get all threats
- `GET /api/threats/<id>` - Get specific threat
- `GET /api/actions` - Get all actions
- `GET /api/actions/<id>` - Get specific action

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- OpenAI for the GPT API
- React.js team for the frontend framework
- Flask team for the backend framework 