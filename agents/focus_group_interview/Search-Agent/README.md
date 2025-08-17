# Education Resource Search Agent

[![CI](https://github.com/langchain-ai/react-agent/actions/workflows/unit-tests.yml/badge.svg)](https://github.com/langchain-ai/react-agent/actions/workflows/unit-tests.yml)
[![Integration Tests](https://github.com/langchain-ai/react-agent/actions/workflows/integration-tests.yml/badge.svg)](https://github.com/langchain-ai/react-agent/actions/workflows/integration-tests.yml)
[![Open in - LangGraph Studio](https://img.shields.io/badge/Open_in-LangGraph_Studio-00324d.svg?logo=data:image/svg%2bxml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSI4NS4zMzMiIGhlaWdodD0iODUuMzMzIiB2ZXJzaW9uPSIxLjAiIHZpZXdCb3g9IjAgMCA2NCA2NCI+PHBhdGggZD0iTTEzIDcuOGMtNi4zIDMuMS03LjEgNi4zLTYuOCAyNS43LjQgMjQuNi4zIDI0LjUgMjUuOSAyNC41QzU3LjUgNTggNTggNTcuNSA1OCAzMi4zIDU4IDcuMyA1Ni43IDYgMzIgNmMtMTIuOCAwLTE2LjEuMy0xOSAxLjhtMzcuNiAxNi42YzIuOCAyLjggMy40IDQuMiAzLjQgNy42cy0uNiA0LjgtMy40IDcuNkw0Ny4yIDQzSDE2LjhsLTMuNC0zLjRjLTQuOC00LjgtNC44LTEwLjQgMC0xNS4ybDMuNC0zLjRoMzAuNHoiLz48cGF0aCBkPSJNMTguOSAyNS42Yy0xLjEgMS4zLTEgMS43LjQgMi41LjkuNiAxLjcgMS44IDEuNyAyLjcgMCAxIC43IDIuOCAxLjYgNC4xIDEuNCAxLjkgMS40IDIuNS4zIDMuMi0xIC42LS42LjkgMS40LjkgMS41IDAgMi43LS41IDIuNy0xIDAtLjYgMS4xLS44IDIuNi0uNGwyLjYuNy0xLjgtMi45Yy01LjktOS4zLTkuNC0xMi4zLTExLjUtOS44TTM5IDI2YzAgMS4xLS45IDIuNS0yIDMuMi0yLjQgMS41LTIuNiAzLjQtLjUgNC4yLjguMyAyIDEuNyAyLjUgMy4xLjYgMS41IDEuNCAyLjMgMiAyIDEuNS0uOSAxLjItMy41LS40LTMuNS0yLjEgMC0yLjgtMi44LS44LTMuMyAxLjYtLjQgMS42LS41IDAtLjYtMS4xLS4xLTEuNS0uNi0xLjItMS42LjctMS43IDMuMy0yLjEgMy41LS41LjEuNS4yIDEuNi4zIDIuMiAwIC43LjkgMS40IDEuOSAxLjYgMi4xLjQgMi4zLTIuMy4yLTMuMi0uOC0uMy0yLTEuNy0yLjUtMy4xLTEuMS0zLTMtMy4zLTMtLjUiLz48L3N2Zz4=)](https://langgraph-studio.vercel.app/templates/open?githubUrl=https://github.com/langchain-ai/react-agent)

This agent helps find and process educational resources from various sources using LangGraph.

## Overview

The Education Resource Search Agent:

1. Validates if a topic is suitable for educational discussion/interview
2. Generates search queries for the topic
3. Searches multiple sources (YouTube, Wikipedia, web)
4. Processes and combines the results
5. Generates educational materials (table of contents, discussion questions)

## Features

- **Multi-source search**: YouTube transcripts, Wikipedia articles, and web search results
- **Content processing**: Removes duplicates, cleans text, formats results
- **Material generation**: Creates structured educational materials
- **Flexible configuration**: Customizable search parameters and model selection

## Getting Started

### Prerequisites

1. Create a `.env` file.

```bash
cp .env.example .env
```

2. Define required API keys in your `.env` file:

```
ANTHROPIC_API_KEY=your_anthropic_api_key
OPENAI_API_KEY=your_openai_api_key
SMITHERY_MCP_KEY=your_smithery_mcp_key
EXA_API_KEY=your_exa_api_key
```

### Setup MCP Servers

The agent uses Smithery MCP (Microservice Communication Protocol) servers for search functionality. These servers need to be running for the agent to work properly.

#### Option 1: Running MCP Servers Locally

1. Install the MCP server dependencies:

```bash
pip install -e ".[mcp]"
```

2. Start the MCP servers:

```bash
cd mcp_servers
python mcp_server.py
```

This will start the main MCP server on port 8000, which includes:
- YouTube Transcript Search (port 8001)
- Web Search (port 8002)

#### Option 2: Using Docker

1. Build and start the MCP servers using Docker Compose:

```bash
cd mcp_servers
docker-compose up -d
```

### Running the Agent

1. Install the agent dependencies:

```bash
pip install -e .
```

2. Run the agent:

```bash
python -m react_agent
```

## Running the Streamlit UI

1. Make sure the MCP servers are running (see above).

2. Run the Streamlit app:

```bash
streamlit run app.py
```

## Customization

1. **Add new search sources**: Extend the agent by adding new search tools in `src/react_agent/tools.py`.
2. **Select a different model**: Change the model in your configuration. Example: `openai/gpt-4-turbo-preview`.
3. **Customize the prompts**: Update the prompts in `src/react_agent/prompts.py`.
4. **Configure search parameters**: Adjust search parameters in `src/react_agent/configuration.py`.

## Development

The agent is built using LangGraph, which provides a flexible framework for creating AI agents. The main components are:

- `graph.py`: Defines the agent's workflow and node connections
- `tools.py`: Contains search tools for different sources
- `utils.py`: Provides utility functions for processing results
- `configuration.py`: Manages configuration settings
- `state.py`: Defines the agent's state structure
- `prompts.py`: Contains prompts for the language model

## MCP Server Architecture

The MCP servers provide search functionality through a RESTful API:

1. **Main MCP Server** (port 8000): Combines all search services
2. **YouTube Transcript Server** (port 8001): Searches YouTube videos and retrieves transcripts
3. **Web Search Server** (port 8002): Searches the web using Exa API

For more details on the MCP servers, see the [MCP Servers README](./mcp_servers/README.md).