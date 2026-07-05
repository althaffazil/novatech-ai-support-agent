import json

from google.genai import types

from src.config.settings import CHAT_MODEL
from src.core.gemini_client import GeminiClient
from src.graph.state import ConversationState


class SupervisorAgent:
    """Routes customer requests to the appropriate specialist agent."""

    SYSTEM_PROMPT = """
    You are the routing supervisor for NovaTech Customer Support.

    Your responsibility is ONLY to determine which specialist agent should handle
    the customer's latest message.

    Routing Rules:

    1. support_agent
    Use for:
    - Greetings
    - Farewells
    - Thank you messages
    - Subscription tier questions
    - Account status questions
    - General customer support conversation related to NovaTech

    2. retrieval_agent
    Use for:
    - Refunds
    - Returns
    - Company policies
    - SLAs
    - Account security
    - Password reset
    - Account recovery
    - Technical troubleshooting
    - Product documentation
    - FAQs
    - Any question that requires company knowledge

    3. escalation_agent
    Use for:
    - Angry customers
    - Serious complaints
    - Legal threats
    - Requests for a human manager
    - Escalations

    4. unsupported_request
    Use for ANY request unrelated to NovaTech customer support.

    Examples include:
    - Mathematics
    - Programming
    - Homework
    - History
    - Geography
    - Science
    - Weather
    - Movies
    - Sports
    - Politics
    - Cooking
    - Travel
    - General knowledge
    - Personal advice
    - Questions about other companies

    IMPORTANT:
    If the request is NOT about NovaTech products, services, customer accounts,
    company policies, or technical support, ALWAYS choose
    "unsupported_request".

    Return ONLY valid JSON.

    Example:

    {
        "next_department": "support_agent"
    }
    """

    def __init__(self) -> None:
        self.client = GeminiClient.get_client()

    def route(
        self,
        state: ConversationState,
    ) -> dict:

        response = self.client.models.generate_content(
            model=CHAT_MODEL,
            contents=state["messages"][-1],
            config=types.GenerateContentConfig(
                system_instruction=self.SYSTEM_PROMPT,
                temperature=0.0,
                response_mime_type="application/json",
            ),
        )

        try:
            decision = json.loads(response.text)

            next_node = decision.get(
                "next_department",
                "support_agent",
            )

        except Exception:
            next_node = "support_agent"

        return {
            "next_node": next_node,
        }