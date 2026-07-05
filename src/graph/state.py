import operator
from typing import Annotated, List, TypedDict


class ConversationState(TypedDict):
    """
    Shared state passed between all LangGraph nodes.
    """

    messages: Annotated[List[str], operator.add]
    next_node: str
    customer_profile: dict