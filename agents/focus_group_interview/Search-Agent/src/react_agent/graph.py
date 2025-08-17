"""Define an education resource search agent.

This agent helps find and process educational resources from various sources.
"""

import csv
import os
from datetime import datetime
from typing import Any, Dict

from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.runnables import RunnableConfig
from langgraph.graph import StateGraph

from react_agent import prompts
from react_agent.configuration import Configuration
from react_agent.state import InputState, State
from react_agent.tools import WikipediaSearchTool
from react_agent.utils import (
    SmitheryMCPClient,
    generate_discussion_materials,
    generate_toc,
    load_chat_model,
    preprocess_text,
    remove_duplicates,
    save_materials_to_file,
    save_to_csv,
)

# Create output directory if it doesn't exist
OUTPUT_DIR = "search_results"
os.makedirs(OUTPUT_DIR, exist_ok=True)


async def router_node(state: State, config: RunnableConfig) -> Dict[str, Any]:
    """Router node that validates if the topic is suitable for discussion/interview."""
    configuration = Configuration.from_context()
    model = load_chat_model(
        model_name=configuration.model,
        model_provider=configuration.model_provider,
        api_key=configuration.model_api_key,
    )

    # Use the topic validation prompt
    validation_prompt = prompts.TOPIC_VALIDATION_PROMPT.format(
        topic=state.messages[-1].content
    )

    response = await model.ainvoke([HumanMessage(content=validation_prompt)])
    response_text = response.content

    if response_text.startswith("VALID"):
        return {
            "messages": state.messages
            + [AIMessage(content="Topic is valid. Proceeding with query processing.")],
            "original_topic": state.messages[-1].content,
            "next": "query_processor",
        }
    else:
        return {
            "messages": state.messages
            + [
                AIMessage(
                    content="Topic is not valid for educational discussion. Please provide a more specific or educational topic."
                )
            ],
            "next": "__end__",
        }


async def query_processor_node(state: State, config: RunnableConfig) -> Dict[str, Any]:
    """Query processor node that generates search query variations."""
    configuration = Configuration.from_context()
    model = load_chat_model(
        model_name=configuration.model,
        model_provider=configuration.model_provider,
        api_key=configuration.model_api_key,
    )

    # Use the query generation prompt
    query_prompt = prompts.QUERY_GENERATION_PROMPT.format(
        topic=state.original_topic
    )

    response = await model.ainvoke([HumanMessage(content=query_prompt)])
    queries = [q.strip() for q in response.content.split("\n") if q.strip()]
    print(f"Generated queries: {queries}")

    return {
        "messages": state.messages
        + [AIMessage(content="Generated queries:\n" + "\n".join(queries))],
        "queries": queries,
        "next": "search_router",
    }


async def search_router_node(state: State, config: RunnableConfig) -> Dict[str, Any]:
    """Search router node that logs the queries and routes to all search engines."""
    # print(f"Search Router - Received queries: {state.queries}") # Removed for linting
    return {
        "messages": state.messages,
        "queries": state.queries,
        "next": "youtube",  # Start with YouTube, then Wikipedia, then web search
    }


async def youtuber_node(state: State, config: RunnableConfig) -> Dict[str, Any]:
    """Node for handling YouTube related tasks using Smithery MCP."""
    configuration = Configuration.from_context()
    client = SmitheryMCPClient(configuration)
    results = []

    for query in state.queries:
        try:
            query_results = await client.search_youtube(
                query, max_results=configuration.max_search_results
            )
            results.extend(query_results)
        except Exception as e:
            # print(f"Error searching YouTube for query '{query}': {str(e)}") # Removed for linting
            results.append(
                {
                    "search_date": datetime.now().isoformat(),
                    "source_link": f"https://youtube.com/search?q={query}",
                    "headline": f"Error searching YouTube for: {query}",
                    "text": f"Error: {str(e)}",
                }
            )

    filename = save_to_csv(results, "youtube")
    state.search_results["youtube"] = results
    print(f"YouTube search results: {results}")

    return {
        "youtube_results": results,
        "next": "wikipedia",  # Continue to Wikipedia search
    }


async def wikipedia_node(state: State, config: RunnableConfig) -> Dict[str, Any]:
    """Node for handling Wikipedia related tasks using wikipedia-api."""
    # configuration = Configuration.from_context() # Removed for linting
    results = []

    # Create Wikipedia search tool instance
    wiki_tool = WikipediaSearchTool()

    for query in state.queries:
        try:
            # Use the tool to search Wikipedia
            query_results = await wiki_tool._arun(query)

            # Add search date and source link to each result
            for result in query_results:
                result["search_date"] = datetime.now().isoformat()
                result["source_link"] = result["url"]
                del result["url"] # Remove the 'url' key as it's not expected by save_to_csv

            results.extend(query_results)
        except Exception as e:
            # print(f"Error searching Wikipedia for query '{query}': {str(e)}") # Removed for linting
            results.append(
                {
                    "search_date": datetime.now().isoformat(),
                    "source_link": f"https://wikipedia.org/wiki/{query}",
                    "headline": f"Error searching Wikipedia for: {query}",
                    "text": f"Error searching Wikipedia: {str(e)}",
                }
            )

    filename = save_to_csv(results, "wikipedia")
    state.search_results["wikipedia"] = results
    print(f"Wikipedia search results: {results}")

    return {
        "wikipedia_results": results,
        "next": "web_search",  # Continue to web search
    }


async def web_search_node(state: State, config: RunnableConfig) -> Dict[str, Any]:
    """Node for handling web search tasks using Smithery MCP."""
    configuration = Configuration.from_context()
    client = SmitheryMCPClient(configuration)
    results = []

    for query in state.queries:
        try:
            query_results = await client.search_web(
                query, max_results=configuration.max_search_results
            )
            results.extend(query_results)
        except Exception as e:
            # print(f"Error searching web for query '{query}': {str(e)}") # Removed for linting
            results.append(
                {
                    "search_date": datetime.now().isoformat(),
                    "source_link": f"https://search.example.com?q={query}",
                    "headline": f"Error searching web for: {query}",
                    "text": f"Error: {str(e)}",
                }
            )

    filename = save_to_csv(results, "web_search")
    state.search_results["web_search"] = results
    print(f"Web search results: {results}")

    return {
        "web_search_results": results,
        "next": "editor",  # Continue to editor node
    }


async def editor_node(state: State, config: RunnableConfig) -> Dict[str, Any]:
    """Node for editing and combining results."""
    # configuration = Configuration.from_context() # Removed for linting

    # Combine all search results
    all_results = []
    if "youtube_results" in state:
        all_results.extend(state.youtube_results)
    if "wikipedia_results" in state:
        all_results.extend(state.wikipedia_results)
    if "web_search_results" in state:
        all_results.extend(state.web_search_results)

    state.search_results = {
        "youtube": state.youtube_results if "youtube_results" in state else [],
        "wikipedia": state.wikipedia_results if "wikipedia_results" in state else [],
        "web_search": state.web_search_results if "web_search_results" in state else [],
    }
    print(f"Combined search results: {state.search_results}")

    # Remove duplicates
    unique_results = remove_duplicates(all_results)
    print(f"Unique results: {unique_results}")

    # Preprocess text content
    for result in unique_results:
        result["text"] = preprocess_text(result["text"])
        result["headline"] = preprocess_text(result["headline"])

    # Save processed results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{OUTPUT_DIR}/processed_results_{timestamp}.csv"

    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f, fieldnames=["search_date", "source_link", "headline", "text"]
        )
        writer.writeheader()
        writer.writerows(unique_results)

    return {
        "messages": state.messages + [AIMessage(content=f"Processed results saved to {filename}")],
        "processed_results": unique_results,
        "next": "publisher",
    }


async def publisher_node(state: State, config: RunnableConfig) -> Dict[str, Any]:
    """Node for publishing final results."""
    # Generate table of contents
    toc = generate_toc(state.processed_results)
    toc_file = save_materials_to_file(toc, "table_of_contents.md")

    # Generate discussion materials
    materials = generate_discussion_materials(state.processed_results)
    materials_file = save_materials_to_file(materials, "discussion_materials.md")

    return {
        "messages": state.messages
        + [
            AIMessage(
                content=f"Generated materials saved:\n- Table of Contents: {toc_file}\n- Discussion Materials: {materials_file}"
            )
        ],
        "next": "save_data",
    }


async def save_data_node(state: State, config: RunnableConfig) -> Dict[str, Any]:
    """Node for saving data."""
    return {
        "next": "__end__",
    }


# Define a new graph
builder = StateGraph(State, input=InputState, config_schema=Configuration)

# Add nodes to the graph
builder.add_node("router", router_node)
builder.add_node("query_processor", query_processor_node)
builder.add_node("search_router", search_router_node)
builder.add_node("youtube", youtuber_node)
builder.add_node("wikipedia", wikipedia_node)
builder.add_node("web_search", web_search_node)
builder.add_node("editor", editor_node)
builder.add_node("publisher", publisher_node)
builder.add_node("save_data", save_data_node)

# Set the entrypoint
builder.add_edge("__start__", "router")

def should_continue(state: State):
    return state.next

# Add edges
builder.add_conditional_edges(
    "router",
    should_continue,
    {
        "query_processor": "query_processor",
        "__end__": "__end__",
    },
)
builder.add_edge("query_processor", "search_router")

builder.add_edge("search_router", "youtube")
builder.add_edge("youtube", "wikipedia")
builder.add_edge("wikipedia", "web_search")

builder.add_edge("web_search", "editor")
builder.add_edge("editor", "publisher")
builder.add_edge("publisher", "save_data")
builder.add_edge("save_data", "__end__")

# Compile the graph
graph = builder.compile(name="Education Resource Searcher")