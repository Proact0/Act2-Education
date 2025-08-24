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

###
# 페르소나 정보
###

with open("../person/persona.json", 'r', encoding='utf-8') as f:
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

###
# agent 선언
###

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

######

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

######

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

######

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

######

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

###
# graph 선언
###

def problem_definition_node(state: MessagesState):
    # 문제정의: 주제 제시 (모더레이터)
    response = moderator_1_agent.invoke({
        "info": [str(persona_data["모더레이터 01"])],
        "messages": state["messages"],
    })
    return {"messages": state["messages"] + [response], "step": "관점제시"}

def perspective_node(state: MessagesState):
    # 관점제시: 3명 전문가 관점 + 모더레이터 요약
    messages = state["messages"]
    for key, agent in [("UX 리서처", ux_researcher_agent), ("UXUI_디자이너", uxui_designer_agent), ("PM (프로덕트 매니저)", pm_agent)]:
        response = agent.invoke({
            "info": [str(persona_data[key])],
            "messages": messages,
        })
        messages.append(response)
    # 모더레이터 요약
    mod_response = moderator_1_agent.invoke({
        "info": [str(persona_data["모더레이터 01"])],
        "messages": messages,
    })
    messages.append(mod_response)
    return {"messages": messages, "step": "상호질의"}

def discussion_node(state: MessagesState):
    # 상호질의: 전문가 자유토론 + 모더레이터 요약
    messages = state["messages"]
    for key, agent in [("UX 리서처", ux_researcher_agent), ("UXUI_디자이너", uxui_designer_agent), ("PM (프로덕트 매니저)", pm_agent)]:
        response = agent.invoke({
            "info": [str(persona_data[key])],
            "messages": messages,
        })
        messages.append(response)
    mod_response = moderator_1_agent.invoke({
        "info": [str(persona_data["모더레이터 01"])],
        "messages": messages,
    })
    messages.append(mod_response)
    return {"messages": messages, "step": "합의도출"}

def consensus_node(state: MessagesState):
    # 합의도출: 전문가 자유토론 + 모더레이터 요약
    messages = state["messages"]
    for key, agent in [("UX 리서처", ux_researcher_agent), ("UXUI_디자이너", uxui_designer_agent), ("PM (프로덕트 매니저)", pm_agent)]:
        response = agent.invoke({
            "info": [str(persona_data[key])],
            "messages": messages,
        })
        messages.append(response)
    mod_response = moderator_1_agent.invoke({
        "info": [str(persona_data["모더레이터 01"])],
        "messages": messages,
    })
    messages.append(mod_response)
    return {"messages": messages, "step": "실행방안"}

def action_plan_node(state: MessagesState):
    # 실행방안: 전문가 자유토론 + 모더레이터 결론
    messages = state["messages"]
    for key, agent in [("UX 리서처", ux_researcher_agent), ("UXUI_디자이너", uxui_designer_agent), ("PM (프로덕트 매니저)", pm_agent)]:
        response = agent.invoke({
            "info": [str(persona_data[key])],
            "messages": messages,
        })
        messages.append(response)
    mod_response = moderator_1_agent.invoke({
        "info": [str(persona_data["모더레이터 01"])],
        "messages": messages,
    })
    messages.append(mod_response)
    return {"messages": messages, "step": "END"}

def should_continue(state: MessagesState):
    step = state.get("step", "문제정의")
    if step == "문제정의":
        return "관점제시"
    elif step == "관점제시":
        return "상호질의"
    elif step == "상호질의":
        return "합의도출"
    elif step == "합의도출":
        return "실행방안"
    else:
        return END

# 그래프 빌드
def setup_meeting_graph():
    builder = StateGraph(MessagesState)
    builder.add_node("문제정의", problem_definition_node)
    builder.add_node("관점제시", perspective_node)
    builder.add_node("상호질의", discussion_node)
    builder.add_node("합의도출", consensus_node)
    builder.add_node("실행방안", action_plan_node)
    builder.add_edge(START, "문제정의")
    builder.add_conditional_edges("문제정의", should_continue)
    builder.add_conditional_edges("관점제시", should_continue)
    builder.add_conditional_edges("상호질의", should_continue)
    builder.add_conditional_edges("합의도출", should_continue)
    builder.add_conditional_edges("실행방안", should_continue)
    return builder.compile()

sequence_graph = setup_meeting_graph()