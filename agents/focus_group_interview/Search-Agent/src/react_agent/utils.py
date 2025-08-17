"""Utility & helper functions."""

import csv
import os
import re
from datetime import datetime
from typing import Dict, List, Optional

import aiohttp
import wikipediaapi
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic

# from langchain.chat_models import init_chat_model
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import BaseMessage

from react_agent.configuration import Configuration

OUTPUT_DIR = "search_results"


def save_to_csv(results: List[Dict[str, str]], source: str):
    """Save search results to CSV file."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{OUTPUT_DIR}/{source}_results_{timestamp}.csv"
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f, fieldnames=["search_date", "source_link", "headline", "text"]
        )
        writer.writeheader()
        writer.writerows(results)
    return filename


def get_message_text(msg: BaseMessage) -> str:
    """Get the text content of a message."""
    content = msg.content
    if isinstance(content, str):
        return content
    elif isinstance(content, dict):
        return content.get("text", "")
    else:
        txts = [c if isinstance(c, str) else (c.get("text") or "") for c in content]
        return "".join(txts).strip()


def load_chat_model(
    model_name: str, model_provider: str = "openai", api_key: Optional[str] = None
) -> BaseChatModel:
    """Load a chat model with the specified configuration."""
    try:
        if model_provider == "openai":
            return ChatOpenAI(
                model=model_name,
                api_key=api_key
            )
        elif model_provider == "anthropic":
            return ChatAnthropic(
                model=model_name,
                api_key=api_key
            )
        else:
            raise ValueError(f"Unsupported model provider: {model_provider}")
    except Exception:
        # print(f"Error loading chat model: {str(e)}")
        raise


class SmitheryMCPClient:
    """Client for interacting with Smithery MCP server."""

    def __init__(self, config: Configuration):
        """Initialize the Smithery MCP client."""
        self.base_url = config.smithery_mcp_url
        self.timeout = config.search_timeout
        self.api_key = config.smithery_mcp_key
        self.youtube_endpoint = config.youtube_mcp_endpoint
        self.web_search_endpoint = config.web_search_mcp_endpoint
        self.wiki_api = wikipediaapi.Wikipedia(
            language="en",
            extract_format=wikipediaapi.ExtractFormat.WIKI,
            user_agent="EducationResourceSearcher/1.0",
        )

    async def search_youtube(
        self, query: str, max_results: int = 10
    ) -> List[Dict[str, str]]:
        """Search YouTube using Smithery MCP YouTube Transcript server."""
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{self.base_url}/{self.youtube_endpoint}/search",
                params={"q": query, "max_results": max_results, "key": self.api_key},
                timeout=self.timeout,
            ) as response:
                if response.status != 200:
                    raise Exception(f"YouTube search failed: {response.status}")
                data = await response.json()
                return [
                    {
                        "search_date": datetime.now().isoformat(),
                        "source_link": item["url"],
                        "headline": item["title"],
                        "text": item.get("transcript", "No transcript available"),
                    }
                    for item in data["results"]
                ]

    async def search_wikipedia(
        self, query: str, max_results: int = 10
    ) -> List[Dict[str, str]]:
        """Search Wikipedia using wikipedia-api library."""
        try:
            # Search for pages
            search_results = self.wiki_api.search(query, max_results)
            results = []

            for title in search_results:
                page = self.wiki_api.page(title)
                if page.exists():
                    results.append(
                        {
                            "search_date": datetime.now().isoformat(),
                            "source_link": page.fullurl,
                            "headline": page.title,
                            "text": page.text[
                                :1000
                            ],  # First 1000 characters of the text
                        }
                    )

            return results
        except Exception as e:
            raise Exception(f"Wikipedia search failed: {str(e)}")

    async def search_web(
        self, query: str, max_results: int = 10
    ) -> List[Dict[str, str]]:
        """Search web using Smithery MCP Exa server."""
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{self.base_url}/{self.web_search_endpoint}/search",
                params={"q": query, "max_results": max_results, "key": self.api_key},
                timeout=self.timeout,
            ) as response:
                if response.status != 200:
                    raise Exception(f"Web search failed: {response.status}")
                data = await response.json()
                return [
                    {
                        "search_date": datetime.now().isoformat(),
                        "source_link": item["url"],
                        "headline": item["title"],
                        "text": item["snippet"],
                    }
                    for item in data["results"]
                ]


def preprocess_text(text: str) -> str:
    """Clean and preprocess text content."""
    # Remove special characters and extra whitespace
    text = re.sub(r"[^\w\s.,!?-]", " ", text)
    text = re.sub(r"\s+", " ", text)

    # Remove common ad patterns
    ad_patterns = [
        r"sponsored",
        r"advertisement",
        r"click here",
        r"sign up now",
        r"limited time offer",
        r"buy now",
        r"free trial",
        r"subscribe",
        r"promotion",
        r"discount",
    ]
    for pattern in ad_patterns:
        text = re.sub(pattern, "", text, flags=re.IGNORECASE)

    return text.strip()


def remove_duplicates(results: List[Dict[str, str]]) -> List[Dict[str, str]]:
    """Remove duplicate sources based on URL."""
    seen_urls = set()
    unique_results = []

    for result in results:
        url = result["source_link"]
        if url not in seen_urls:
            seen_urls.add(url)
            unique_results.append(result)

    return unique_results


def generate_toc(results: List[Dict[str, str]]) -> str:
    """Generate table of contents from search results."""
    toc = ["# Table of Contents\n"]

    # Group by source
    sources = {}
    for result in results:
        source = result["source_link"].split("/")[2]  # Extract domain
        if source not in sources:
            sources[source] = []
        sources[source].append(result)

    # Generate TOC entries
    for source, items in sources.items():
        toc.append(f"\n## {source}\n")
        for item in items:
            toc.append(f"- {item['headline']}")

    return "\n".join(toc)


def generate_discussion_materials(results: List[Dict[str, str]]) -> str:
    """Generate discussion and interview materials from search results."""
    materials = ["# Discussion and Interview Materials\n"]

    # Group by source
    sources = {}
    for result in results:
        source = result["source_link"].split("/")[2]
        if source not in sources:
            sources[source] = []
        sources[source].append(result)

    # Generate materials for each source
    for source, items in sources.items():
        materials.append(f"\n## {source}\n")

        # Key points
        materials.append("### Key Points")
        for item in items:
            materials.append(f"- {item['headline']}")
            materials.append(f"  - {item['text'][:200]}...")

        # Discussion questions
        materials.append("\n### Discussion Questions")
        for item in items:
            materials.append(
                f"1. How does {item['headline']} relate to the main topic?"
            )
            materials.append("2. What are the key takeaways from this source?")

        # Interview questions
        materials.append("\n### Interview Questions")
        for item in items:
            materials.append(f"1. Can you elaborate on {item['headline']}?")
            materials.append(
                "2. What are your thoughts on the perspective presented in this source?"
            )

    return "\n".join(materials)


def save_materials_to_file(content: str, filename: str) -> str:
    """Save generated materials to a markdown file."""
    output_dir = "generated_materials"
    os.makedirs(output_dir, exist_ok=True)

    filepath = os.path.join(output_dir, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    return filepath