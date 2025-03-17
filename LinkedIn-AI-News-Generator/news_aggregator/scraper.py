"""
AI News Aggregator - Scraper Module
Fetches AI news from multiple sources and saves them to CSV and Markdown files
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timedelta
import time
import random
import feedparser
import os
import sys

# Try importing GoogleNews
try:
    from GoogleNews import GoogleNews
    google_news_available = True
except ImportError:
    print("GoogleNews import failed. Will skip Google News sources.")
    google_news_available = False

# Try importing newspaper with error handling
try:
    from newspaper import Article
    newspaper_available = True
except ImportError:
    print("Newspaper3k import failed. Will skip article content extraction.")
    newspaper_available = False

    # Define a dummy ArticleException for compatibility
    class ArticleException(Exception):
        pass
else:
    # If import succeeded, get the exception class too
    from newspaper.article import ArticleException

from news_aggregator.data_utils import save_to_csv, save_to_markdown


def fetch_from_rss_feeds():
    """Fetch AI news from various tech/AI RSS feeds"""

    # List of AI and tech RSS feeds
    rss_feeds = [
        "https://www.technologyreview.com/topic/artificial-intelligence/feed",
        "https://www.artificialintelligence-news.com/feed/",
        "https://venturebeat.com/category/ai/feed/",
        "https://feeds.feedburner.com/aisearch",
        "https://machinelearnings.co/feed",
        "https://www.marktechpost.com/category/artificial-intelligence/feed/",
        "https://www.reddit.com/r/artificial/.rss",
        "https://www.reddit.com/r/MachineLearning/.rss"
    ]

    all_articles = []

    for feed_url in rss_feeds:
        try:
            print(f"Fetching from: {feed_url}")
            feed = feedparser.parse(feed_url)

            # Extract domain for source attribution
            domain = feed_url.split('/')[2]

            for entry in feed.entries[:10]:  # Get up to 10 recent entries per feed
                # Extract publication date
                if hasattr(entry, 'published_parsed') and entry.published_parsed:
                    try:
                        pub_date = datetime(*entry.published_parsed[:6])
                    except:
                        pub_date = datetime.now()  # Default to current time if parsing fails
                else:
                    pub_date = datetime.now()  # Default to current time if no date found

                # Extract summary
                summary = ""
                if hasattr(entry, 'summary'):
                    summary = entry.summary
                elif hasattr(entry, 'description'):
                    summary = entry.description
                else:
                    summary = "No summary available"

                # Clean up summary (remove HTML tags)
                try:
                    summary = BeautifulSoup(summary, "html.parser").get_text()
                except:
                    pass

                # Only include recent articles (last 7 days)
                if pub_date > (datetime.now() - timedelta(days=7)):
                    article_data = {
                        'title': entry.title,
                        'date': pub_date,
                        'source': domain,
                        'url': entry.link,
                        'summary': summary[:500] + "..." if len(summary) > 500 else summary
                    }
                    all_articles.append(article_data)

            # Be nice to servers
            time.sleep(random.uniform(1, 3))

        except Exception as e:
            print(f"Error fetching from {feed_url}: {str(e)}")

    return all_articles


def fetch_from_google_news():
    """Fetch AI news from Google News"""
    if not google_news_available:
        print("Skipping Google News (import failed)")
        return []

    # List of search terms
    search_terms = [
        "artificial intelligence",
        "machine learning",
        "deep learning",
        "GPT",
        "AI research",
        "computer vision",
        "LLM"
    ]

    all_articles = []

    for term in search_terms:
        try:
            print(f"Searching Google News for: {term}")

            # Configure GoogleNews
            googlenews = GoogleNews(period='7d')
            googlenews.search(term)
            results = googlenews.results()

            # Process results
            for item in results[:5]:  # Top 5 results per term
                # Get the date with fallback
                try:
                    if isinstance(item.get('datetime'), datetime):
                        item_date = item.get('datetime')
                    else:
                        item_date = datetime.now()
                except:
                    item_date = datetime.now()

                article_data = {
                    'title': item.get('title', 'No title'),
                    'date': item_date,
                    'source': item.get('media', 'Google News'),
                    'url': item.get('link', ''),
                    'summary': item.get('desc', 'No summary available')
                }
                all_articles.append(article_data)

            # Clear results for next search
            googlenews.clear()

            # Be nice to servers
            time.sleep(random.uniform(1, 3))

        except Exception as e:
            print(f"Error fetching Google News for {term}: {str(e)}")

    return all_articles


def fetch_from_hackernews():
    """Fetch AI-related news from Hacker News"""
    try:
        print("Fetching from Hacker News...")
        response = requests.get("https://hn.algolia.com/api/v1/search?query=AI%20OR%20artificial%20intelligence%20OR%20machine%20learning&tags=story&numericFilters=created_at_i>1577836800")
        data = response.json()

        all_articles = []
        for hit in data.get('hits', [])[:20]:  # Get up to 20 stories
            # Convert timestamp to datetime
            try:
                created_at = datetime.fromtimestamp(hit.get('created_at_i', 0))
            except:
                created_at = datetime.now()

            # Only include recent articles (last 7 days)
            if created_at > (datetime.now() - timedelta(days=7)):
                article_data = {
                    'title': hit.get('title', 'No title'),
                    'date': created_at,
                    'source': 'Hacker News',
                    'url': hit.get('url', ''),
                    'summary': f"Points: {hit.get('points', 0)} | Comments: {hit.get('num_comments', 0)}"
                }
                all_articles.append(article_data)

        return all_articles
    except Exception as e:
        print(f"Error fetching from Hacker News: {str(e)}")
        return []


def extract_article_content(url):
    """Extract the main content of an article using newspaper3k"""
    if not newspaper_available:
        return {
            'text': "Content extraction not available (newspaper3k import failed)",
            'keywords': [],
            'authors': []
        }

    try:
        article = Article(url)
        article.download()
        article.parse()
        return {
            'text': article.text,
            'keywords': article.keywords,
            'authors': article.authors
        }
    except ArticleException as e:
        print(f"Error extracting article content from {url}: {str(e)}")
        return {
            'text': "Content extraction failed",
            'keywords': [],
            'authors': []
        }
    except Exception as e:
        print(f"Unexpected error extracting content from {url}: {str(e)}")
        return {
            'text': "Content extraction failed",
            'keywords': [],
            'authors': []
        }


def remove_duplicates(articles):
    """Remove duplicate articles based on title similarity"""
    unique_articles = []
    titles = set()

    for article in articles:
        # Create a simplified version of the title for comparison
        try:
            simple_title = ''.join(e.lower() for e in article['title'] if e.isalnum())
        except:
            # If there's any error processing the title, use a fallback
            simple_title = str(random.randint(10000, 99999))

        # Check if we've seen this title before
        if simple_title not in titles and len(simple_title) > 10:
            titles.add(simple_title)
            unique_articles.append(article)

    return unique_articles


def main(output_dir='.'):
    """Main function to run the news aggregator"""
    print("Starting AI News Aggregator...")

    # Collect articles from different sources
    print("\n1. Fetching from RSS feeds...")
    rss_articles = fetch_from_rss_feeds()

    print(f"\n2. Fetching from Google News...")
    try:
        google_articles = fetch_from_google_news()
    except Exception as e:
        print(f"Error with Google News: {str(e)}")
        google_articles = []

    print(f"\n3. Fetching from Hacker News...")
    try:
        hn_articles = fetch_from_hackernews()
    except Exception as e:
        print(f"Error with Hacker News: {str(e)}")
        hn_articles = []

    # Combine all articles
    all_articles = rss_articles + google_articles + hn_articles

    # Remove duplicates
    print("\n4. Removing duplicate articles...")
    unique_articles = remove_duplicates(all_articles)

    if unique_articles:
        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)
        
        # Save as CSV
        csv_file = os.path.join(output_dir, 'ai_news.csv')
        save_to_csv(unique_articles, csv_file)

        # Save as Markdown for better readability
        md_file = os.path.join(output_dir, 'ai_news.md')
        save_to_markdown(unique_articles, md_file)

        print(f"\nTotal articles fetched: {len(unique_articles)}")
        print(f"\nFiles created:")
        print(f"1. CSV data: {csv_file}")
        print(f"2. Markdown report: {md_file}")

        # Return the dataframe for potential further use
        return pd.DataFrame(unique_articles)
    else:
        print("No articles found. Please check your internet connection or try different sources.")
        return None


if __name__ == "__main__":
    main()