"""Financial analysis utilities for burn rate, runway, and downside simulation."""

import pandas as pd


def calculate_burn(df: pd.DataFrame) -> float:
    """
    Calculate average monthly burn from a DataFrame of monthly expenses.

    Args:
        df: DataFrame with columns: month, expenses, cash_balance.

    Returns:
        Average monthly burn (mean of expenses).

    Raises:
        ValueError: If required columns are missing or DataFrame is empty.
    """
    if df is None or df.empty:
        raise ValueError("DataFrame is empty or None")

    required = {"month", "expenses", "cash_balance"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"DataFrame missing required columns: {missing}")

    return float(df["expenses"].mean())


def calculate_runway(cash_balance: float, monthly_burn: float) -> float:
    """
    Calculate months of runway remaining.

    Args:
        cash_balance: Current cash balance.
        monthly_burn: Average monthly burn rate.

    Returns:
        Months of runway (cash_balance / monthly_burn).
        Returns 0.0 if monthly_burn is zero or negative.

    Raises:
        ValueError: If cash_balance or monthly_burn is negative.
    """
    if cash_balance < 0:
        raise ValueError("cash_balance must be non-negative")
    if monthly_burn < 0:
        raise ValueError("monthly_burn must be non-negative")
    if monthly_burn == 0:
        return 0.0
    return cash_balance / monthly_burn


def simulate_downside(
    monthly_burn: float,
    increase_percent: float = 20,
) -> float:
    """
    Simulate burn with a percentage increase (downside scenario).

    Args:
        monthly_burn: Base monthly burn rate.
        increase_percent: Percentage increase to apply (default 20).

    Returns:
        Burn with percentage increase applied: monthly_burn * (1 + increase_percent/100).

    Raises:
        ValueError: If monthly_burn or increase_percent is negative.
    """
    if monthly_burn < 0:
        raise ValueError("monthly_burn must be non-negative")
    if increase_percent < 0:
        raise ValueError("increase_percent must be non-negative")
    return monthly_burn * (1 + increase_percent / 100)


def analyze_financials(csv_path: str) -> dict:
    """
    Read a CSV file and compute burn, runway, and downside metrics.

    Expects CSV with columns: month, expenses, cash_balance.
    Uses the latest row's cash_balance for runway.

    Args:
        csv_path: Path to the CSV file.

    Returns:
        Dict with keys: burn, runway, downside_burn, runway_at_downside.

    Raises:
        FileNotFoundError: If csv_path does not exist.
        ValueError: If CSV is empty or missing required columns.
    """
    try:
        df = pd.read_csv(csv_path)
    except FileNotFoundError:
        raise FileNotFoundError(f"CSV file not found: {csv_path}")
    except pd.errors.EmptyDataError:
        raise ValueError(f"CSV file is empty: {csv_path}")
    except Exception as e:
        raise ValueError(f"Failed to read CSV: {e}") from e

    if df is None or df.empty:
        raise ValueError("CSV contains no data")

    required = {"month", "expenses", "cash_balance"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"CSV missing required columns: {missing}")

    burn = calculate_burn(df)
    # Use latest cash balance (last row)
    cash_balance = float(df["cash_balance"].iloc[-1])
    runway = calculate_runway(cash_balance, burn)
    downside_burn = simulate_downside(burn, increase_percent=20)
    runway_at_downside = calculate_runway(cash_balance, downside_burn)

    return {
        "burn": burn,
        "runway": runway,
        "downside_burn": downside_burn,
        "runway_at_downside": runway_at_downside,
    }
