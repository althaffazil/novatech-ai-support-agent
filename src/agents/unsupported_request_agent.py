from src.graph.state import ConversationState


class UnsupportedRequestAgent:
    """Handles requests outside the scope of NovaTech Customer Support."""

    def execute(
        self,
        state: ConversationState,
    ) -> dict:

        return {
            "messages": [
                (
                    "NovaTech Assistant: "
                    "I'm here to help only with NovaTech products, "
                    "services, customer accounts, company policies, "
                    "and technical support. "
                    "Please ask a question related to NovaTech."
                )
            ],
            "next_node": "FINISH",
        }