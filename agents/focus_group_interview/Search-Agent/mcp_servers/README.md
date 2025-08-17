# Smithery MCP Servers

This directory contains the implementation of Smithery MCP (Microservice Communication Protocol) servers for educational resource search.

## Overview

The MCP servers provide search functionality for various sources:

1. **YouTube Transcript Search** - Search for YouTube videos and retrieve their transcripts
2. **Web Search** - Search the web using Exa API

## Setup

### Prerequisites

- Python 3.9+
- API keys:
  - Exa API key (for web search)
  - Smithery MCP key (for authentication)

### Installation

1. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file with the following variables:
   ```
   SMITHERY_MCP_KEY=your_mcp_key
   EXA_API_KEY=your_exa_api_key
   MCP_SERVER_PORT=8000
   YOUTUBE_MCP_PORT=8001
   WEB_SEARCH_MCP_PORT=8002
   ```

## Running the Servers

### Running Individual Servers

1. YouTube Transcript Server:
   ```bash
   python youtube_transcript_server.py
   ```

2. Web Search Server:
   ```bash
   python web_search_server.py
   ```

### Running the Combined MCP Server

```bash
python mcp_server.py
```

The main server will be available at `http://localhost:8000`.

## API Endpoints

### YouTube Transcript Search

- **Endpoint**: `/mcp-youtube-transcript/search`
- **Method**: GET
- **Parameters**:
  - `q`: Search query
  - `max_results`: Maximum number of results (default: 5)
  - `key`: API key for authentication
- **Health Check**: `/mcp-youtube-transcript/health`

### Web Search

- **Endpoint**: `/exa/search`
- **Method**: GET
- **Parameters**:
  - `q`: Search query
  - `max_results`: Maximum number of results (default: 5)
  - `key`: API key for authentication
- **Health Check**: `/exa/health`

### Main Server

- **Root**: `/`
- **Health Check**: `/health`

## Usage with the Education Resource Search Agent

The agent is configured to connect to these MCP servers. Make sure the servers are running before using the agent.

## Troubleshooting

- If you encounter connection errors, check that the servers are running and the ports are correctly configured.
- For API key errors, verify that the `.env` file contains the correct keys.
- For YouTube transcript errors, some videos may not have transcripts available. 