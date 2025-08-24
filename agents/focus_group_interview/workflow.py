from langgraph.graph import StateGraph

from agents.base_workflow import BaseWorkflow
from agents.focus_group_interview.modules.state import FocusGroupInterviewState
from agents.focus_group_interview.modules.nodes import (
    SimpleQuestionGenerationNode,
    SimpleResponseCollectionNode,
    SimpleAnalysisNode
)


class FocusGroupInterviewWorkflow(BaseWorkflow):
    """
    포커스 그룹 인터뷰를 위한 Workflow 클래스

    이 클래스는 교육 관련 포커스 그룹 인터뷰를 위한 Workflow를 정의합니다.
    BaseWorkflow를 상속받아 기본 구조를 구현하고, FocusGroupInterviewState를 사용하여 상태를 관리합니다.
    """

    def __init__(self, state):
        super().__init__()
        self.state = state

    def build(self):
        """
        포커스 그룹 인터뷰 Workflow 그래프 구축 메서드

        StateGraph를 사용하여 포커스 그룹 인터뷰를 위한 Workflow 그래프를 구축합니다.
        현재는 기본 구조만 포함하고 있으며, 추후 노드와 조건부 에지를 추가하여
        다양한 경로를 가진 Workflow를 구축할 수 있습니다.

        Returns:
            CompiledStateGraph: 컴파일된 상태 그래프 객체
        """
        builder = StateGraph(self.state)

        # 노드 추가
        builder.add_node("generate_questions", SimpleQuestionGenerationNode())
        builder.add_node("collect_responses", SimpleResponseCollectionNode())
        builder.add_node("analyze_responses", SimpleAnalysisNode())

        # 에지 추가 - 순차적 실행
        builder.add_edge("__start__", "generate_questions")
        builder.add_edge("generate_questions", "collect_responses")
        builder.add_edge("collect_responses", "analyze_responses")
        builder.add_edge("analyze_responses", "__end__")

        workflow = builder.compile()  # 그래프 컴파일
        workflow.name = self.name  # Workflow 이름 설정

        return workflow


# 포커스 그룹 인터뷰 Workflow 인스턴스 생성
focus_group_interview_workflow = FocusGroupInterviewWorkflow(FocusGroupInterviewState)
