"""
노드 클래스 모듈

이 모듈은 LangGraph Workflow에서 사용되는 마케팅 관련 노드 클래스들을 정의합니다.
각 노드 클래스는 BaseNode를 상속받아 구현되며, Workflow 그래프에서 특정 기능을 수행하는 단위 컴포넌트입니다.
각 노드는 execute 메서드를 구현하여 상태(state)를 입력받아 처리하고, 처리 결과를 새로운 상태 업데이트로 반환합니다.
"""

import os

import requests
from langchain_core.documents import Document

from agents.base_node import BaseNode
from agents.marketing.modules.chains import (
    create_notion_page_chain,
    map_reduce_summary_chain,
    stuff_summary_chain,
    write_blog_content_chain,
)
from agents.marketing.modules.state import ContentState
from agents.marketing.modules.utils import load_pdf_documents

# 아래는 구현 예정인 노드 클래스들입니다. 실제 구현 시 주석을 해제하고 사용하면 됩니다.

# class CampaignGenerationNode(BaseNode):
#     """
#     교육 제품/서비스에 적합한 마케팅 캠페인을 생성하는 노드
#
#     이 노드는 LangChain의 캠페인 생성 체인을 활용하여 교육 제품이나 서비스에 적합한 마케팅 전략을 생성합니다.
#     대상 청중, 제품 정보, 캠페인 목표 등을 고려하여 전략을 수립하고 Workflow의 다음 단계로 전달합니다.
#     """
#
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)  # BaseNode 초기화
#         # set_campaign_generation_chain 함수를 통해 LangChain 체인을 가져와 설정
#         self.chain = set_campaign_generation_chain()  # 캠페인 생성 체인 설정
#
#     def execute(self, state) -> dict:
#         """
#         주어진 상태(state)에서 필요한 정보를 추출하여 캠페인 전략을 생성하고 결과를 반환합니다.
#
#         Args:
#             state (dict): Workflow의 현재 상태. target_audience, product_name, product_description 등의 정보를 포함함.
#
#         Returns:
#             dict: 생성된 캠페인 전략을 포함한 상태 업데이트
#         """
#         # 캠페인 생성 체인 실행 - LLM을 통해 캠페인 전략 생성
#         campaign_strategy = self.chain.invoke(
#             {
#                 "target_audience": state["target_audience"],  # 대상 청중
#                 "product_name": state["product_name"],  # 제품/서비스 이름
#                 "product_description": state["product_description"],  # 제품/서비스 설명
#                 "marketing_channels": state["marketing_channels"],  # 마케팅 채널
#                 "campaign_goals": state["campaign_goals"],  # 캠페인 목표
#             }
#         )
#
#         # 생성된 캠페인 전략을 새로운 상태 업데이트로 반환
#         return {"messages": campaign_strategy}
#
#
# class ContentCreationNode(BaseNode):
#     """
#     마케팅 캠페인에 필요한 콘텐츠를 생성하는 노드
#
#     이 노드는 LangChain의 콘텐츠 생성 체인을 활용하여 마케팅 캠페인에 필요한 다양한 콘텐츠를 생성합니다.
#     이전 단계에서 생성된 캠페인 전략을 기반으로 각 마케팅 채널에 적합한 콘텐츠를 생성하여 Workflow의 다음 단계로 전달합니다.
#     """
#
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)  # BaseNode 초기화
#         # set_content_creation_chain 함수를 통해 LangChain 체인을 가져와 설정
#         self.chain = set_content_creation_chain()  # 콘텐츠 생성 체인 설정
#
#     def execute(self, state) -> dict:
#         """
#         주어진 상태(state)에서 필요한 정보를 추출하여 마케팅 콘텐츠를 생성하고 결과를 반환합니다.
#
#         Args:
#             state (dict): Workflow의 현재 상태. target_audience, product_name, marketing_channels, messages 등의 정보를 포함함.
#
#         Returns:
#             dict: 생성된 마케팅 콘텐츠를 포함한 상태 업데이트
#         """
#         # 콘텐츠 생성 체인 실행 - LLM을 통해 마케팅 콘텐츠 생성
#         marketing_content = self.chain.invoke(
#             {
#                 "target_audience": state["target_audience"],  # 대상 청중
#                 "product_name": state["product_name"],  # 제품/서비스 이름
#                 "product_description": state["product_description"],  # 제품/서비스 설명
#                 "marketing_channels": state["marketing_channels"],  # 마케팅 채널
#                 "messages": state["messages"],  # 이전 메시지 (캠페인 전략 포함)
#             }
#         )
#
#         # 생성된 마케팅 콘텐츠를 새로운 상태 업데이트로 반환
#         return {"messages": marketing_content}


class DocSummarizationNode(BaseNode):
    """
    문서를 요약해주는 노드

    필요에따라 map reduce 방식, stuff 방식 혹은 둘 모두를 사용하여 문서를 요약하여 state에 추가합니다.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.map_reduce_summary_chain = map_reduce_summary_chain()
        self.stuff_summary_chain = stuff_summary_chain()

    def load_pdf(self, input_file: str) -> list[Document]:
        return load_pdf_documents(input_file)

    def execute(self, state: ContentState) -> dict:
        """
        주어진 상태(state)에 포함된 문서명(str)을 가지고 문서를 열람한 뒤 요약합니다.

        llm의 버전에 따라 다르지만 gpt기준 토큰 수 제한이 있어 map reduce를 먼저 수행한 뒤 stuff로 한번 더 요약합니다.

        Args:
            state (ContentState): Workflow의 현재 상태. input_file 정보를 포함.

        Returns:
            dict: 요약된 문서를 포함한 상태 업데이트
        """
        # TODO: pdf 외의 다른 입력도 고려하여 분기를 만들지?

        interview_doc = self.load_pdf(state.get("input_file"))

        document_summary = self.map_reduce_summary_chain.invoke(interview_doc)
        document_summary = self.stuff_summary_chain.invoke(document_summary)
        return {"document_summary": document_summary}


class NotionWritingNode(BaseNode):
    """
    노션 컨텐츠 작성 및 업로드 노드

    제공받은 문서(또는 요약)을 바탕으로 Notion에 게시할 블로그 컨텐츠를 작성합니다.
    작성한 컨텐츠는 Notion API를 사용해 게시합니다.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.write_content_chain = write_blog_content_chain()
        self.create_page_chain = create_notion_page_chain()
        self.parent_id = os.environ["NOTION_PARENT_ID"]
        self.api_key = os.environ["NOTION_API_KEY"]

    def create_page(self, payload: dict) -> str:
        # TODO: retry 코드 추가 필요

        payload["parent"] = {"page_id": self.parent_id}

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28",
        }

        res = requests.post(
            "https://api.notion.com/v1/pages", headers=headers, json=payload
        )

        if res.status_code == 200:
            return "success ✅"
        else:
            return f"failed ❌: {res.status_code}, {res.text}"

    def execute(self, state: ContentState) -> dict:
        """
        주어진 상태(state)의 문서 요약을 바탕으로 블로그 컨텐츠를 작성합니다.
        이후 작성한 컨텐츠를 json형태로 바꾸어 notion api를 통해 notion에 게시합니다.

        Args:
            state (ContentState): Workflow의 현재 상태. input_file 정보를 포함.

        Returns:
            dict: 생성된 블로그 콘텐츠를 포함한 상태 업데이트
        """
        page_content = self.write_content_chain.invoke(
            {"document_summary": state["document_summary"]}
        )
        output_json = self.create_page_chain.invoke({"page_content": page_content})
        # output_str = re.sub(r"```json|```", "", output_str).strip() # TODO: 필요한지 검증

        results = self.create_page(output_json)

        return {
            "page_content": page_content,
            "results": results,
        }
