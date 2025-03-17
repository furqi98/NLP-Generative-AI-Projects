# AI News Aggregator and LinkedIn Content Generator

## Overview
This project combines an AI news aggregator with a LinkedIn content generator. It scrapes AI-related news from various sources and then uses AI agents to create engaging LinkedIn posts based on the collected news.

## Features
- News aggregation from multiple sources (RSS feeds, Google News, Hacker News)
- Multi-agent approach for content generation:
  - Curator agent to select the most engaging news
  - Researcher agent to gather additional context
  - Writer agent to create the LinkedIn post

## Project Structure
```
ai_news_linkedin/
│
├── requirements.txt              # Dependencies
├── .env                          # Store API keys (create from .env.template)
│
├── news_aggregator/              # News aggregation module
│   ├── __init__.py
│   ├── scraper.py                # Contains the news scraping functionality
│   └── data_utils.py             # Utilities for data handling and saving
│
├── linkedin_generator/           # LinkedIn content generation module
│   ├── __init__.py
│   ├── agents/                   # Individual agents
│   │   ├── __init__.py
│   │   ├── curator.py            # Agent 1: Curates articles
│   │   ├── researcher.py         # Agent 2: Researches topics
│   │   └── writer.py             # Agent 3: Writes LinkedIn posts
│   └── system.py                 # Main orchestration system
│
└── main.py                       # Entry point
```

## Setup
1. Clone this repository
2. Install dependencies: `pip install -r requirements.txt`
3. Create a `.env` file from the `.env.template` and add your API keys

## Usage
- Run the news aggregator: `python main.py --mode scrape`
- Run the LinkedIn content generator: `python main.py --mode generate`
- Run both in sequence: `python main.py --mode all`

## API Keys Required
- Hugging Face API token - for language model access
- Tavily API key - for AI-optimized search functionality
