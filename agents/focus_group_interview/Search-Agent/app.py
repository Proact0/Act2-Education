"""Streamlit UI for the Education Resource Search Agent."""

import asyncio

import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage

from react_agent.graph import graph

st.title("Education Resource Search Agent")


topic = st.text_input("Enter the educational topic you want to learn about:")


if st.button("Start Learning"):
    if topic:
        st.session_state.log = []
        st.session_state.log.append(f"Starting agent for topic: {topic}")

        with st.spinner("Agent is working..."):

            async def run_agent():
                """Run the agent asynchronously and update the log."""
                async for s in graph.astream({"messages": [("user", topic)]}):
                    st.session_state.log.append(s)

            asyncio.run(run_agent())

        # After the agent run completes, update the UI
        st.rerun()


if "log" in st.session_state:
    st.subheader("Agent Activity")
    for message in st.session_state.log:
        if isinstance(message, str):
            st.write(message)
        elif isinstance(message, dict):
            # Extract relevant information from the state dictionary
            if "messages" in message and message["messages"]:
                last_msg = message["messages"][-1]
                if isinstance(last_msg, AIMessage):
                    st.write(f"AI: {last_msg.content}")
                elif isinstance(last_msg, HumanMessage):
                    st.write(f"User: {last_msg.content}")
            if "queries" in message and message["queries"]:
                st.write(f"Generated queries: {', '.join(message['queries'])}")
            if "search_results" in message and message["search_results"]:
                st.write(
                    f"Search results collected from: {', '.join(message['search_results'].keys())}"
                )
            if (
                "processed_results" in message
                and message["processed_results"] is not None
            ):
                st.write(f"Processed {len(message['processed_results'])} documents.")
            if "__end__" in message:
                processed_results = message.get("processed_results", [])
                st.success(
                    f"Agent finished! Collected {len(processed_results)} documents."
                )

                # Display the generated materials
                st.subheader("Generated Materials")
                try:
                    with open("generated_materials/table_of_contents.md") as f:
                        st.markdown("### Table of Contents")
                        st.markdown(f.read())
                except FileNotFoundError:
                    st.warning("Table of Contents not found.")

                try:
                    with open("generated_materials/discussion_materials.md") as f:
                        st.markdown("### Discussion Materials")
                        st.markdown(f.read())
                except FileNotFoundError:
                    st.warning("Discussion Materials not found.")
        else:
            st.write(message)  # Fallback for unexpected message types
