from langgraph.graph import END, START, StateGraph

from src.agents.escalation_agent import EscalationAgent
from src.agents.retrieval_agent import RetrievalAgent
from src.agents.support_agent import SupportAgent
from src.agents.supervisor_agent import SupervisorAgent
from src.graph.routers import supervisor_router
from src.graph.state import ConversationState
from src.memory.sqlite_checkpoint import SqliteCheckpointManager
from src.retrieval.retrieval_service import RetrievalService
from src.agents.unsupported_request_agent import (
    UnsupportedRequestAgent,
)

class CustomerSupportWorkflow:
    """Builds and compiles the LangGraph workflow."""

    def __init__(
        self,
        retrieval_service: RetrievalService,
        checkpoint_manager: SqliteCheckpointManager,
    ) -> None:

        self.retrieval_service = retrieval_service
        self.checkpoint_manager = checkpoint_manager

        self.supervisor = SupervisorAgent()
        self.support = SupportAgent()
        self.retrieval = RetrievalAgent(
            retrieval_service,
        )
        self.escalation = EscalationAgent()
        self.unsupported = UnsupportedRequestAgent()

    def build(self):

        workflow = StateGraph(
            ConversationState,
        )

        workflow.add_node(
            "Supervisor",
            self.supervisor.route,
        )

        workflow.add_node(
            "support_agent",
            self.support.execute,
        )

        workflow.add_node(
            "retrieval_agent",
            self.retrieval.execute,
        )

        workflow.add_node(
            "escalation_agent",
            self.escalation.execute,
        )

        workflow.add_node(
            "unsupported_request",
            self.unsupported.execute,
        )

        workflow.add_edge(
            START,
            "Supervisor",
        )

        workflow.add_conditional_edges(
            "Supervisor",
            supervisor_router,
            {
                "support_agent": "support_agent",
                "retrieval_agent": "retrieval_agent",
                "escalation_agent": "escalation_agent",
                "unsupported_request": "unsupported_request",
                END: END,
            }
        )

        workflow.add_edge(
            "support_agent",
            END,
        )

        workflow.add_edge(
            "retrieval_agent",
            END,
        )

        workflow.add_edge(
            "escalation_agent",
            END,
        )

        workflow.add_edge(
            "unsupported_request",
            END,
        )

        return workflow.compile(
            checkpointer=self.checkpoint_manager.get_checkpointer(),
        )