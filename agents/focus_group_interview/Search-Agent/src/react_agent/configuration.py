"""Define the configurable parameters for the agent."""

from __future__ import annotations

import os
from dataclasses import dataclass, field, fields
from typing import Optional

from dotenv import load_dotenv
from langchain_core.runnables import ensure_config
from langgraph.config import get_config

from react_agent import prompts

# Load environment variables from .env file
load_dotenv()


@dataclass(kw_only=True)
class Configuration:
    """The configuration for the agent."""

    system_prompt: str = field(
        default=prompts.SYSTEM_PROMPT,
        metadata={
            "description": "The system prompt to use for the agent's interactions. "
            "This prompt sets the context and behavior for the agent."
        },
    )

    model: str = field(
        default="gpt-4-turbo-preview",
        metadata={
            "description": "The name of the language model to use for the agent's main interactions. "
            "Should be in the form: provider/model-name."
        },
    )

    model_provider: str = field(
        default="openai",
        metadata={
            "description": "The provider of the language model (e.g., 'openai', 'anthropic')."
        },
    )

    model_api_key: Optional[str] = field(
        default=os.getenv("OPENAI_API_KEY"),
        metadata={"description": "API key for the language model."},
    )

    openai_api_key: Optional[str] = field(
        default=os.getenv("OPENAI_API_KEY"),
        metadata={"description": "OpenAI API key for fallback or specific operations."},
    )

    max_search_results: int = field(
        default=5,
        metadata={
            "description": "The maximum number of search results to return for each search query."
        },
    )

    smithery_mcp_url: str = field(
        default=os.getenv("SMITHERY_MCP_URL", "http://localhost:8000"),
        metadata={
            "description": "The URL of the Smithery MCP server for search operations."
        },
    )

    smithery_mcp_key: Optional[str] = field(
        default=os.getenv("SMITHERY_MCP_KEY"),
        metadata={"description": "API key for the Smithery MCP server."},
    )

    # YouTube MCP server configuration
    youtube_mcp_endpoint: str = field(
        default=os.getenv("YOUTUBE_MCP_ENDPOINT", "mcp-youtube-transcript"),
        metadata={"description": "The endpoint for the YouTube MCP server."},
    )

    # Web search MCP server configuration
    web_search_mcp_endpoint: str = field(
        default=os.getenv("WEB_SEARCH_MCP_ENDPOINT", "exa"),
        metadata={"description": "The endpoint for the web search MCP server."},
    )

    output_directory: str = field(
        default="search_results",
        metadata={"description": "The directory where search results will be saved."},
    )

    search_timeout: int = field(
        default=30,
        metadata={"description": "Timeout in seconds for search operations."},
    )

    generated_materials_dir: str = field(
        default="generated_materials",
        metadata={"description": "Directory where generated materials will be saved."},
    )

    @classmethod
    def from_runnable_config(cls, config: dict) -> Configuration:
        """Create a Configuration instance from a runnable config."""
        return cls(
            system_prompt=config.get("system_prompt", prompts.SYSTEM_PROMPT),
            model=config.get("model", "anthropic/claude-3-sonnet-20240229"),
            model_provider=config.get("model_provider", "anthropic"),
            model_api_key=config.get("model_api_key", os.getenv("ANTHROPIC_API_KEY")),
            openai_api_key=config.get("openai_api_key", os.getenv("OPENAI_API_KEY")),
            max_search_results=config.get("max_search_results", 5),
            search_timeout=config.get("search_timeout", 30),
            smithery_mcp_url=config.get(
                "smithery_mcp_url",
                os.getenv("SMITHERY_MCP_URL", "http://localhost:8000"),
            ),
            smithery_mcp_key=config.get(
                "smithery_mcp_key", os.getenv("SMITHERY_MCP_KEY")
            ),
            youtube_mcp_endpoint=config.get(
                "youtube_mcp_endpoint",
                os.getenv("YOUTUBE_MCP_ENDPOINT", "mcp-youtube-transcript"),
            ),
            web_search_mcp_endpoint=config.get(
                "web_search_mcp_endpoint", os.getenv("WEB_SEARCH_MCP_ENDPOINT", "exa")
            ),
            output_directory=config.get("output_directory", "search_results"),
            generated_materials_dir=config.get(
                "generated_materials_dir", "generated_materials"
            ),
        )

    @classmethod
    def from_context(cls) -> Configuration:
        """Create a Configuration instance from a RunnableConfig object."""
        try:
            config = get_config()
        except RuntimeError:
            config = None
        config = ensure_config(config)
        configurable = config.get("configurable") or {}
        _fields = {f.name for f in fields(cls) if f.init}
        return cls(**{k: v for k, v in configurable.items() if k in _fields})
