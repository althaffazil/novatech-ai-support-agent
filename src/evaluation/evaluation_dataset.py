from langsmith import Client

DATASET_NAME = "NovaTech_Routing_Tests"

TEST_CASES = [
    {
        "input": "Hello, is anyone there?",
        "expected": "support_agent",
    },
    {
        "input": "What is my current subscription tier?",
        "expected": "support_agent",
    },
    {
        "input": "I need a refund for my broken monitor.",
        "expected": "retrieval_agent",
    },
    {
        "input": "How many days do I have to return an enterprise product?",
        "expected": "retrieval_agent",
    },
    {
        "input": "This is completely unacceptable. Let me speak to your manager immediately.",
        "expected": "escalation_agent",
    },
    {
        "input": "I am going to sue your company if you don't fix this.",
        "expected": "escalation_agent",
    },
    {
        "input": "What is 10 + 20?",
        "expected": "unsupported_request",
    },
    {
        "input": "Write a Python function.",
        "expected": "unsupported_request",
    },
]


class EvaluationDataset:
    """Creates or reuses the LangSmith evaluation dataset."""

    def __init__(
        self,
        client: Client,
    ) -> None:
        self.client = client

    def create(
        self,
        recreate: bool = False,
    ):

        if self.client.has_dataset(
            dataset_name=DATASET_NAME,
        ):

            if not recreate:
                return self.client.read_dataset(
                    dataset_name=DATASET_NAME,
                )

            self.client.delete_dataset(
                dataset_name=DATASET_NAME,
            )

        dataset = self.client.create_dataset(
            dataset_name=DATASET_NAME,
            description="Supervisor routing evaluation",
        )

        self.client.create_examples(
            inputs=[
                {
                    "messages": [case["input"]]
                }
                for case in TEST_CASES
            ],
            outputs=[
                {
                    "expected_route": case["expected"]
                }
                for case in TEST_CASES
            ],
            dataset_id=dataset.id,
        )

        return dataset