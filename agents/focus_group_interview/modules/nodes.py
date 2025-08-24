"""
노드 클래스 모듈

이 모듈은 LangGraph Workflow에서 사용되는 노드 클래스들을 정의합니다.
각 노드 클래스는 BaseNode를 상속받아 구현되며, Workflow 그래프에서 특정 기능을 수행하는 단위 컴포넌트입니다.
각 노드는 execute 메서드를 구현하여 상태(state)를 입력받아 처리하고, 처리 결과를 새로운 상태 업데이트로 반환합니다.
"""

from typing import Dict, Any
from langchain_core.messages import HumanMessage, AIMessage


class SimpleQuestionGenerationNode:
    """
    간단한 질문 생성 노드 (테스트용)
    
    실제 LLM 없이 미리 정의된 질문을 생성합니다.
    """
    
    def __init__(self):
        self.name = "simple_question_generation"
    
    def __call__(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        주어진 주제와 대상에 맞는 질문을 생성합니다.
        
        Args:
            state: 현재 workflow 상태
            
        Returns:
            생성된 질문이 포함된 상태 업데이트
        """
        topic = state.get("interview_topic", "")
        audience = state.get("target_audience", "")
        
        # 테스트용 질문 생성
        questions = [
            f"{audience}들이 {topic}에 대해 어떻게 생각하시나요?",
            f"{topic}의 가장 큰 장점은 무엇이라고 생각하시나요?",
            f"{topic}에서 개선이 필요한 부분은 무엇인가요?",
            f"{audience}에게 {topic}가 어떤 영향을 미친다고 생각하시나요?",
            f"{topic}를 더 효과적으로 만들기 위한 아이디어가 있으신가요?"
        ]
        
        print(f"\n[질문 생성 노드 실행]")
        print(f"주제: {topic}")
        print(f"대상: {audience}")
        print(f"생성된 질문 수: {len(questions)}")
        
        return {"questions": questions}


class SimpleResponseCollectionNode:
    """
    간단한 응답 수집 노드 (시뮬레이션)
    
    실제 응답 수집 대신 샘플 응답을 생성합니다.
    """
    
    def __init__(self):
        self.name = "simple_response_collection"
    
    def __call__(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        질문에 대한 응답을 시뮬레이션합니다.
        
        Args:
            state: 현재 workflow 상태
            
        Returns:
            수집된 응답이 포함된 상태 업데이트
        """
        questions = state.get("questions", [])
        responses = state.get("responses", [])
        
        # 각 질문에 대한 샘플 응답 생성
        sample_responses = []
        for i, question in enumerate(questions[:3], 1):  # 처음 3개 질문만
            response = HumanMessage(content=f"질문 {i}: {question}")
            sample_responses.append(response)
            
            ai_response = AIMessage(content=f"응답 {i}: 이것은 '{question}'에 대한 샘플 응답입니다. 매우 유익하고 통찰력 있는 의견입니다.")
            sample_responses.append(ai_response)
        
        print(f"\n[응답 수집 노드 실행]")
        print(f"질문 수: {len(questions)}")
        print(f"수집된 응답 수: {len(sample_responses)}")
        
        return {"responses": responses + sample_responses}


class SimpleAnalysisNode:
    """
    간단한 분석 노드
    
    수집된 응답을 분석하여 요약합니다.
    """
    
    def __init__(self):
        self.name = "simple_analysis"
    
    def __call__(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        응답을 분석하여 인사이트를 도출합니다.
        
        Args:
            state: 현재 workflow 상태
            
        Returns:
            분석 결과가 포함된 상태 업데이트
        """
        responses = state.get("responses", [])
        topic = state.get("interview_topic", "")
        audience = state.get("target_audience", "")
        
        # 간단한 분석 결과 생성
        analysis_message = AIMessage(
            content=f"""
            [포커스 그룹 인터뷰 분석 결과]
            
            주제: {topic}
            대상: {audience}
            
            주요 인사이트:
            1. 참가자들은 {topic}에 대해 전반적으로 긍정적인 반응을 보였습니다.
            2. 개선이 필요한 영역이 여러 개 확인되었습니다.
            3. {audience}의 요구사항이 명확히 파악되었습니다.
            
            응답 수: {len(responses)}
            분석 완료 시간: 현재 시간
            """
        )
        
        print(f"\n[분석 노드 실행]")
        print(f"분석된 응답 수: {len(responses)}")
        print("분석 완료!")
        
        return {"responses": responses + [analysis_message]}


# 기존 주석 처리된 코드는 아래에 유지

# from agents.base_node import BaseNode

# from agents.focus_group_interview.modules.chains import set_question_generation_chain, set_response_analysis_chain


# class QuestionGenerationNode(BaseNode):
#     """
#     인터뷰 주제와 대상 청중에 적합한 질문을 생성하는 노드
#
#     이 노드는 LangChain의 질문 생성 체인을 활용하여 포커스 그룹 인터뷰에 적합한 질문을 생성합니다.
#     주어진 인터뷰 주제와 대상 청중에 맞게 질문을 생성하여 Workflow의 다음 단계로 전달합니다.
#     """

#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)  # BaseNode 초기화
#         # set_question_generation_chain 함수를 통해 LangChain 체인을 가져와 설정
#         self.chain = set_question_generation_chain()  # 질문 생성 체인 설정

#     def execute(self, state) -> dict:
#         """
#         주어진 상태(state)에서 필요한 정보를 추출하여 질문을 생성하고 결과를 반환합니다.
#
#         Args:
#             state (dict): Workflow의 현재 상태. interview_topic과 target_audience 정보를 포함함.
#
#         Returns:
#             dict: 새로 생성된 질문들을 포함한 상태 업데이트
#         """
#         # 질문 생성 체인 실행 - LLM을 통해 질문 생성
#         generated_questions = self.chain.invoke(
#             {
#                 "interview_topic": state["interview_topic"],  # 인터뷰 주제
#                 "target_audience": state["target_audience"],  # 대상 청중
#             }
#         )

#         # 생성된 질문을 반환 - 새로운 상태 업데이트로 반환
#         return {"questions": generated_questions}


# class ResponseAnalysisNode(BaseNode):
#     """
#     인터뷰 응답을 분석하는 노드
#
#     이 노드는 LangChain의 응답 분석 체인을 활용하여 포커스 그룹 인터뷰에서 수집된 응답들을 분석합니다.
#     응답을 분석하여 주요 통찰과 패턴을 추출하고, 이를 Workflow의 다음 단계로 전달합니다.
#     """

#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)  # BaseNode 초기화
#         # set_response_analysis_chain 함수를 통해 LangChain 체인을 가져와 설정
#         self.chain = set_response_analysis_chain()  # 응답 분석 체인 설정

#     def execute(self, state) -> dict:
#         """
#         주어진 상태(state)에서 인터뷰 응답을 추출하여 분석하고 결과를 반환합니다.
#
#         Args:
#             state (dict): Workflow의 현재 상태. responses, interview_topic, target_audience 정보를 포함함.
#
#         Returns:
#             dict: 분석된 결과를 포함한 상태 업데이트
#         """
#         # 응답 분석 체인 실행 - LLM을 통해 응답 분석
#         analysis_result = self.chain.invoke(
#             {
#                 "responses": state["responses"],  # 인터뷰 응답
#                 "interview_topic": state["interview_topic"],  # 인터뷰 주제
#                 "target_audience": state["target_audience"],  # 대상 청중
#             }
#         )

#         # 분석 결과를 새로운 상태 업데이트로 반환
#         return {"responses": analysis_result}
