# Job Search App 🤖

A Flask web app that searches for remote jobs based on your skills and automatically generates professional application emails using Claude AI.

## What it does

- Enter your skills in the search box (e.g. python, flask, api)
- Fetches matching remote jobs from Remotive API
- Ranks jobs by skill match percentage
- Generates a personalized application email for each job using Claude AI
- Shows everything in a clean web interface

## Tools and Technologies

- Python
- Flask
- Claude AI (Anthropic)
- Remotive API
- python-dotenv

## Setup

1. Clone the repo
2. Create a `.env` file with your `ANTHROPIC_API_KEY`
3. Run `pip install flask anthropic requests python-dotenv`
4. Run `python job_app.py`
5. Open `http://127.0.0.1:5000`

## Built by

Araj Sahi — Python Developer based in Toronto 🇨🇦
github.com/arajsahi
