"""
LinkedIn Content System - Main orchestration system
"""

import os
import pandas as pd
import time
from langchain_huggingface import HuggingFaceEndpoint
from linkedin_generator.agents.curator import CuratorAgent
from linkedin_generator.agents.researcher import ResearcherAgent
from linkedin_generator.agents.writer import WriterAgent

def load_articles(file_path="ai_news.csv"):
    """Load articles from CSV file"""
    try:
        df = pd.read_csv(file_path)
        print(f"Loaded {len(df)} articles from {file_path}")
        return df
    except Exception as e:
        print(f"Error loading articles: {str(e)}")
        return pd.DataFrame(columns=['title', 'date', 'source', 'url', 'summary'])

class LinkedInContentSystem:
    """Main system that orchestrates the three agents"""

    def __init__(self):
        # Get API token from environment
        huggingface_api_token = os.getenv('HUGGINGFACE_API_TOKEN')
        if not huggingface_api_token:
            raise ValueError("HUGGINGFACE_API_TOKEN environment variable is required")
        
        # Initialize the shared LLM
        self.llm = HuggingFaceEndpoint(
            repo_id="mistralai/Mistral-7B-Instruct-v0.2",
            temperature=0.7,
            max_new_tokens=512,
            huggingfacehub_api_token=huggingface_api_token,
            timeout=120
        )
        
        # Initialize agents with the shared LLM
        self.curator = CuratorAgent(self.llm)
        self.researcher = ResearcherAgent(self.llm)
        self.writer = WriterAgent(self.llm)

        # State variables
        self.articles_df = None
        self.shortlisted_df = None
        self.selected_article = None
        self.research_brief = None
        self.search_results = None
        self.linkedin_post = None

    def run(self, file_path="ai_news.csv"):
        """Run the full pipeline"""
        # Step 1: Load articles
        print("🔍 Loading articles...")
        self.articles_df = load_articles(file_path)

        if self.articles_df.empty:
            print("No articles found. Please run the news scraper first.")
            return

        # Step 2: Shortlist articles
        print("\n🔍 Shortlisting the most promising articles based on titles...")
        self.shortlisted_df = self.curator.shortlist_articles(self.articles_df)

        # Display shortlisted articles
        print("\nShortlisted Articles:")
        print(self.shortlisted_df[['title', 'source']].to_string())

        # Step 3: Select the best article
        print("\n🔍 Analyzing and selecting the best article for LinkedIn...")
        self.selected_article, analysis = self.curator.select_best_article(self.shortlisted_df)

        # Display selected article
        print("\nSelected Article:")
        if self.selected_article:
            for key, value in self.selected_article.items():
                print(f"{key}: {value}")
                
        print("\nSelection Analysis:")
        print(analysis)

        # Step 4: Research additional information
        print("\n🔍 Researching additional information using Tavily...")
        self.research_brief, self.search_results = self.researcher.research_topic(self.selected_article)

        # Display research brief
        print("\nResearch Brief:")
        print(self.research_brief)

        # Step 5: Generate LinkedIn post
        print("\n✍️ Generating LinkedIn post...")
        self.linkedin_post = self.writer.generate_post(self.selected_article, self.research_brief)

        # Display the LinkedIn post
        self.display_post_with_options()
        
        return self.linkedin_post

    def display_post_with_options(self):
        """Display the LinkedIn post with editing options"""
        print("\n===== GENERATED LINKEDIN POST =====")
        print(self.linkedin_post)
        print("\n===================================")
        
        # Character count
        char_count = len(self.linkedin_post)
        print(f"Character count: {char_count} {'(Good LinkedIn length)' if char_count <= 1300 else '(Consider shortening)'}")
        
        # Save to file option
        save_option = input("\nWould you like to save this post to a file? (y/n): ")
        if save_option.lower() == 'y':
            file_name = input("Enter filename (default: linkedin_post.txt): ") or "linkedin_post.txt"
            with open(file_name, 'w', encoding='utf-8') as f:
                f.write(self.linkedin_post)
            print(f"Post saved to {file_name}")
        
        # Refine option
        refine_option = input("\nWould you like to refine this post? (y/n): ")
        if refine_option.lower() == 'y':
            feedback = input("Enter your feedback for refinement: ")
            print("\n✍️ Refining LinkedIn post based on feedback...")
            self.linkedin_post = self.writer.refine_post(self.linkedin_post, feedback)
            # Show the refined post
            self.display_post_with_options()
        
        # Regenerate option
        regenerate_option = input("\nWould you like to regenerate the post from scratch? (y/n): ")
        if regenerate_option.lower() == 'y':
            print("\n✍️ Regenerating LinkedIn post...")
            self.linkedin_post = self.writer.generate_post(self.selected_article, self.research_brief)
            # Show the regenerated post
            self.display_post_with_options()


if __name__ == "__main__":
    system = LinkedInContentSystem()
    system.run()