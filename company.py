"""
Company profile extraction using MiniMax.
"""

import json
import re

import requests

from minimax_helper import chat_completion

SYSTEM_PROMPT = """You are a startup analyst. Analyze the startup description provided and extract structured information.

Return ONLY valid JSON with exactly these keys (use null if information is not mentioned):
- business_model: string (e.g., SaaS, marketplace, fintech, e-commerce, hardware, etc.)
- customer_type: string ("B2B" or "B2C" only, or null)
- stage: string ("pre-seed" or "seed" only, or null)
- milestone: string (what they want to achieve next, or null)
- mentioned_competitors: array of strings (company names if mentioned, or empty array [])

Do not include any other text, markdown, or explanation. Output only the raw JSON object."""


def extract_company_profile(startup_description: str) -> dict:
    """
    Extract a structured company profile from a startup description using MiniMax.

    Args:
        startup_description: Raw text describing the startup.

    Returns:
        A dictionary with keys: business_model, customer_type, stage,
        milestone, mentioned_competitors. Values are strings, null, or list
        as appropriate; missing info is None or [].

    Raises:
        ValueError: If MINIMAX_API_KEY is not set.
        RuntimeError: If the MiniMax API request fails.
    """
    if not startup_description or not startup_description.strip():
        return {
            "business_model": None,
            "customer_type": None,
            "stage": None,
            "milestone": None,
            "mentioned_competitors": [],
        }

    response = chat_completion(
        system_prompt=SYSTEM_PROMPT,
        user_prompt=startup_description.strip(),
    )

    return _parse_profile_json(response)


def _parse_profile_json(response: str) -> dict:
    """Parse JSON from MiniMax response, handling markdown and extra text."""
    text = response.strip()

    # Remove markdown code blocks if present
    code_block = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", text)
    if code_block:
        text = code_block.group(1).strip()

    # Try to find a JSON object in the response
    start = text.find("{")
    if start != -1:
        depth = 0
        for i in range(start, len(text)):
            if text[i] == "{":
                depth += 1
            elif text[i] == "}":
                depth -= 1
                if depth == 0:
                    text = text[start : i + 1]
                    break

    try:
        data = json.loads(text)
    except json.JSONDecodeError as e:
        raise ValueError(
            f"Failed to parse MiniMax response as JSON: {e}. Raw response: {response[:500]}"
        ) from e

    if not isinstance(data, dict):
        raise ValueError(
            f"MiniMax response was not a JSON object: {type(data).__name__}"
        )

    # Normalize to expected keys and types
    return {
        "business_model": data.get("business_model"),
        "customer_type": data.get("customer_type"),
        "stage": data.get("stage"),
        "milestone": data.get("milestone"),
        "mentioned_competitors": _ensure_competitors_list(
            data.get("mentioned_competitors")
        ),
    }


def _ensure_competitors_list(value) -> list:
    """Ensure mentioned_competitors is a list of strings."""
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item).strip() for item in value if item]
    return [str(value).strip()]


def find_competitors(business_model: str, keywords: str) -> list[str]:
    """
    Find up to 10 company names from OpenCorporates matching the given keywords.

    Args:
        business_model: Business model context (for future use; not sent to API).
        keywords: Search query string for the OpenCorporates companies search.

    Returns:
        A list of up to 10 company names. Empty list on error or no results.
        Only companies with non-null, non-empty names are included.
    """
    if not keywords or not str(keywords).strip():
        return []

    url = "https://api.opencorporates.com/v0.4/companies/search"
    params = {"q": str(keywords).strip()}

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
    except requests.RequestException:
        return []

    try:
        data = response.json()
    except json.JSONDecodeError:
        return []

    companies = (
        data.get("results") or {}
    ).get("companies") or []

    names = []
    for item in companies:
        company = item.get("company") if isinstance(item, dict) else None
        if not isinstance(company, dict):
            continue
        name = company.get("name")
        if name is not None and str(name).strip():
            names.append(str(name).strip())
        if len(names) >= 10:
            break

    return names[:10]
