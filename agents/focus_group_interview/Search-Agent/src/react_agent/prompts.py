"""Default prompts used by the agent."""

SYSTEM_PROMPT = """You are an educational resource search assistant that helps find and organize learning materials.

System time: {system_time}"""

TOPIC_VALIDATION_PROMPT = """Given the following topic, determine if it's a valid topic for a search.

Topic: {topic}

Respond with either 'VALID' or 'INVALID' followed by a brief explanation."""

QUERY_GENERATION_PROMPT = """Generate 5 search queries for the topic: {topic}
Output format: Each query on a new line with a number prefix (1., 2., etc.). Do not include any other text or explanations."""

RESULT_COMBINATION_PROMPT = """Given the following search results from different sources, combine and organize them into a coherent educational resource.
Consider:
1. Relevance to the original topic
2. Quality and reliability of sources
3. Different perspectives and viewpoints
4. Educational value and depth

Topic: {topic}
Search Results:
{results}

Provide a structured summary that includes:
1. Key findings
2. Different perspectives
3. Educational value
4. Recommended resources"""
