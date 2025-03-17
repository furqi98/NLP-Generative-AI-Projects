"""
AI News Aggregator Package
"""

from news_aggregator.scraper import main as run_scraper
from news_aggregator.data_utils import save_to_csv, save_to_markdown

__all__ = ['run_scraper', 'save_to_csv', 'save_to_markdown']