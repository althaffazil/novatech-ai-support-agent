from langgraph.graph import END

from src.graph.state import ConversationState


def supervisor_router(state: ConversationState):
    """
    Routes execution from the Supervisor node
    to the selected specialist agent.
    """

    next_node = state.get("next_node", "support_agent")

    if next_node == "FINISH":
        return END

    return next_node


def worker_router(state: ConversationState):
    """
    Reserved for future graph expansion.

    In this project every specialist agent ends
    the workflow, matching the project PDF.
    """

    return END