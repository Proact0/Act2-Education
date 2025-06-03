from langgraph.graph import StateGraph

from agents.base_workflow import BaseWorkflow
from agents.marketing.modules.nodes import DocSummarizationNode, NotionWritingNode
from agents.marketing.modules.state import ContentState  # , MarketingState


class MarketingWorkflow(BaseWorkflow):
    """
    교육 마케팅을 위한 Workflow 클래스

    이 클래스는 교육 관련 마케팅 캠페인 및 콘텐츠 생성을 위한 Workflow를 정의합니다.
    BaseWorkflow를 상속받아 기본 구조를 구현하고, MarketingState를 사용하여 상태를 관리합니다.
    """

    def __init__(self, state):
        super().__init__()
        self.state = state

    def build(self):
        """
        마케팅 Workflow 그래프 구축 메서드

        StateGraph를 사용하여 교육 마케팅을 위한 Workflow 그래프를 구축합니다.
        현재는 기본 구조만 포함하고 있으며, 추후 노드와 조건부 에지를 추가하여
        다양한 경로를 가진 Workflow를 구축할 수 있습니다.

        Returns:
            CompiledStateGraph: 컴파일된 상태 그래프 객체
        """
        builder = StateGraph(self.state)

        # 노드 추가 예시
        # builder.add_node("generate_campaign", CampaignGenerationNode())
        # builder.add_node("create_content", ContentCreationNode())

        # 에지 추가 예시 - 아래 코드는 참고용이며 실제 구현 시 주석을 해제하고 사용할 수 있습니다
        # 1. 단순 에지: 시작 노드에서 need_campaign_strategy 함수로 연결
        # builder.add_edge("__start__", need_campaign_strategy)
        #
        # 2. 조건부 에지: need_campaign_strategy 함수의 반환값에 따라 다른 노드로 분기
        # builder.add_conditional_edges(
        #     "__start__",                # 시작 노드
        #     need_campaign_strategy,     # 라우팅 함수 - 어떤 노드로 갈지 결정
        #     {                           # 라우팅 함수 반환값에 따른 목적지 노드
        #         "generate_campaign": "generate_campaign",  # 캠페인 생성 필요 시
        #         "create_content": "create_content"        # 콘텐츠 생성 필요 시
        #     }
        # )

        # 기본 에지 설정 (임시)
        # builder.add_edge("__start__", "__end__")

        # Notion contents writer node and edge
        builder.add_node("summarize_doc", DocSummarizationNode())
        builder.add_node("notion_write", NotionWritingNode())

        builder.add_edge("__start__", "summarize_doc")
        builder.add_edge("summarize_doc", "notion_write")
        builder.add_edge("notion_write", "__end__")

        workflow = builder.compile()  # 그래프 컴파일
        workflow.name = self.name  # Workflow 이름 설정

        return workflow


# 마케팅 Workflow 인스턴스 생성
marketing_workflow = MarketingWorkflow(ContentState)


if __name__ == "__main__":
    input_state = {"input_file": "agents/marketing/input_content_001_splitted.pdf"}

    final_state = marketing_workflow().invoke(input_state)
    print("📄 결과:", final_state["result"])
