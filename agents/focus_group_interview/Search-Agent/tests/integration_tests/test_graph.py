from langchain_core.messages import HumanMessage

import pytest
from langsmith import unit

from react_agent import graph


@pytest.mark.asyncio
async def test_react_agent_simple_passthrough() -> None:
    res = await graph.ainvoke(
        {"messages": [HumanMessage(content="Who is the founder of LangChain?")]},
        {"configurable": {"system_prompt": "You are a helpful AI assistant."}},
    )

    assert any("harrison" in str(item.get("text", "")).lower() for item in res["processed_results"])
