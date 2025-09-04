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
    SECRET_KEY: str = get_env("SECRET_KEY")

    # Intasend Configuration
    INTASEND_PUBLISHABLE_KEY: str = get_env("INTASEND_PUBLISHABLE_KEY", "demo_key")
    INTASEND_SECRET_KEY: str = get_env("INTASEND_SECRET_KEY", "demo_secret")
    INTASEND_TEST_MODE: bool = os.getenv("INTASEND_TEST_MODE", "True").lower() == "true"

    # Optional variables with defaults
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
