import json

from google.genai import types

from src.config.settings import CHAT_MODEL
from src.core.gemini_client import GeminiClient
from src.graph.state import ConversationState


class SupportAgent:
    """Handles general customer conversations."""

    SYSTEM_PROMPT = """
    You are a friendly NovaTech Customer Support Assistant.

    Your responsibilities are:

    - Welcome customers.
    - Answer greetings and conversational messages related to NovaTech customer support.
    - Answer simple account-related questions using the provided customer context.
    - Keep responses concise, professional, and friendly.
    - Personalize responses only when the provided customer context is relevant.

    Do not invent company policies or technical procedures.
    Policy, refund, SLA, account security, and troubleshooting questions are handled by other specialist agents.
    """

    def __init__(self) -> None:
        self.client = GeminiClient.get_client()

    def execute(
        self,
        state: ConversationState,
    ) -> dict:

        customer_profile = state.get("customer_profile", {})

        system_prompt = (
            f"{self.SYSTEM_PROMPT}\n\n"
            f"Customer Context:\n"
            f"{json.dumps(customer_profile, indent=2)}"
        )

        response = self.client.models.generate_content(
            model=CHAT_MODEL,
            contents=" ".join(state["messages"]),
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
            ),
        )

        return {
            "messages": [
                f"NovaTech Agent: {response.text}"
            ],
            "next_node": "FINISH",
        }