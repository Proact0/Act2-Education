"""LLM 모델 설정 모듈

이 모듈은 LangChain에서 사용할 LLM 모델을 설정하고 반환하는 함수들을 포함합니다.
"""

import os

from langchain_openai import ChatOpenAI


def get_openai_model(
    model_name: str = "gpt-3.5-turbo", temperature: float = 0.7, max_tokens: int = 4000
) -> ChatOpenAI:
    """
    OpenAI 모델 인스턴스를 생성하고 반환합니다.

    이 함수는 교육 마케팅 관련 작업에 적합한 설정으로
    OpenAI의 ChatGPT 모델을 초기화합니다.

    Returns:
        ChatOpenAI: 초기화된 OpenAI 모델 인스턴스
    """
    return ChatOpenAI(
        api_key=os.environ["OPENAI_API_KEY"],
        model_name=model_name,  # 모델 이름 (gpt-4 사용)
        temperature=temperature,  # 창의성 조절 (0.7은 균형 잡힌 창의성)
        max_tokens=max_tokens,  # 최대 토큰 수
    )
