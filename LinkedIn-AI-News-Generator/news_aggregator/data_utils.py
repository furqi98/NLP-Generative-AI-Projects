"""
Data utilities for saving and processing news articles
"""

import pandas as pd
from datetime import datetime
import os

def save_to_csv(articles, filename="ai_news.csv"):
    """Save articles to a CSV file"""
    df = pd.DataFrame(articles)
    df.to_csv(filename, index=False)
    print(f"Data saved to {filename}")
    return filename

def save_to_markdown(articles, filename="ai_news.md"):
    """Save articles to a Markdown file with more readable formatting"""
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"# AI News and Trends\n")
        f.write(f"*Fetched on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n")

        # Group by source
        df = pd.DataFrame(articles)
        for source, group in df.groupby('source'):
            f.write(f"## Source: {source}\n\n")

            # Sort by date (newest first)
            try:
                sorted_group = group.sort_values(by='date', ascending=False)
            except:
                # If sorting fails, use the original group
                sorted_group = group

            for _, article in sorted_group.iterrows():
                f.write(f"### {article['title']}\n")

                # Format date safely
                try:
                    date_str = article['date'].strftime('%Y-%m-%d %H:%M')
                except:
                    date_str = "Unknown date"

                f.write(f"*Published: {date_str}*\n\n")
                f.write(f"{article['summary']}\n\n")
                f.write(f"[Read More]({article['url']})\n\n")
                f.write("---\n\n")

    print(f"Data saved to {filename}")
    return filename