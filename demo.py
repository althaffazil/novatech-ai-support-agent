from src.config.logging_config import configure_logging
from src.core.application_container import ApplicationContainer


def main() -> None:
    configure_logging()

    chat_service = ApplicationContainer().chat_service

    user_id = "demo_enterprise_user"

    print("=" * 60)
    print("NovaTech Enterprise Customer Support Demo")
    print("Type 'exit' to quit.")
    print("=" * 60)

    while True:
        user_message = input("\nYou: ").strip()

        if user_message.lower() in {"exit", "quit"}:
            print("\nGoodbye!")
            break

        response = chat_service.process_chat_request(
            user_id=user_id,
            user_message=user_message,
        )

        print(f"\nNovaTech: {response}")


if __name__ == "__main__":
    main()