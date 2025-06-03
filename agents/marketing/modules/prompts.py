"""프롬프트 템플릿 모듈

이 모듈은 LangChain 프롬프트 템플릿을 정의하고 반환하는 함수들을 포함합니다.
각 함수는 특정 작업에 맞는 프롬프트 템플릿을 생성합니다.
"""

from langchain_core.prompts import PromptTemplate

# 예시 함수들입니다. 참고용으로 남겨둡니다.

# def get_campaign_generation_prompt() -> PromptTemplate:
#     """
#     교육 마케팅 캠페인 생성을 위한 프롬프트 템플릿을 반환합니다.
#
#     이 프롬프트는 대상 청중, 제품 정보, 마케팅 채널, 캠페인 목표를 입력으로 받아
#     효과적인 교육 마케팅 캠페인을 생성하도록 설계되었습니다.
#
#     Returns:
#         PromptTemplate: 캠페인 생성을 위한 프롬프트 템플릿
#     """
#     template = """
#     당신은 교육 분야의 마케팅 전략 전문가입니다.
#     아래 정보를 바탕으로 효과적인 교육 마케팅 캠페인을 개발해주세요.
#
#     # 대상 청중
#     {target_audience}
#
#     # 제품/서비스 정보
#     이름: {product_name}
#     설명: {product_description}
#
#     # 마케팅 채널
#     {marketing_channels}
#
#     # 캠페인 목표
#     {campaign_goals}
#
#     # 지침
#     - 교육적 가치와 학습 효과를 강조하는 캠페인을 개발하세요.
#     - 대상 청중의 요구와 관심사에 맞춘 전략을 구성하세요.
#     - 지정된 마케팅 채널에 적합한 접근 방식을 제안하세요.
#     - 캠페인 목표를 달성하기 위한 구체적인 전략을 포함하세요.
#     - 교육 분야의 최신 트렌드를 고려하세요.
#
#     다음 JSON 형식으로 캠페인 정보를 반환해주세요:
#     ```json
#     {
#       "campaign_name": "캠페인 이름",
#       "campaign_strategy": "캠페인 전략 개요",
#       "key_messages": ["핵심 메시지 1", "핵심 메시지 2", ...],
#       "timeline": "캠페인 타임라인",
#       "success_metrics": ["성공 지표 1", "성공 지표 2", ...]
#     }
#     ```
#     """
#     return PromptTemplate.from_template(template)
#
#
# def get_content_creation_prompt() -> PromptTemplate:
#     """
#     마케팅 콘텐츠 생성을 위한 프롬프트 템플릿을 반환합니다.
#
#     이 프롬프트는 대상 청중, 제품 정보, 마케팅 채널, 캠페인 전략을 입력으로 받아
#     효과적인 마케팅 콘텐츠를 생성하도록 설계되었습니다.
#
#     Returns:
#         PromptTemplate: 콘텐츠 생성을 위한 프롬프트 템플릿
#     """
#     template = """
#     당신은 교육 분야의 마케팅 콘텐츠 전문가입니다.
#     아래 정보를 바탕으로 효과적인 마케팅 콘텐츠를 생성해주세요.
#
#     # 대상 청중
#     {target_audience}
#
#     # 제품/서비스 정보
#     이름: {product_name}
#     설명: {product_description}
#
#     # 마케팅 채널
#     {marketing_channels}
#
#     # 캠페인 전략
#     {messages}
#
#     # 지침
#     - 각 마케팅 채널에 적합한 형식과 톤으로 콘텐츠를 작성하세요.
#     - 교육적 가치와 학습 효과를 강조하는 메시지를 포함하세요.
#     - 대상 청중의 요구와 관심사에 맞춘 콘텐츠를 개발하세요.
#     - 행동 유도(Call to Action)를 명확하게 포함하세요.
#     - 교육 분야의 전문성을 보여주는 언어와 표현을 사용하세요.
#
#     다음 구조로 각 마케팅 채널별 콘텐츠를 작성해주세요:
#
#     ## [채널 이름] 콘텐츠
#     (해당 채널에 적합한 콘텐츠)
#
#     ## [채널 이름] 콘텐츠
#     (해당 채널에 적합한 콘텐츠)
#
#     ...
#     """
#     return PromptTemplate.from_template(template)


def summary_doc_prompt() -> PromptTemplate:
    template = """
        다음 문서를 확인하고 정리해줘.
        문서의 핵심 요약과, 주요 질문사항을 포함하여 정리해줘.
        {text}
    """
    return PromptTemplate(template=template, input_variables=["text"])


def get_write_contents_prompt() -> PromptTemplate:
    template = """
        너는 블로그 글을 쓰는 컨텐츠팀에서 근무하고 있어.
        아래 내용을 확인하고 ux research에 관련된 블로그 컨텐츠를 작성해줘
        입력: {document_summary}

        중요 조건:
        - 다양한 사람들이 이해할 수 있도록 쉽게 써야 해.
        - 노션에 글을 쓸거야. 마크다운 문법과 아이콘을 활용해서 눈에 잘 띄는 컨텐츠를 만들어줘.
    """
    return PromptTemplate.from_template(template)


def notion_page_creation_prompt() -> PromptTemplate:
    template = """
        너는 노션 페이지를 만들어야 해. 주어진 입력에 대해서 JSON body를 만들어줘.
        입력: {page_content}

        중요 조건:
        - 절대 간단한 요약 JSON을 출력하지 마. 반드시 Notion API의 완전한 JSON 구조를 따라야 해.
        - 결과는 JSON 형태로만 출력해줘. 대신 제일 처음과 끝에 코드 블록(```json)은 절대 붙이지 마.**
        - 임의로 내용을 요약하지 마. 있는 내용 그대로를 포함하는 JSON을 만들어야 해.
        - children의 paragraph 속성 아래에 'rich_text'를 반드시 넣어야 해.
        - 글의 내용은 children 아래에 여러 블록으로 적절하게 나뉘어야 해.
        - 아래는 JSON 예시야 사용자 입력을 바탕으로 해당 JSON 내용을 채워줘. JSON의 형태는 엄격하게 검증해줘.
        ```
        "parent": {{ "page_id": "부모 페이지 ID" }},
        "properties": {{
            "title": [
                {{
                    "type": "text",
                    "text": {{
                    "content": "페이지 제목"
                    }}
                }}
            ]
        }},
        "children": [
            {{
                "object": "block",
                "type": "paragraph",
                "paragraph": {{
                    "rich_text": [
                        {{
                            "type": "text",
                            "text": {{
                                "content": "문단 내용"
                            }}
                        }}
                    ]
                }}
            }}
        ]
        ```
    """
    return PromptTemplate.from_template(template)
