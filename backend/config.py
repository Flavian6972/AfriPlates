from dotenv import load_dotenv
import os

# Load .env file into environment
load_dotenv()


def get_env(name: str, default: str | None = None) -> str:
    """Fetch environment variable or raise error if missing."""
    value = os.getenv(name, default)
    if value is None:
        raise ValueError(f"Missing required environment variable: {name}")
    return value


class Config:
    # Required variables
    SQLALCHEMY_DATABASE_URI: str = get_env("SQLALCHEMY_DATABASE_URI")
    OPENAI_API_KEY: str = get_env("OPENAI_API_KEY")

    # Optional variables with defaults
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
