"""
VC Diligence Streamlit app: startup description, CSV upload, analysis, and memo.
"""

import tempfile
from pathlib import Path

import streamlit as st

from company import extract_company_profile, find_competitors
from finance import analyze_financials
from main import load_benchmarks
from memo import generate_memo

st.set_page_config(page_title="VC Diligence", page_icon="📋", layout="wide")

st.title("📋 VC Diligence")
st.caption("Analyze startup description and financials to generate a diligence memo.")

# Inputs
with st.expander("Inputs", expanded=True):
    startup_description = st.text_area(
        "Startup description",
        placeholder="Paste or type the startup description (business model, stage, milestones, etc.)...",
        height=160,
        help="The raw text used to extract company profile and context for the memo.",
    )

    csv_file = st.file_uploader(
        "Financials CSV",
        type=["csv"],
        help="CSV with columns: month, expenses, cash_balance.",
    )

    run_analysis = st.button("Run analysis", type="primary", use_container_width=True)

# Initialize session state for results
if "company_profile" not in st.session_state:
    st.session_state.company_profile = None
if "financial_metrics" not in st.session_state:
    st.session_state.financial_metrics = None
if "memo_text" not in st.session_state:
    st.session_state.memo_text = None
if "competitors" not in st.session_state:
    st.session_state.competitors = []

def run_pipeline():
    if not startup_description or not startup_description.strip():
        st.error("Please enter a startup description.")
        return
    if csv_file is None:
        st.error("Please upload a financials CSV file.")
        return

    with st.spinner("Extracting company profile..."):
        company_profile = extract_company_profile(startup_description.strip())

    business_model = company_profile.get("business_model")
    if business_model and str(business_model).strip():
        with st.spinner("Finding competitors..."):
            competitors = find_competitors(
                business_model, str(business_model).strip()
            )
    else:
        competitors = []

    try:
        benchmark_data = load_benchmarks()
    except FileNotFoundError:
        st.error("Benchmarks file (benchmarks.json) not found in the project.")
        return

    with tempfile.NamedTemporaryFile(mode="wb", suffix=".csv", delete=False) as tmp:
        tmp.write(csv_file.getvalue())
        tmp_path = tmp.name

    try:
        with st.spinner("Analyzing financials..."):
            financial_metrics = analyze_financials(tmp_path)
    except (ValueError, FileNotFoundError) as e:
        st.error(f"Financials error: {e}")
        return
    finally:
        Path(tmp_path).unlink(missing_ok=True)

    with st.spinner("Generating diligence memo..."):
        memo_text = generate_memo(
            company_profile,
            financial_metrics,
            benchmark_data,
        )

    st.session_state.company_profile = company_profile
    st.session_state.competitors = competitors
    st.session_state.financial_metrics = financial_metrics
    st.session_state.memo_text = memo_text

if run_analysis:
    run_pipeline()

# Company profile card
if st.session_state.company_profile is not None:
    st.divider()
    st.subheader("Company profile")
    profile = st.session_state.company_profile
    with st.container():
        st.markdown(
            f"""
            <div style="
                background: linear-gradient(135deg, #1e3a5f 0%, #0d2137 100%);
                border-radius: 12px;
                padding: 1.5rem;
                color: #e8eef4;
                box-shadow: 0 4px 14px rgba(0,0,0,0.15);
                margin-bottom: 1rem;
            ">
                <p style="margin:0.25rem 0;"><b>Business model</b> &nbsp; {profile.get('business_model') or '—'}</p>
                <p style="margin:0.25rem 0;"><b>Customer type</b> &nbsp; {profile.get('customer_type') or '—'}</p>
                <p style="margin:0.25rem 0;"><b>Stage</b> &nbsp; {profile.get('stage') or '—'}</p>
                <p style="margin:0.25rem 0;"><b>Milestone</b> &nbsp; {profile.get('milestone') or '—'}</p>
                <p style="margin:0.25rem 0;"><b>Mentioned competitors</b> &nbsp; {', '.join(profile.get('mentioned_competitors') or []) or '—'}</p>
                <p style="margin:0.25rem 0; margin-top:0.5rem;"><b>Found competitors</b> &nbsp; {', '.join(st.session_state.competitors[:10]) or '—'}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

# Financial metrics table
if st.session_state.financial_metrics is not None:
    st.subheader("Financial metrics")
    fm = st.session_state.financial_metrics
    st.dataframe(
        {
            "Metric": [
                "Monthly burn",
                "Runway (months)",
                "Downside scenario burn",
                "Runway at downside (months)",
            ],
            "Value": [
                f"{fm['burn']:,.2f}",
                f"{fm['runway']:.2f}",
                f"{fm['downside_burn']:,.2f}",
                f"{fm['runway_at_downside']:.2f}",
            ],
        },
        use_container_width=True,
        hide_index=True,
    )

# Generated memo
if st.session_state.memo_text:
    st.subheader("Diligence memo")
    st.markdown(st.session_state.memo_text)
