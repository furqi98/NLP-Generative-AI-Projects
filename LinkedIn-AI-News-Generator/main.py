#!/usr/bin/env python3
"""
AI News Aggregator and LinkedIn Content Generator
Entry point script that runs either the news scraper or the LinkedIn content generator
"""

import os
import argparse
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='AI News Aggregator and LinkedIn Content Generator')
    parser.add_argument('--mode', type=str, choices=['scrape', 'generate', 'all'], 
                        default='all', help='Operation mode: scrape news, generate content, or both')
    parser.add_argument('--input', type=str, default='ai_news.csv',
                        help='Input CSV file for content generation (default: ai_news.csv)')
    parser.add_argument('--output_dir', type=str, default='.',
                        help='Directory to save output files (default: current directory)')
    
    args = parser.parse_args()
    
    # Run in the specified mode
    if args.mode in ['scrape', 'all']:
        print("Starting AI News Aggregator...")
        from news_aggregator.scraper import main as run_scraper
        run_scraper(output_dir=args.output_dir)
        
    if args.mode in ['generate', 'all']:
        print("\nStarting LinkedIn Content Generator...")
        # Check if required environment variables are set
        if not os.getenv('HUGGINGFACE_API_TOKEN') or not os.getenv('TAVILY_API_KEY'):
            print("Error: HUGGINGFACE_API_TOKEN and TAVILY_API_KEY must be set in the .env file")
            return
            
        from linkedin_generator.system import LinkedInContentSystem
        system = LinkedInContentSystem()
        system.run(file_path=args.input)
        
if __name__ == "__main__":
    main()