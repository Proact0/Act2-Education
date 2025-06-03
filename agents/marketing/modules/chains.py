"""LangChain 체인을 설정하는 함수 모듈

LCEL(LangChain Expression Language)을 사용하여 체인을 구성합니다.
기본적으로 modules.prompt 템플릿과 modules.models 모듈을 사용하여 LangChain 체인을 생성합니다.
"""

from langchain.chains.summarize import load_summarize_chain
from langchain.schema.runnable import RunnableSerializable  # , RunnablePassthrough
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser

from agents.marketing.modules.models import get_openai_model
from agents.marketing.modules.prompts import (
    get_write_contents_prompt,
    notion_page_creation_prompt,
    summary_doc_prompt,
)

# from langchain_core.pydantic_v1 import BaseModel, Field


# 예시 함수들입니다. 참고용으로 남겨둡니다.

# class MarketingCampaign(BaseModel):
#     """마케팅 캠페인을 위한 Pydantic 모델"""
#     campaign_name: str = Field(description="마케팅 캠페인 이름")
#     campaign_strategy: str = Field(description="마케팅 캠페인 전략 개요")
#     key_messages: List[str] = Field(description="핵심 마케팅 메시지 목록")
#     timeline: str = Field(description="캠페인 타임라인")
#     success_metrics: List[str] = Field(description="성공 지표 목록")


# def set_campaign_generation_chain() -> RunnableSerializable:
#     """
#     마케팅 캠페인 생성에 사용할 LangChain 체인을 생성합니다.
#
#     이 함수는 LCEL(LangChain Expression Language)을 사용하여 체인을 구성합니다.
#     체인은 다음 단계로 구성됩니다:
#     1. 입력에서 target_audience, product_name, product_description 등을 추출하여 프롬프트에 전달
#     2. 프롬프트 템플릿에 값을 삽입하여 최종 프롬프트 생성
#     3. LLM을 호출하여 마케팅 캠페인 생성 수행
#     4. 결과를 JSON으로 파싱하여 캠페인 정보 반환
#
#     Returns:
#         RunnableSerializable: 실행 가능한 체인 객체
#     """
#     # 캠페인 생성을 위한 프롬프트 가져오기
#     prompt = get_campaign_generation_prompt()
#     # OpenAI 모델 가져오기
#     model = get_openai_model()
#     # JSON 출력 파서 설정
#     parser = JsonOutputParser(pydantic_object=MarketingCampaign)
#
#     # LCEL을 사용하여 체인 구성
#     return (
#         # 입력에서 필요한 필드 추출 및 프롬프트에 전달
#         RunnablePassthrough.assign(
#             target_audience=lambda x: x["target_audience"],  # 대상 청중 추출
#             product_name=lambda x: x["product_name"],  # 제품/서비스 이름 추출
#             product_description=lambda x: x["product_description"],  # 제품/서비스 설명 추출
#             marketing_channels=lambda x: x["marketing_channels"],  # 마케팅 채널 추출
#             campaign_goals=lambda x: x["campaign_goals"],  # 캠페인 목표 추출
#         )
#         | prompt  # 프롬프트 적용
#         | model  # LLM 모델 호출
#         | parser  # 결과를 JSON으로 파싱
#     )


# def set_content_creation_chain() -> RunnableSerializable:
#     """
#     마케팅 콘텐츠 생성에 사용할 LangChain 체인을 생성합니다.
#
#     이 함수는 LCEL(LangChain Expression Language)을 사용하여 체인을 구성합니다.
#     체인은 다음 단계로 구성됩니다:
#     1. 입력에서 target_audience, product_name, marketing_channels 등을 추출하여 프롬프트에 전달
#     2. 프롬프트 템플릿에 값을 삽입하여 최종 프롬프트 생성
#     3. LLM을 호출하여 마케팅 콘텐츠 생성 수행
#     4. 결과를 문자열로 변환
#
#     Returns:
#         RunnableSerializable: 실행 가능한 체인 객체
#     """
#     # 콘텐츠 생성을 위한 프롬프트 가져오기
#     prompt = get_content_creation_prompt()
#     # OpenAI 모델 가져오기
#     model = get_openai_model()
#
#     # LCEL을 사용하여 체인 구성
#     return (
#         # 입력에서 필요한 필드 추출 및 프롬프트에 전달
#         RunnablePassthrough.assign(
#             target_audience=lambda x: x["target_audience"],  # 대상 청중 추출
#             product_name=lambda x: x["product_name"],  # 제품/서비스 이름 추출
#             product_description=lambda x: x["product_description"],  # 제품/서비스 설명 추출
#             marketing_channels=lambda x: x["marketing_channels"],  # 마케팅 채널 추출
#             messages=lambda x: x["messages"],  # 이전 메시지 추출 (캠페인 전략 포함)
#         )
#         | prompt  # 프롬프트 적용
#         | model  # LLM 모델 호출
#         | StrOutputParser()  # 결과를 문자열로 변환
#     )


def map_reduce_summary_chain() -> RunnableSerializable:
    """
    Map Reduce 방식으로 문서를 나누어서 각각을 요약한 뒤 모두 합쳐서 한번 더 요약합니다.
    """
    model = get_openai_model()
    prompt = summary_doc_prompt()
    chain = load_summarize_chain(
        llm=model, chain_type="map_reduce", map_prompt=prompt, combine_prompt=prompt
    )
    return chain


def stuff_summary_chain() -> RunnableSerializable:
    """
    문서를 한번에 보고 요약합니다.
    """
    model = get_openai_model()
    prompt = summary_doc_prompt()
    chain = load_summarize_chain(
        llm=model,
        chain_type="stuff",
        prompt=prompt,
    )
    return chain


def write_blog_content_chain() -> RunnableSerializable:
    model = get_openai_model()
    prompt = get_write_contents_prompt()

    return prompt | model | StrOutputParser()


def create_notion_page_chain() -> RunnableSerializable:
    model = get_openai_model()
    prompt = notion_page_creation_prompt()

    return prompt | model | JsonOutputParser()
