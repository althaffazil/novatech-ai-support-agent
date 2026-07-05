from langsmith.schemas import Example, Run

from src.agents.supervisor_agent import SupervisorAgent
from src.graph.state import ConversationState


class RoutingEvaluator:
    """Evaluates the Supervisor routing decisions."""

    def __init__(self) -> None:
        self.supervisor = SupervisorAgent()

    def target(self, inputs: dict) -> dict:
        """
        Runs only the Supervisor node.
        """

        state: ConversationState = {
            "messages": inputs["messages"],
            "next_node": "",
            "customer_profile": {},
        }

        decision = self.supervisor.route(state)

        return {
            "actual_route": decision["next_node"],
        }

    @staticmethod
    def evaluator(
        run: Run,
        example: Example,
    ) -> dict:

        actual = run.outputs.get("actual_route")

        expected = example.outputs.get("expected_route")

        score = 1.0 if actual == expected else 0.0

        return {
            "key": "routing_accuracy",
            "score": score,
        }