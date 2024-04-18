# YouTube Comment Scraper

## Overview

This project integrates advanced NLP and AI to enhance user engagement with YouTube content. Key components include:

- **`Scraper.py`**: Scrapes YouTube for video IDs based on user query.
  
- **`Relevant_comment.py`**: Processes video comments using BERT and SpaCy to extract relevant responses.

- **`qa.py`**: Interacts with the AI21 language model to provide context-aware responses.

- **`ui.py`**: A Flask web app that integrates all components and dynamically updates the UI with relevant images from the Pexels API.

## Use Cases

- **Education**: Extract discussions and questions from video lectures.
  
- **Content Creation**: Gain insights for better engagement and audience sentiment analysis.

- **Research**: Automate and refine data collection and analysis on social media and user interactions.

## Prerequisites

Before running the project, ensure you have the following:

- YouTube API Key
- AI21 API Key and Model URL
- File paths for any local files you need to reference

## Setup

1. **Replace API Keys and URLs**:
   - Open `scrapper.py` and replace `api_key = 'YOUR API KEY'` with your YouTube API key.
   - Open `qa.py` and replace `url = "YOUR URL"` with your AI21 website model URL and `api_key = "YOUR API KEY"` with your AI21 API key.

2. **Update File Paths**:
   - Replace all placeholder file paths in the scripts with your actual file paths.

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt

## Usage

1. **Run the Flask Application**:
   ```bash
   python ui.py
   ```
   Your Flask application will start running, and you should see an output similar to:
   ```plaintext
   * Serving Flask app 'ui'
   * Debug mode: on
   WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
   * Running on http://127.0.0.1:5000
   Press CTRL+C to quit
   * Restarting with stat
   * Debugger is active!
   * Debugger PIN: 325-090-574
   ```
2. **Access the Application**:
Open a web browser and navigate to `http://127.0.0.1:5000` to use the application locally.
