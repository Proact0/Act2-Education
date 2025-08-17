"""Define the state structures for the agent."""

from __future__ import annotations

from typing import Dict, List, Optional

from langchain_core.messages import BaseMessage
from pydantic import BaseModel, Field


class InputState(BaseModel):
    """Input state for the agent."""

    messages: List[BaseMessage]
    original_topic: Optional[str] = None


class State(InputState):
    """State for the education resource search agent."""

    queries: Optional[List[str]] = None
    youtube_results: Optional[List[Dict[str, str]]] = Field(default_factory=list)
    wikipedia_results: Optional[List[Dict[str, str]]] = Field(default_factory=list)
    web_search_results: Optional[List[Dict[str, str]]] = Field(default_factory=list)
    search_results: Dict[str, List[Dict[str, str]]] = Field(default_factory=dict)
    processed_results: Optional[List[Dict[str, str]]] = None
    next: str = ""  # Indicates the next node to be executed in the workflow
