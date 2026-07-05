from src.config.logging_config import configure_logging
from src.web.app_factory import create_app


def main() -> None:

    configure_logging()

    app = create_app()

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True,
    )


if __name__ == "__main__":
    main()