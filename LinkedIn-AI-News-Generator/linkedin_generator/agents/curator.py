"""
Curator Agent - Analyzes news articles and selects the most promising one for LinkedIn
"""

import pandas as pd
from langchain_huggingface import HuggingFaceEndpoint
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
import os

class CuratorAgent:
    """Agent 1: Analyzes news articles and selects the most promising one for LinkedIn"""

    def __init__(self, llm=None):
        # Get API token from environment if not passed directly
        if not llm:
            huggingface_api_token = os.getenv('HUGGINGFACE_API_TOKEN')
            if not huggingface_api_token:
                raise ValueError("HUGGINGFACE_API_TOKEN environment variable is required")
                
            self.llm = HuggingFaceEndpoint(
                repo_id="mistralai/Mistral-7B-Instruct-v0.2",
                temperature=0.7,
                max_new_tokens=512,
                huggingfacehub_api_token=huggingface_api_token,
                timeout=120
            )
        else:
            self.llm = llm

        self.shortlist_prompt = PromptTemplate(
            input_variables=["titles"],
            template="""
            You are an AI content curator specializing in finding trending AI topics that would perform well on LinkedIn. Your job is to analyze these article titles and select the 10 most promising ones that would generate high engagement on LinkedIn.

            Consider these factors when selecting:
            1. Trending technologies or emerging AI concepts
            2. Business applications of AI
            3. Industry transformations or disruptions
            4. Personal development opportunities in AI
            5. Controversial or debate-worthy topics

            Here are the article titles:
            {titles}

            Return a list of exactly 10 titles that would make the best LinkedIn posts, numbering them from 1-10. Only return the titles, nothing else.
            """
        )

        self.selection_prompt = PromptTemplate(
            input_variables=["articles"],
            template="""
            You are an AI content strategist for LinkedIn. Your task is to analyze these AI news articles and select the ONE that would make the most engaging LinkedIn post.

            LinkedIn audience typically engages with:
            - Practical business applications of AI
            - Career opportunities and skills development
            - Industry transformations
            - Thought leadership on emerging technologies
            - Success stories and case studies

            Here are the articles to analyze:
            {articles}

            Select the single most promising article that would generate maximum engagement on LinkedIn. First analyze each article explaining its potential engagement factors, then make your final selection.

            Return your analysis in this format:
            ANALYSIS:
            [Your detailed analysis of each article]

            SELECTION:
            [Title of the selected article]

            REASONING:
            [Explain why this article will perform best on LinkedIn]
            """
        )

        self.chain = LLMChain(llm=self.llm, prompt=self.selection_prompt)
        self.shortlist_chain = LLMChain(llm=self.llm, prompt=self.shortlist_prompt)

    def shortlist_articles(self, df, n=10):
        """Shortlist N articles from the dataframe based on titles"""
        all_titles = df['title'].tolist()
        titles_text = "\n".join([f"{i+1}. {title}" for i, title in enumerate(all_titles)])

        result = self.shortlist_chain.run(titles=titles_text)

        # Extract the selected titles
        selected_titles = []
        for line in result.split('\n'):
            if line.strip() and any(line.strip().startswith(str(i) + ".") for i in range(1, 11)):
                # Extract the title after the number
                parts = line.strip().split(".", 1)
                if len(parts) > 1:
                    selected_titles.append(parts[1].strip())

        # Match selected titles with original dataframe
        shortlisted_df = df[df['title'].isin(selected_titles)]

        # If we didn't get exactly 10 (due to parsing issues), take the top N
        if len(shortlisted_df) < n:
            remaining = n - len(shortlisted_df)
            missing_df = df[~df['title'].isin(selected_titles)].head(remaining)
            shortlisted_df = pd.concat([shortlisted_df, missing_df])

        return shortlisted_df.head(n)

    def select_best_article(self, df):
        """Select the best article for a LinkedIn post"""
        # Format articles for the prompt
        articles_text = ""
        for i, row in df.iterrows():
            articles_text += f"Article {i+1}:\n"
            articles_text += f"Title: {row['title']}\n"
            articles_text += f"Source: {row['source']}\n"
            articles_text += f"Summary: {row['summary']}\n\n"

        result = self.chain.run(articles=articles_text)

        # Extract the selected article title
        selected_title = None
        if "SELECTION:" in result:
            selection_section = result.split("SELECTION:")[1].split("REASONING:")[0].strip()
            selected_title = selection_section

        # Find the matching article
        selected_article = None
        for _, row in df.iterrows():
            if selected_title and selected_title in row['title']:
                selected_article = row.to_dict()
                break

        # If no match found, take the first article as fallback
        if not selected_article and not df.empty:
            selected_article = df.iloc[0].to_dict()

        return selected_article, result