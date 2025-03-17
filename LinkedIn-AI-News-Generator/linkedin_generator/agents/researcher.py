"""
Researcher Agent - Researches additional information on the selected topic
"""

import os
import time
from langchain_huggingface import HuggingFaceEndpoint
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_community.tools.tavily_search.tool import TavilySearchResults

class ResearcherAgent:
    """Agent 2: Researches additional information on the selected topic using Tavily AI-optimized search"""

    def __init__(self, llm=None):
        # Get API tokens from environment if not passed directly
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

        # Check for Tavily API key
        tavily_api_key = os.getenv('TAVILY_API_KEY')
        if not tavily_api_key:
            raise ValueError("TAVILY_API_KEY environment variable is required")

        # Set up Tavily search tool - AI-optimized for agents
        self.search_tool = TavilySearchResults(
            tavily_api_key=tavily_api_key,
            max_results=5,
            include_raw_content=True,
            include_images=False
        )

        self.research_prompt = PromptTemplate(
            input_variables=["article", "search_results"],
            template="""
            You are an AI research specialist. You need to create a concise brief on the following article for a LinkedIn post.

            Original article:
            {article}

            Additional search results:
            {search_results}

            Create a brief summary covering only:
            1. 2-3 key facts or statistics about the topic
            2. Recent developments or trends (1-2 points)
            3. Industry impact and business applications (1-2 points)
            4. One expert opinion or quote if available

            Keep your response under 500 words. Focus only on the most important information.
            """
        )

        self.chain = LLMChain(llm=self.llm, prompt=self.research_prompt)

    def generate_search_queries(self, article):
        """Generate search queries based on the selected article"""
        title = article.get('title', '')
        summary = article.get('summary', '')

        # Create 3 different search queries for diverse results
        queries = [
            f"{title} latest developments impact business",
            f"{title} expert opinions statistics trends",
            f"{title} industry applications future implications"
        ]

        return queries

    def research_topic(self, article):
        """Research additional information about the topic using Tavily"""
        queries = self.generate_search_queries(article)

        all_results = []
        for query in queries:
            try:
                print(f"Searching Tavily for: {query}")
                results = self.search_tool.run(query)
                # Extract just the titles and snippets to reduce token count
                processed_results = self._process_search_results(results)
                all_results.append(f"Results for '{query}':\n{processed_results}")
                time.sleep(1)  # Be nice to the search API
            except Exception as e:
                print(f"Error during Tavily search: {str(e)}")

        search_results = "\n\n".join(all_results)

        # Format the article for the prompt
        article_text = f"Title: {article.get('title', '')}\n"
        article_text += f"Source: {article.get('source', '')}\n"
        article_text += f"Summary: {article.get('summary', '')}\n"
        article_text += f"URL: {article.get('url', '')}\n"

        # Truncate search results if they're too long (approximate token limit)
        max_search_results_chars = 10000  # Roughly estimate to keep under token limits
        if len(search_results) > max_search_results_chars:
            print(f"Warning: Truncating search results from {len(search_results)} characters to {max_search_results_chars}")
            search_results = search_results[:max_search_results_chars] + "... [truncated due to length]"

        research_brief = self.chain.run(article=article_text, search_results=search_results)

        return research_brief, search_results
        
    def _process_search_results(self, results):
        """Process search results to extract only the most important information"""
        try:
            processed = []
            # Assuming results is a list of dictionaries with 'title' and 'snippet' fields
            if isinstance(results, str):
                # If it's already a string, just truncate it
                return results[:1000]
                
            if isinstance(results, list):
                for item in results[:3]:  # Only use top 3 results
                    if isinstance(item, dict):
                        title = item.get('title', 'No title')
                        snippet = item.get('snippet', item.get('content', 'No content'))
                        url = item.get('url', 'No URL')
                        
                        # Truncate snippet to reduce token count
                        if snippet and len(snippet) > 300:
                            snippet = snippet[:300] + "..."
                            
                        processed.append(f"Title: {title}\nURL: {url}\nSummary: {snippet}\n")
                    else:
                        processed.append(str(item)[:200])  # Just convert to string and truncate
                        
                return "\n".join(processed)
            
            # Fallback for unknown format
            return str(results)[:1000]  # Truncate to 1000 chars as a safety measure
        except Exception as e:
            print(f"Error processing search results: {str(e)}")
            return "Error processing search results. Using limited information."