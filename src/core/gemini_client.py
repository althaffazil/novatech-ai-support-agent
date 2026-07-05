from google import genai

from src.config.settings import GEMINI_API_KEY


class GeminiClient:
    """Singleton wrapper around the Gemini SDK client."""

    _client = None

    @classmethod
    def get_client(cls) -> genai.Client:
        if cls._client is None:
            if not GEMINI_API_KEY:
                raise ValueError(
                    "GEMINI_API_KEY is not configured. "
                    "Please check your .env file."
                )

            cls._client = genai.Client(api_key=GEMINI_API_KEY)

        return cls._client