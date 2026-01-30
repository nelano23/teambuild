"""
MiniMax API helper for chat completions.
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

MINIMAX_BASE_URL = "https://api.minimax.io/v1/text/chatcompletion_v2"
DEFAULT_MODEL = "MiniMax-M2"


def _build_api_url() -> str:
    """Build API URL with GroupId query parameter from .env."""
    group_id = os.getenv("MINIMAX_GROUP_ID")
    if not group_id:
        raise ValueError(
            "MINIMAX_GROUP_ID is not set. Add it to your .env file."
        )
    return f"{MINIMAX_BASE_URL}?GroupId={group_id.strip()}"


def chat_completion(
    system_prompt: str,
    user_prompt: str,
    model: str | None = None,
) -> str:
    """
    Call the MiniMax chat completion API and return the assistant's response.

    Args:
        system_prompt: System message that sets the assistant's behavior.
        user_prompt: The user's message.
        model: Optional model name. Defaults to "MiniMax-M2".

    Returns:
        The assistant's response text.

    Raises:
        ValueError: If MINIMAX_API_KEY or MINIMAX_GROUP_ID is not set in .env.
        RuntimeError: If the API request fails or returns an error.
    """
    api_key = os.getenv("MINIMAX_API_KEY")
    if not api_key:
        raise ValueError(
            "MINIMAX_API_KEY is not set. Add it to your .env file."
        )

    api_url = _build_api_url()
    model_name = model or DEFAULT_MODEL
    headers = {
        "Authorization": f"Bearer {api_key.strip()}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": model_name,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": 0.7,
        "max_tokens": 2000,
    }

    try:
        response = requests.post(
            api_url,
            headers=headers,
            json=payload,
            timeout=60,
        )
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        if hasattr(e, "response") and e.response is not None:
            try:
                err_body = e.response.json()
                msg = err_body.get("error", {}).get("message", str(e))
            except Exception:
                msg = e.response.text or str(e)
            raise RuntimeError(f"MiniMax API error: {msg}") from e
        raise RuntimeError(f"MiniMax API request failed: {e}") from e

    result = response.json()
    try:
        content = result["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError) as e:
        raise RuntimeError(
            "MiniMax API returned unexpected response structure."
        ) from e
    if content is None:
        raise RuntimeError(
            "MiniMax API response missing message content."
        )

    return content.strip()


def call_minimax(
    system_prompt: str,
    user_prompt: str,
    model: str | None = None,
) -> str:
    """
    Alias for chat_completion. Call the MiniMax API and return the response.
    """
    return chat_completion(system_prompt, user_prompt, model)
