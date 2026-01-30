#!/usr/bin/env python3
"""
VC diligence main script: company profile, competitors, financials, and memo generation.
"""

import json
import sys
from pathlib import Path

from company import extract_company_profile, find_competitors
from finance import analyze_financials
from memo import generate_memo

DEFAULT_CSV_PATH = "financials.csv"
DEFAULT_MEMO_PATH = "diligence_memo.md"
BENCHMARKS_PATH = "benchmarks.json"


def load_startup_description() -> str:
    """Prompt user for startup description or read from file."""
    print("\nEnter startup description:")
    print("  - Type your description and press Enter twice to finish")
    print("  - Or enter a file path (e.g. description.txt) to load from file")
    print()
    first_line = input("Description or file path: ").strip()

    if not first_line:
        raise ValueError("No description or file path provided.")

    path = Path(first_line)
    if path.exists() and path.is_file():
        return path.read_text(encoding="utf-8").strip()
    # Multi-line: first line + any further lines until empty line
    lines = [first_line]
    while True:
        line = input().strip()
        if not line:
            break
        lines.append(line)
    return "\n".join(lines).strip()


def load_benchmarks() -> dict:
    """Load benchmarks from benchmarks.json."""
    path = Path(BENCHMARKS_PATH)
    if not path.exists():
        raise FileNotFoundError(f"Benchmarks file not found: {BENCHMARKS_PATH}")
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def main() -> None:
    print("=" * 60)
    print("VC Diligence Pipeline")
    print("=" * 60)

    company_profile = None
    financial_metrics = None
    benchmark_data = None

    try:
        # Step 1: Prompt for startup description (or read from file)
        print("\nStep 1: Reading startup description...")
        startup_description = load_startup_description()
        print("  Done.")

        # Step 2: Extract company profile
        print("\nStep 2: Analyzing company description...")
        company_profile = extract_company_profile(startup_description)
        print("  Done.")

        # Step 3: Print extracted profile
        print("\nStep 3: Extracted company profile:")
        print("---")
        for key, value in company_profile.items():
            print(f"  {key}: {value}")
        print("---\n")

        # Step 4: Find competitors if business_model is available
        print("Step 4: Finding competitors...")
        competitors = []
        business_model = company_profile.get("business_model") if company_profile else None
        if business_model and str(business_model).strip():
            keywords = str(business_model).strip()
            competitors = find_competitors(business_model, keywords)
            print(f"  Found {len(competitors)} competitor(s).")
        else:
            print("  Skipped (no business model available).")
        if competitors:
            print("  Competitors:", ", ".join(competitors[:5]), "..." if len(competitors) > 5 else "")

        # Step 5: Load benchmarks
        print("\nStep 5: Loading benchmarks...")
        benchmark_data = load_benchmarks()
        print(f"  Loaded {len(benchmark_data)} benchmark set(s).")

        # Step 6: Prompt for CSV path (or use default)
        print("\nStep 6: Reading financial data...")
        csv_prompt = f"CSV file path [{DEFAULT_CSV_PATH}]: "
        csv_input = input(csv_prompt).strip() or DEFAULT_CSV_PATH
        csv_path = Path(csv_input)
        if not csv_path.exists():
            raise FileNotFoundError(f"CSV file not found: {csv_path}")

        # Step 7: Analyze financials
        print("\nStep 7: Analyzing financials...")
        financial_metrics = analyze_financials(str(csv_path))
        print("  Done.")

        # Step 8: Print financial metrics
        print("\nStep 8: Financial metrics:")
        print("---")
        print(f"  Monthly burn: {financial_metrics['burn']:,.2f}")
        print(f"  Runway (months): {financial_metrics['runway']:.2f}")
        print(f"  Downside scenario burn: {financial_metrics['downside_burn']:,.2f}")
        print(f"  Runway at downside (months): {financial_metrics['runway_at_downside']:.2f}")
        print("---\n")

        # Step 9: Generate memo
        print("Step 9: Generating diligence memo...")
        generate_memo(company_profile, financial_metrics, benchmark_data)
        print("  Done.")

        # Step 10: Success message with memo location

        memo_path = Path(DEFAULT_MEMO_PATH)
        print("\nStep 10: Complete.")
        print("=" * 60)
        print("Success!")
        print(f"Memo saved to: {memo_path.absolute()}")
        print("=" * 60)

    except FileNotFoundError as e:
        print(f"\nError (missing file): {e}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"\nError (invalid input): {e}", file=sys.stderr)
        sys.exit(1)
    except RuntimeError as e:
        print(f"\nError (API or runtime): {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\nCancelled by user.", file=sys.stderr)
        sys.exit(130)
    except Exception as e:
        print(f"\nUnexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
