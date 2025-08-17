"""Smithery MCP Server.

This is the main MCP server that combines all search services.
"""

import os
from typing import Dict

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import httpx
from mcp_servers.web_search_server import app as web_search_app
from mcp_servers.youtube_transcript_server import app as youtube_app

# Load environment variables
load_dotenv()

app = FastAPI(
    title="Smithery MCP Server",
    description="API for searching educational resources",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API key for authentication
API_KEY = os.getenv("SMITHERY_MCP_KEY", "default_key")

# Mount sub-applications
app.mount("/mcp-youtube-transcript", youtube_app)
app.mount("/exa", web_search_app)


@app.get("/")
async def root() -> Dict:
    """Root endpoint."""
    return {
        "message": "Smithery MCP Server is running",
        "services": [
            {
                "name": "YouTube Transcript Search",
                "endpoint": "/mcp-youtube-transcript/search",
                "health": "/mcp-youtube-transcript/health",
            },
            {"name": "Web Search", "endpoint": "/exa/search", "health": "/exa/health"},
        ],
    }


@app.get("/health")
async def health_check() -> Dict:
    """Health check endpoint for all services."""
    health_status = {"status": "ok", "services": {}}

    # Check YouTube service
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f'http://localhost:{os.getenv("YOUTUBE_MCP_PORT", "8001")}/mcp-youtube-transcript/health')
            response.raise_for_status()
            youtube_health = response.json()
            health_status["services"]["youtube"] = youtube_health["status"]
    except Exception as e:
        health_status["services"]["youtube"] = f"error: {str(e)}"

    # Check web search service
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f'http://localhost:{os.getenv("WEB_SEARCH_MCP_PORT", "8002")}/exa/health')
            response.raise_for_status()
            web_search_health = response.json()
            health_status["services"]["web_search"] = web_search_health["status"]
    except Exception as e:
        health_status["services"]["web_search"] = f"error: {str(e)}"

    return health_status


if __name__ == "__main__":
    import uvicorn
    import os

    port = int(os.getenv("MCP_SERVER_PORT", "8000"))
    uvicorn.run(app, host="0.0.0.0", port=port, log_config=None)
