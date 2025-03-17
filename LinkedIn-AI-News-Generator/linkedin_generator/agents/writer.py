"""
Writer Agent - Generates the LinkedIn post and handles refinements
"""

import os
from langchain_huggingface import HuggingFaceEndpoint
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

class WriterAgent:
    """Agent 3: Generates the LinkedIn post and handles refinements"""

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

        # Keep the template internally - we'll use it but prevent it from leaking to output
        self._post_prompt = PromptTemplate(
            input_variables=["article", "research"],
            template="""
            You are a professional LinkedIn content creator specializing in AI and technology content. Your posts consistently get high engagement through a perfect blend of informative content, conversational tone, and strategic formatting.

            Create a highly engaging LinkedIn post based on this information:

            Article:
            {article}

            Research:
            {research}

            Follow these LinkedIn best practices:
            1. Start with a compelling hook or question
            2. Include relevant statistics or surprising facts
            3. Break content into short, skimmable paragraphs
            4. Add 3-5 relevant hashtags
            5. Include a clear call-to-action
            6. Keep to around 1300 characters (LinkedIn's sweet spot)
            7. Use emojis strategically (but not excessively)
            8. Format with line breaks for readability

            Your post should sound authentic, conversational, and thought-provoking - not promotional or overly formal.

            Write ONLY the post content, nothing else. Do not include any prompt text or instructions.
            """
        )

        self._refine_prompt = PromptTemplate(
            input_variables=["original_post", "feedback"],
            template="""
            You are a professional LinkedIn content creator specializing in AI and technology content.

            Here is an original LinkedIn post:
            {original_post}

            The user has provided this feedback on the post:
            {feedback}

            Revise the post based on this feedback while maintaining high engagement potential.
            Write ONLY the revised post content, nothing else.
            """
        )

        self.post_chain = LLMChain(llm=self.llm, prompt=self._post_prompt)
        self.refine_chain = LLMChain(llm=self.llm, prompt=self._refine_prompt)

    def generate_post(self, article, research):
        """Generate a LinkedIn post based on the article and research"""
        # Format the article for the prompt
        article_text = f"Title: {article.get('title', '')}\n"
        article_text += f"Source: {article.get('source', '')}\n"
        article_text += f"Summary: {article.get('summary', '')}\n"

        # Generate the post
        raw_post = self.post_chain.run(article=article_text, research=research)

        # Process the output to extract just the LinkedIn post
        # Remove any template text or instructions that might have been included
        lines = raw_post.split('\n')
        clean_lines = []
        for line in lines:
            # Filter out any lines that are likely template instructions
            if "LinkedIn" in line and "post" in line and ":" in line:
                continue
            if "Write ONLY" in line or "Your post should" in line:
                continue
            if line.strip().startswith("Post:") and len(line) < 10:
                continue
            clean_lines.append(line)

        cleaned_post = '\n'.join(clean_lines).strip()
        return cleaned_post

    def refine_post(self, original_post, feedback):
        """Refine the post based on user feedback"""
        raw_refined_post = self.refine_chain.run(original_post=original_post, feedback=feedback)

        # Similar cleaning for refined post
        lines = raw_refined_post.split('\n')
        clean_lines = []
        for line in lines:
            if "LinkedIn" in line and "post" in line and ":" in line:
                continue
            if "Write ONLY" in line or "Your post should" in line:
                continue
            if line.strip().startswith("Post:") and len(line) < 10:
                continue
            clean_lines.append(line)

        cleaned_post = '\n'.join(clean_lines).strip()
        return cleaned_post