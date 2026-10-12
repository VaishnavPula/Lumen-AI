import os

try:
    from dotenv import load_dotenv
    load_dotenv()  # reads the .env file, if there is one
except ImportError:
    pass

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-only-secret-change-me")
    DATABASE = os.path.join(BASE_DIR, "instance", "chatbot.db")

    GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
    GEMINI_MODEL = os.environ.get("GEMINI_MODEL", "gemini-3.8-flash")

    MAX_MESSAGE_LENGTH = 2000      # characters per user message
    MAX_HISTORY_MESSAGES = 20      # how many past messages we send to Gemini

    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
