"""Gemini API service."""

import logging

from flask import current_app
from google import genai
from google.genai import types


logger = logging.getLogger(__name__)


SYSTEM_PROMPT = (
    "You are Lumen, a friendly and clear AI assistant for students. "
    "Explain things simply, use short examples, and put code inside "
    "triple-backtick code blocks."
)


class GeminiError(Exception):
    """Error raised when Gemini cannot answer."""

    def __init__(self, message, status_code=502):
        super().__init__(message)
        self.user_message = message
        self.status_code = status_code


def get_ai_reply(history, user_message):
    """Send the conversation to Gemini and return the AI response."""

    api_key = current_app.config["GEMINI_API_KEY"]

    if not api_key:
        raise GeminiError(
            "The AI is not set up yet. Add GEMINI_API_KEY to the .env file.",
            503
        )

    # Convert our database messages into Gemini messages.
    contents = []

    for item in history:
        role = "user" if item["sender"] == "user" else "model"

        contents.append(
            types.Content(
                role=role,
                parts=[
                    types.Part(text=item["message"])
                ]
            )
        )

    # Add the new message.
    contents.append(
        types.Content(
            role="user",
            parts=[
                types.Part(text=user_message)
            ]
        )
    )

    try:
        client = genai.Client(api_key=api_key)

        response = client.models.generate_content(
            model=current_app.config["GEMINI_MODEL"],
            contents=contents,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT
            )
        )

        reply = (response.text or "").strip()

        if not reply:
            raise GeminiError(
                "The AI returned an empty answer. Please try again.",
                502
            )

        return reply

    except GeminiError:
        raise

    except Exception:
        logger.exception("Gemini request failed")

        raise GeminiError(
            "Sorry, something went wrong while contacting the AI. Please try again.",
            502
        )

