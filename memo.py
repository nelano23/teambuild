"""
Generate VC financial diligence memos using MiniMax.
"""

from minimax_helper import call_minimax

SYSTEM_PROMPT = (
    "You are an expert VC analyst. Generate a concise financial diligence memo "
    "analyzing whether this startup's financials align with their stage and business model. "
    "Be specific and data-driven."
)


def _format_user_prompt(
    company_profile: dict,
    financial_metrics: dict,
    benchmark_data: dict,
) -> str:
    """Build the user prompt with company profile, financials, and benchmarks."""
    lines = [
        "## Company profile",
        f"- Business model: {company_profile.get('business_model', 'N/A')}",
        f"- Customer type: {company_profile.get('customer_type', 'N/A')}",
        f"- Stage: {company_profile.get('stage', 'N/A')}",
        f"- Milestone: {company_profile.get('milestone', 'N/A')}",
        f"- Mentioned competitors: {company_profile.get('mentioned_competitors', []) or 'None'}",
        "",
        "## Financial metrics",
        f"- Monthly burn: {financial_metrics.get('burn', 'N/A')}",
        f"- Runway (months): {financial_metrics.get('runway', 'N/A')}",
        f"- Downside scenario burn: {financial_metrics.get('downside_burn', 'N/A')}",
        f"- Runway at downside (months): {financial_metrics.get('runway_at_downside', 'N/A')}",
        "",
        "## Relevant benchmark ranges",
    ]
    for key, values in benchmark_data.items():
        if isinstance(values, dict):
            lines.append(f"- **{key}**: {values}")
        else:
            lines.append(f"- **{key}**: {values}")
    lines.extend([
        "",
        "---",
        "Please analyze and cover:",
        "1. **Burn assessment** – How does current burn compare to benchmarks for this stage/model?",
        "2. **Runway adequacy** – Is runway sufficient relative to targets and milestones?",
        "3. **Capital efficiency** – Efficiency vs. peers (burn per employee / benchmarks if relevant).",
        "4. **Milestone alignment** – Can they reach the stated milestone with current runway?",
        "",
        "Return the memo in markdown format.",
    ])
    return "\n".join(lines)


def generate_memo(
    company_profile: dict,
    financial_metrics: dict,
    benchmark_data: dict,
) -> str:
    """
    Generate a financial diligence memo using MiniMax.

    Args:
        company_profile: Dict with business_model, customer_type, stage,
            milestone, mentioned_competitors.
        financial_metrics: Dict with burn, runway, downside_burn,
            runway_at_downside (e.g. from finance.analyze_financials).
        benchmark_data: Dict of benchmark ranges (e.g. from benchmarks.json).

    Returns:
        The memo as markdown text.

    Raises:
        ValueError: If MINIMAX_API_KEY is not set.
        RuntimeError: If the MiniMax API request fails.
    """
    user_prompt = _format_user_prompt(
        company_profile, financial_metrics, benchmark_data
    )
    memo = call_minimax(
        system_prompt=SYSTEM_PROMPT,
        user_prompt=user_prompt,
    )

    with open("diligence_memo.md", "w", encoding="utf-8") as f:
        f.write(memo)

    return memo
