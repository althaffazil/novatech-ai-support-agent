from langgraph.graph.state import CompiledStateGraph

from src.graph.state import ConversationState
import logging

logger = logging.getLogger(__name__)

class ChatService:
    """Bridge between external applications and the LangGraph workflow."""

    def __init__(
        self,
        workflow: CompiledStateGraph,
    ) -> None:
        self.workflow = workflow

    def process_chat_request(
        self,
        user_id: str,
        user_message: str,
    ) -> str:

        thread_config = {
            "configurable": {
                "thread_id": user_id,
            }
        }

        customer_profile = {
            "subscription_tier": "Standard",
            "account_status": "Active",
        }

        if "premium" in user_id.lower():
            customer_profile["subscription_tier"] = (
                "Enterprise Priority"
            )

        initial_state: ConversationState = {
            "messages": [
                f"User: {user_message}"
            ],
            "next_node": "",
            "customer_profile": customer_profile,
        }

        try:
            final_state = self.workflow.invoke(
                initial_state,
                thread_config,
            )

            response = final_state["messages"][-1]

            if ":" in response:
                response = response.split(
                    ":",
                    1,
                )[1].strip()

            return response

        except Exception as ex:
            logger.exception(
                "Chat request failed."
            )

            return (
                "System Alert: Our support service is "
                "currently unavailable. "
                "Please try again later."
            )