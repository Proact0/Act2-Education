"""This module provides tools for web scraping and search functionality.

It includes search tools for YouTube, Wikipedia, and web search using Smithery MCP.
"""

from typing import List, Optional

import aiohttp
import wikipedia
import wikipediaapi
from langchain_core.tools import BaseTool

from react_agent.configuration import Configuration


class YouTubeSearchTool(BaseTool):
    """Tool for searching YouTube videos and transcripts."""

    name: str = "youtube_search"
    description: str = "Search for videos on YouTube and retrieve transcripts. Input should be a search query."

    def _run(self, query: str) -> str:
        """Run the YouTube search synchronously."""
        import asyncio
        return asyncio.run(self._arun(query))

    async def _arun(self, query: str) -> str:
        """Run the YouTube search asynchronously."""
        configuration = Configuration.from_context()

        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{configuration.smithery_mcp_url}/{configuration.youtube_mcp_endpoint}/search",
                params={
                    "q": query,
                    "max_results": configuration.max_search_results,
                    "key": configuration.smithery_mcp_key,
                },
                timeout=configuration.search_timeout,
            ) as response:
                if response.status != 200:
                    return f"YouTube search failed: {response.status}"

                data = await response.json()
                results = data.get("results", [])

                if not results:
                    return "No YouTube videos found for the query."

                # Format the results
                formatted_results = []
                for item in results:
                    title = item.get("title", "No title")
                    url = item.get("url", "No URL")
                    transcript_snippet = (
                        item.get("transcript", "No transcript available")[:300] + "..."
                    )

                    formatted_results.append(
                        f"Title: {title}\nURL: {url}\nTranscript: {transcript_snippet}\n"
                    )

                return "\n".join(formatted_results)


class WikipediaSearchTool(BaseTool):
    """Tool for searching Wikipedia articles."""

    name: str = "wikipedia_search"
    description: str = (
        "Search for articles on Wikipedia. Input should be a search query."
    )
    wiki_api: Optional[wikipediaapi.Wikipedia] = None

    def __init__(self):
        """Initialize the Wikipedia search tool."""
        super().__init__()
        self.wiki_api = wikipediaapi.Wikipedia(
            language="en",
            extract_format=wikipediaapi.ExtractFormat.WIKI,
            user_agent="EducationResourceSearcher/1.0",
        )

    def _run(self, query: str) -> list[dict[str, str]]:
        """Run the Wikipedia search."""
        print(f"Wikipedia search query: {query}")
        try:
            # Use wikipedia_search_function to get article titles
            search_titles = wikipedia.search(query, results=5) # Limit to 5 results
            
            results = []
            for title in search_titles:
                page = self.wiki_api.page(title)
                if page.exists():
                    results.append({
                        "headline": page.title,
                        "url": page.fullurl,
                        "text": page.summary[:1500] # Truncate summary to 1500 characters
                    })
            
            if not results:
                print("No Wikipedia articles found for the query.")
                return []
            
            return results
        except Exception as e:
            print(f"Error searching Wikipedia: {str(e)}")
            return []

    async def _arun(self, query: str) -> list[dict[str, str]]:
        """Run the Wikipedia search asynchronously."""
        print(f"Wikipedia search query: {query}")
        try:
            # Use wikipedia_search_function to get article titles
            search_titles = wikipedia.search(query, results=5) # Limit to 5 results
            
            results = []
            for title in search_titles:
                page = self.wiki_api.page(title)
                if page.exists():
                    results.append({
                        "headline": page.title,
                        "url": page.fullurl,
                        "text": page.summary[:1500] # Truncate summary to 1500 characters
                    })
            
            if not results:
                print("No Wikipedia articles found for the query.")
                return []
            
            return results
        except Exception as e:
            print(f"Error searching Wikipedia: {str(e)}")
            return []


class WebSearchTool(BaseTool):
    """Tool for web search using Smithery MCP Exa."""

    name: str = "web_search"
    description: str = "Search the web for information. Input should be a search query."

    def _run(self, query: str) -> str:
        """Run the web search synchronously."""
        import asyncio
        return asyncio.run(self._arun(query))

    async def _arun(self, query: str) -> str:
        """Run the web search asynchronously."""
        configuration = Configuration.from_context()

        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{configuration.smithery_mcp_url}/{configuration.web_search_mcp_endpoint}/search",
                params={
                    "q": query,
                    "max_results": configuration.max_search_results,
                    "key": configuration.smithery_mcp_key,
                },
                timeout=configuration.search_timeout,
            ) as response:
                if response.status != 200:
                    return f"Web search failed: {response.status}"

                data = await response.json()
                results = data.get("results", [])

                if not results:
                    return "No web search results found for the query."

                # Format the results
                formatted_results = []
                for item in results:
                    title = item.get("title", "No title")
                    url = item.get("url", "No URL")
                    snippet = item.get("snippet", "No snippet available")

                    formatted_results.append(
                        f"Title: {title}\nURL: {url}\nSnippet: {snippet}\n"
                    )

                return "\n".join(formatted_results)


# List of available tools
TOOLS: List[BaseTool] = [YouTubeSearchTool(), WikipediaSearchTool(), WebSearchTool()]
