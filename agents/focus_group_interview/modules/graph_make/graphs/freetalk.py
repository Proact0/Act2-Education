import os
import json
import random
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langgraph.graph import MessagesState, END
from langgraph.graph import StateGraph, START

load_dotenv()

"""
knowledge 부분은 추후 search 부분과 연결
"""

# 페르소나 정보
with open("./persona/persona.json", 'r', encoding='utf-8') as f:
    persona_data = json.load(f)

moderator_1_prompt = persona_data['모더레이터 01']
moderator_2_prompt = persona_data['모더레이터 02']
ux_researcher_prompt = persona_data['UX 리서처']
uxui_designer_prompt = persona_data['UXUI_디자이너']
pm_prompt = persona_data['PM (프로덕트 매니저)']

moderator_1_role = persona_data['모더레이터 01']['role']
moderator_2_role = persona_data['모더레이터 02']['role']
ux_researcher_role = persona_data['UX 리서처']['role']
uxui_designer_role = persona_data['UXUI_디자이너']['role']
pm_role = persona_data['PM (프로덕트 매니저)']['role']

MODEL = "gpt-4.1-mini"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

ux_researcher = ChatOpenAI(
    model=MODEL,
    openai_api_key=OPENAI_API_KEY
)

ux_researcher_prompt = ChatPromptTemplate.from_messages([
    "system",
    f"""
info는 당신에 대한 정보 입니다.

대화의 주제를 기준으로 다른 agent와 토론을 진행하세요
    """,
    MessagesPlaceholder(variable_name="info"),
    MessagesPlaceholder(variable_name="messages"),
    # MessagesPlaceholder(variable_name="knowledge"),
])

ux_researcher_agent = ux_researcher_prompt | ux_researcher

uxui_designer = ChatOpenAI(
    model=MODEL,
    openai_api_key=OPENAI_API_KEY
)

uxui_designer_prompt = ChatPromptTemplate.from_messages([
    "system",
    f"""
info는 당신에 대한 정보 입니다.

대화의 주제를 기준으로 다른 agent와 토론을 진행하세요
    """,
    MessagesPlaceholder(variable_name="info"),
    MessagesPlaceholder(variable_name="messages"),
    # MessagesPlaceholder(variable_name="knowledge"),
])

uxui_designer_agent = uxui_designer_prompt | uxui_designer

pm = ChatOpenAI(
    model=MODEL,
    openai_api_key=OPENAI_API_KEY
)

pm_prompt = ChatPromptTemplate.from_messages([
    "system",
    f"""
info는 당신에 대한 정보 입니다.

대화의 주제를 기준으로 다른 agent와 토론을 진행하세요
    """,
    MessagesPlaceholder(variable_name="info"),
    MessagesPlaceholder(variable_name="messages"),
    # MessagesPlaceholder(variable_name="knowledge"),
])

pm_agent = pm_prompt | pm

moderator_1 = ChatOpenAI(
    model=MODEL,
    openai_api_key=OPENAI_API_KEY
)

moderator_1_prompt = ChatPromptTemplate.from_messages([
    "system",
    f"""
info는 당신에 대한 정보 입니다.

대화의 주제를 기준으로 다른 agent와 토론을 진행하세요
    """,
    MessagesPlaceholder(variable_name="info"),
    MessagesPlaceholder(variable_name="messages"),
    # MessagesPlaceholder(variable_name="knowledge"),
])

moderator_1_agent = moderator_1_prompt | moderator_1

moderator_2 = ChatOpenAI(
    model=MODEL,
    openai_api_key=OPENAI_API_KEY
)

moderator_2_prompt = ChatPromptTemplate.from_messages([
    "system",
    f"""
info는 당신에 대한 정보 입니다.

대화의 주제를 기준으로 다른 agent와 토론을 진행하세요
    """,
    MessagesPlaceholder(variable_name="info"),
    MessagesPlaceholder(variable_name="messages"),
    # MessagesPlaceholder(variable_name="knowledge"),
])

moderator_2_agent = moderator_2_prompt | moderator_2

# 자유토론 노드 예시 (자유롭게 토론하며 메시지 누적)
def freetalk_node(state: MessagesState):
    messages = state["messages"]
    # 랜덤으로 한 명이 발언
    agent_key, agent = random.choice([
        ("UX 리서처", ux_researcher_agent),
        ("UXUI_디자이너", uxui_designer_agent),
        ("PM (프로덕트 매니저)", pm_agent)
    ])
    response = agent.invoke({
        "info": [str(persona_data[agent_key])],
        "messages": messages,
    })
    messages.append(response)
    return {"messages": messages, "step": state.get("step", "자유토론"), "turn": state.get("turn", 0) + 1}

# 모더레이터가 체크리스트 평가 후 종료 조건 판단
def moderator_check_node(state: MessagesState):
    messages = state["messages"]
    response = moderator_1_agent.invoke({
        "info": [str(persona_data["모더레이터 01"])],
        "messages": messages,
    })
    messages.append(response)
    # 예시: 5턴 이상이면 종료
    if state.get("turn", 0) >= 5:
        return {"messages": messages, "step": "종료"}
    return {"messages": messages, "step": "자유토론", "turn": state.get("turn", 0)}

# 다음 단계 결정
def should_continue(state: MessagesState):
    if state.get("step") == "종료":
        return END
    # 2턴마다 모더레이터 체크
    if state.get("turn", 0) % 2 == 0:
        return "모더레이터 체크"
    return "자유토론"

# 그래프 빌드
def setup_freetalk_graph():
    builder = StateGraph(MessagesState)
    builder.add_node("자유토론", freetalk_node)
    builder.add_node("모더레이터 체크", moderator_check_node)
    builder.add_edge(START, "자유토론")
    builder.add_conditional_edges("자유토론", should_continue)
    builder.add_conditional_edges("모더레이터 체크", should_continue)
    return builder.compile()

freetalk_graph = setup_freetalk_graph()