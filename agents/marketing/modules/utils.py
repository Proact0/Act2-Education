"""
유틸리티 및 보조 함수 모듈

이 모듈은 교육 마케팅 Workflow에서 사용할 수 있는 다양한 유틸리티 함수를 제공합니다.
마케팅 캠페인 데이터 처리, 콘텐츠 포맷팅, 성과 분석 등에 필요한 유틸리티 함수들을 포함합니다.

아래는 예시 코드입니다. 참고용으로 남겨둡니다.
"""

# from typing import List, Dict, Any
# from langchain_core.messages import BaseMessage
# import re
# import json
# from datetime import datetime

from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document


def load_pdf_documents(
    file_path: str,
    chunk_size: int = 5000,
    chunk_overlap: int = 100,
) -> list[Document]:
    """
    PDF 파일을 로드하고, 지정된 크기로 텍스트를 분할한 후 Document 객체 리스트로 반환합니다.

    RecursiveCharacterTextSplitter를 통해 긴 텍스트를 여러 chunk로 나눕니다.
    각 chunk는 downstream LLM 처리에 적합한 길이로 유지됩니다.

    Args:
        file_path (str): 분할할 PDF 파일의 경로.
        chunk_size (int, optional): 각 chunk의 최대 문자 수.
        chunk_overlap (int, optional): 인접한 chunk 간 중복 문자 수.

    Returns:
        List[Document]: 분할된 문서 조각들의 리스트. 각 Document는 page_content와 metadata를 포함합니다.
    """
    loader = PyPDFLoader(file_path)
    documents = loader.load()
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap
    )
    return splitter.split_documents(documents)


# def get_message_text(msg: BaseMessage) -> str:
#     """메시지의 텍스트 내용을 가져옵니다."""
#     content = msg.content
#     if isinstance(content, str):
#         return content
#     elif isinstance(content, dict):
#         return content.get("text", "")
#     else:
#         txts = [c if isinstance(c, str) else (c.get("text") or "") for c in content]
#         return "".join(txts).strip()


# def format_marketing_content(
#     content: str,
#     platform: str,
#     character_limit: int = None
# ) -> str:
#     """
#     마케팅 콘텐츠를 특정 플랫폼에 맞게 포맷팅합니다.
#
#     Args:
#         content: 원본 마케팅 콘텐츠
#         platform: 대상 플랫폼 (예: "twitter", "instagram", "facebook", "linkedin")
#         character_limit: 문자 수 제한 (기본값: None)
#
#     Returns:
#         포맷팅된 콘텐츠
#     """
#     # 플랫폼별 기본 문자 제한
#     platform_limits = {
#         "twitter": 280,
#         "instagram": 2200,
#         "facebook": 63206,
#         "linkedin": 3000,
#         "email": 10000
#     }
#
#     # 문자 제한 설정
#     limit = character_limit or platform_limits.get(platform.lower(), None)
#
#     # 콘텐츠 포맷팅
#     formatted_content = content
#
#     # 플랫폼별 특수 포맷팅
#     if platform.lower() == "twitter":
#         # 해시태그 추출 및 최적화
#         hashtags = re.findall(r'#\w+', content)
#         # 본문에서 해시태그 제거
#         clean_content = re.sub(r'#\w+', '', content).strip()
#         # 문자 제한 고려하여 콘텐츠 자르기
#         if limit and len(clean_content) > limit - len(" ".join(hashtags)) - 1:
#             clean_content = clean_content[:limit - len(" ".join(hashtags)) - 4] + "..."
#         # 해시태그 추가
#         formatted_content = clean_content + "\n\n" + " ".join(hashtags)
#
#     elif platform.lower() == "instagram":
#         # 해시태그 최적화 및 줄바꿈 추가
#         hashtags = re.findall(r'#\w+', content)
#         clean_content = re.sub(r'#\w+', '', content).strip()
#         formatted_content = clean_content + "\n\n" + "\n".join(hashtags)
#
#     # 문자 제한 적용
#     if limit and len(formatted_content) > limit:
#         formatted_content = formatted_content[:limit - 3] + "..."
#
#     return formatted_content


# def analyze_content_performance(
#     content_metrics: List[Dict[str, Any]]
# ) -> Dict[str, Any]:
#     """
#     마케팅 콘텐츠 성과를 분석합니다.
#
#     Args:
#         content_metrics: 콘텐츠 성과 지표 목록
#
#     Returns:
#         분석 결과
#     """
#     # 성과 지표 집계
#     total_impressions = sum(item.get("impressions", 0) for item in content_metrics)
#     total_engagements = sum(item.get("engagements", 0) for item in content_metrics)
#     total_clicks = sum(item.get("clicks", 0) for item in content_metrics)
#
#     # 평균 참여율 계산
#     avg_engagement_rate = (total_engagements / total_impressions) if total_impressions > 0 else 0
#
#     # 클릭률(CTR) 계산
#     ctr = (total_clicks / total_impressions) if total_impressions > 0 else 0
#
#     # 최고 성과 콘텐츠 찾기
#     best_performing = max(content_metrics, key=lambda x: x.get("engagements", 0), default={})
#
#     return {
#         "total_impressions": total_impressions,
#         "total_engagements": total_engagements,
#         "total_clicks": total_clicks,
#         "average_engagement_rate": avg_engagement_rate,
#         "ctr": ctr,
#         "best_performing_content": best_performing.get("content_id", ""),
#         "analysis_date": datetime.now().strftime("%Y-%m-%d")
#     }


# def generate_campaign_report(
#     campaign_data: Dict[str, Any],
#     content_performance: Dict[str, Any]
# ) -> str:
#     """
#     마케팅 캠페인 보고서를 생성합니다.
#
#     Args:
#         campaign_data: 캠페인 데이터
#         content_performance: 콘텐츠 성과 데이터
#
#     Returns:
#         포맷팅된 보고서 문자열
#     """
#     report = f"# {campaign_data.get('campaign_name', '마케팅 캠페인')} 보고서\n\n"
#     report += f"기간: {campaign_data.get('start_date', '')} ~ {campaign_data.get('end_date', '')}\n\n"
#
#     report += "## 캠페인 개요\n"
#     report += f"{campaign_data.get('description', '')}\n\n"
#
#     report += "## 주요 성과\n"
#     report += f"- 총 노출 수: {content_performance.get('total_impressions', 0):,}\n"
#     report += f"- 총 참여 수: {content_performance.get('total_engagements', 0):,}\n"
#     report += f"- 총 클릭 수: {content_performance.get('total_clicks', 0):,}\n"
#     report += f"- 평균 참여율: {content_performance.get('average_engagement_rate', 0):.2%}\n"
#     report += f"- 클릭률(CTR): {content_performance.get('ctr', 0):.2%}\n\n"
#
#     report += "## 채널별 성과\n"
#     for channel, metrics in campaign_data.get('channel_performance', {}).items():
#         report += f"### {channel}\n"
#         report += f"- 노출 수: {metrics.get('impressions', 0):,}\n"
#         report += f"- 참여 수: {metrics.get('engagements', 0):,}\n"
#         report += f"- 전환 수: {metrics.get('conversions', 0):,}\n\n"
#
#     report += "## 결론 및 권장사항\n"
#     report += f"{campaign_data.get('conclusions', '')}\n\n"
#
#     return report
