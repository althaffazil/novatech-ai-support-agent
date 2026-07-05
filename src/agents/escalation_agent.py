from src.graph.state import ConversationState


class EscalationAgent:
    """Handles high-priority customer escalations."""

    def execute(
        self,
        state: ConversationState,
    ) -> dict:

        profile = state.get("customer_profile", {})

        tier = profile.get(
            "subscription_tier",
            "Standard",
        )

        response = (
            f"Escalation Manager: I understand your frustration. "
            f"As a {tier} customer, I am immediately escalating "
            f"your ticket to our Tier-2 human support team. "
            f"A manager will contact you at your registered "
            f"email within 15 minutes."
        )

        return {
            "messages": [response],
            "next_node": "FINISH",
        }