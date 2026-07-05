import json

from google.genai import types

from src.config.settings import CHAT_MODEL
from src.core.gemini_client import GeminiClient
from src.graph.state import ConversationState
from src.retrieval.retrieval_service import RetrievalService


class RetrievalAgent:
    """Answers policy and technical questions using the knowledge base."""

    def __init__(
        self,
        retrieval_service: RetrievalService,
    ) -> None:
        self.client = GeminiClient.get_client()
        self.retrieval_service = retrieval_service

    def execute(
        self,
        state: ConversationState,
    ) -> dict:

        user_message = state["messages"][-1]

        # Step 1: Reformulate the search query
        reformulation = self.client.models.generate_content(
            model=CHAT_MODEL,
            contents=(
                "Extract the core search terms from the "
                f"following customer request:\n\n{user_message}"
            ),
            config=types.GenerateContentConfig(
                temperature=0.0,
            ),
        )

        search_query = reformulation.text.strip()

        # Step 2: Retrieve relevant knowledge
        retrieved_context = self.retrieval_service.search(
            search_query
        )

        customer_profile = state.get(
            "customer_profile",
            {},
        )

        system_prompt = f"""
You are the NovaTech Policy Expert.

Customer Context:

{json.dumps(customer_profile, indent=2)}

Answer ONLY using the retrieved company policies below.

If the answer is not present in the retrieved context,
clearly state that you do not know and recommend opening
a support ticket.

Retrieved Policies:

{retrieved_context}
"""

        # Step 3: Generate grounded answer
        response = self.client.models.generate_content(
            model=CHAT_MODEL,
            contents=user_message,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                temperature=0.0,
            ),
        )

        return {
            "messages": [
                f"NovaTech Policy Expert: {response.text}"
            ],
            "next_node": "FINISH",
        }