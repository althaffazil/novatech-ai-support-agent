from langsmith.evaluation import evaluate

from src.evaluation.evaluation_dataset import (
    DATASET_NAME,
    EvaluationDataset,
)
from src.evaluation.langsmith_client import (
    LangSmithClientFactory,
)
from src.evaluation.routing_evaluator import (
    RoutingEvaluator,
)


def main() -> None:

    client = (
        LangSmithClientFactory()
        .get_client()
    )

    dataset = EvaluationDataset(
        client,
    )

    dataset.create(
        recreate=True,
    )

    evaluator = RoutingEvaluator()

    evaluate(
        evaluator.target,
        data=DATASET_NAME,
        evaluators=[
            evaluator.evaluator,
        ],
        experiment_prefix="Supervisor_Routing_Test",
    )

    print()

    print("✅ Evaluation completed successfully.")


if __name__ == "__main__":
    main()