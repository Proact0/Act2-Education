from __future__ import annotations

from dataclasses import dataclass
from typing import Annotated, List, Optional, TypedDict

from langchain_core.messages import AIMessage, HumanMessage
from langgraph.graph.message import add_messages


@dataclass
class MarketingState(TypedDict):
    """
    마케팅 Workflow의 상태를 정의하는 TypedDict 클래스

    교육 콘텐츠 마케팅을 위한 Workflow에서 사용되는 상태 정보를 정의합니다.
    LangGraph의 상태 관리를 위한 클래스로, Workflow 내에서 처리되는 데이터의 형태와 구조를 지정합니다.

    아래는 예시 상태 변수들입니다. 실제 구현 시 필요에 따라 수정해서 사용해주세요!
    """

    target_audience: str  # 대상 청중 (예: "고등학생", "대학생", "직장인")
    product_name: str  # 교육 제품/서비스 이름
    product_description: str  # 교육 제품/서비스 설명
    marketing_channels: List[
        str
    ]  # 마케팅 채널 목록 (예: "소셜 미디어", "이메일", "블로그")
    campaign_goals: List[str]  # 캠페인 목표 목록
    messages: Annotated[List[HumanMessage | AIMessage], add_messages]  # 메시지 목록
    # Annotated는 Python 타입 어노테이션으로, add_messages는 LangGraph에서 사용하는 특별한 함수입니다.
    # add_messages는 메시지 목록에 새로운 메시지를 추가할 때 이전 메시지를 유지하면서 추가하는 기능을 자동으로 처리합니다.


@dataclass
class ContentState(TypedDict):
    input_file: str
    document_summary: Optional[str]
    content: Optional[str]
    result: Optional[str]
