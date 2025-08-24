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

###
# graph 선언
###

def ux_researcher_generator_node(state: MessagesState):

    response = ux_researcher_agent.invoke({
        "info": [str(persona_data["UX 리서처"])],
        "messages": state["messages"],
        # "knowledge": [""]
    })
    
    return {"messages" : [response]}

def uxui_designer_generator_node(state: MessagesState):

    response = uxui_designer_agent.invoke({
        "info": [str(persona_data["UXUI_디자이너"])],
        "messages": state["messages"],
        # "knowledge": [""]
    })
    
    return {"messages" : [response]}

def pm_generator_node(state: MessagesState):

    response = pm_agent.invoke({
        "info": [str(persona_data["PM (프로덕트 매니저)"])],
        "messages": state["messages"],
        # "knowledge": [""]
    })
    
    return {"messages" : [response]}

def should_continue(state: MessagesState) -> str:

    if len(state["messages"]) >= 10:
        return END
    
    else:
        chosen_agent = random.choice(["UX 리서처", "UXUI 디자이너", "PM (프로덕트 매니저)"])

        return chosen_agent

def setup_runnable():
    builder = StateGraph(MessagesState)
    builder.add_node("UX 리서처", ux_researcher_generator_node)
    builder.add_node("UXUI 디자이너", uxui_designer_generator_node)
    builder.add_node("PM (프로덕트 매니저)", pm_generator_node)
    builder.add_edge(START, "UX 리서처")
    builder.add_conditional_edges("UX 리서처", should_continue)
    builder.add_conditional_edges("UXUI 디자이너", should_continue)
    builder.add_conditional_edges("PM (프로덕트 매니저)", should_continue)

    return builder.compile()

normal_graph = setup_runnable()


