"""Web Search MCP Server.

This server provides an API for searching the web using Exa API.
"""

import os
from typing import Dict, List

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel

# Load environment variables
load_dotenv()

app = FastAPI(
    title="Web Search MCP Server",
    description="API for searching the web using Exa API",
    version="1.0.0",
)

# API keys for authentication
MCP_API_KEY = os.getenv("SMITHERY_MCP_KEY", "default_key")
EXA_API_KEY = os.getenv("EXA_API_KEY")

# Exa API endpoint
EXA_API_URL = "https://api.exa.ai/search"


class SearchResult(BaseModel):
    """Search result model."""

    title: str
    url: str
    snippet: str


class SearchResponse(BaseModel):
    """Search response model."""

    results: List[SearchResult]


@app.get("/exa/search", response_model=SearchResponse)
async def search_web(
    q: str = Query(..., description="Search query"),
    max_results: int = Query(5, description="Maximum number of results to return"),
    key: str = Query(..., description="API key for authentication"),
) -> Dict:
    """Search the web using Exa API.

    Args:
        q: Search query
        max_results: Maximum number of results to return
        key: API key for authentication

    Returns:
        Search results
    """
    # Validate API key
    if key != MCP_API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")

    # Validate Exa API key
    if not EXA_API_KEY:
        raise HTTPException(status_code=500, detail="Exa API key not configured")

    try:
        # Search using Exa API
        async with httpx.AsyncClient() as client:
            response = await client.post(
                EXA_API_URL,
                headers={"x-api-key": EXA_API_KEY},
                json={
                    "query": q,
                    "numResults": max_results,
                    "useAutoprompt": True,
                    "type": "keyword",
                },
                timeout=30.0,
            )

            if response.status_code != 200:
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"Exa API error: {response.text}",
                )

            data = response.json()

            # Process results
            results = []
            for result in data.get("results", []):
                results.append(
                    SearchResult(
                        title=result.get("title", "No title"),
                        url=result.get("url", "No URL"),
                        snippet=result.get("text", "No snippet available"),
                    )
                )

            return {"results": results}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching web: {str(e)}")


@app.get("/exa/health")
async def health_check() -> Dict:
    """Health check endpoint."""
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("WEB_SEARCH_MCP_PORT", "8002"))
    uvicorn.run(app, host="0.0.0.0", port=port)
