"""YouTube Transcript MCP Server.

This server provides an API for searching YouTube videos and retrieving transcripts.
"""

import os
from typing import Dict, List, Optional
import httpx

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from youtube_search_python import YoutubeSearch
from youtube_transcript_api import YouTubeTranscriptApi

# Load environment variables
load_dotenv()

app = FastAPI(
    title="YouTube Transcript MCP Server",
    description="API for searching YouTube videos and retrieving transcripts",
    version="1.0.0",
)

# API key for authentication
API_KEY = os.getenv("SMITHERY_MCP_KEY", "default_key")


class YouTubeResult(BaseModel):
    """YouTube search result model."""

    title: str
    url: str
    channel: str
    duration: str
    views: Optional[str] = None
    transcript: Optional[str] = None


class SearchResponse(BaseModel):
    """Search response model."""

    results: List[YouTubeResult]


def get_video_id(url: str) -> str:
    """Extract video ID from YouTube URL."""
    if "youtube.com/watch?v=" in url:
        return url.split("youtube.com/watch?v=")[1].split("&")[0]
    elif "youtu.be/" in url:
        return url.split("youtu.be/")[1].split("?")[0]
    else:
        raise ValueError("Invalid YouTube URL")


def get_transcript(video_id: str) -> str:
    """Get transcript for a YouTube video."""
    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        return " ".join([t["text"] for t in transcript_list])
    except Exception:
        # Log the error instead of printing
        # print(f"Error getting transcript for video {video_id}: {str(e)}")
        return "Transcript not available"


@app.get("/mcp-youtube-transcript/search", response_model=SearchResponse)
async def search_youtube(
    q: str = Query(..., description="Search query"),
    max_results: int = Query(5, description="Maximum number of results to return"),
    key: str = Query(..., description="API key for authentication"),
) -> Dict:
    """Search YouTube videos and retrieve transcripts.

    Args:
        q: Search query
        max_results: Maximum number of results to return
        key: API key for authentication

    Returns:
        Search results with transcripts
    """
    # Validate API key
    if key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")

    try:
        # Search YouTube
        search_results = YoutubeSearch(q, max_results=max_results).to_dict()
        
        # Process results
        results = []
        for result in search_results:
            video_url = f"https://youtube.com{result['url_suffix']}"
            video_id = get_video_id(video_url)
            
            # Get transcript
            transcript = get_transcript(video_id)
            
            results.append(
                YouTubeResult(
                    title=result["title"],
                    url=video_url,
                    channel=result["channel"],
                    duration=result["duration"],
                    views=result.get("views"),
                    transcript=transcript,
                )
            )
        
        return {"results": results}

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error searching YouTube: {str(e)}"
        )


@app.get("/mcp-youtube-transcript/health")
async def health_check() -> Dict:
    """Health check endpoint."""
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("YOUTUBE_MCP_PORT", "8001"))
    uvicorn.run(app, host="0.0.0.0", port=port)
