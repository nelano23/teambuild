# VC Diligence Pipeline

An AI-powered financial diligence tool for venture capitalists that automates the analysis of startup financials and generates professional investment memos.

## 🎯 What It Does

Given a startup's description and financial data, this tool:
- Extracts key business information (model, stage, competitors) using AI
- Calculates financial health metrics (burn rate, runway, capital efficiency)
- Compares against industry benchmarks
- Generates a professional VC diligence memo in seconds

**Perfect for:** VCs, angel investors, accelerators, and anyone performing startup due diligence.

---

## 🚀 Features

- **AI-Powered Analysis**: Uses MiniMax API to understand startup descriptions
- **Financial Metrics**: Automatically calculates burn rate, runway, and downside scenarios
- **Industry Benchmarks**: Compares against stage and business model standards
- **Competitor Research**: Integrates with OpenCorporates API for market context
- **Professional Output**: Generates markdown memos ready to share

---

## 📋 Requirements

- Python 3.10+ (Python 3.11 recommended)
- MiniMax API account ([sign up here](https://www.minimax.chat/))
- Mac, Linux, or Windows

---

## ⚙️ Installation

### 1. Clone the Repository
```bash
git clone https://github.com/nelano23/teambuild.git
cd teambuild
```

### 2. Install Dependencies
```bash
pip3 install requests python-dotenv pandas
```

### 3. Set Up Environment Variables
Create a `.env` file in the project root:
```bash
touch .env
```

Add your MiniMax credentials (no quotes, no spaces):
```
MINIMAX_API_KEY=your_api_key_here
MINIMAX_GROUP_ID=your_group_id_here
```

**Where to find these:**
- Log in to [MiniMax Dashboard](https://www.minimax.chat/)
- Navigate to API Keys section
- Copy both your API Key and Group ID

---

## 🎮 Usage

### Run the Tool
```bash
python3 main.py
```

### Input Options

**Option 1: Type your startup description**
```
Enter startup description:
  - Type your description and press Enter twice to finish
  - Or enter a file path (e.g. description.txt) to load from file
```

**Option 2: Use a file**
```
Description or file path: test_startup.txt
```

**Provide Financial Data**
```
CSV file path [financials.csv]: your_financials.csv
```

### Output
The tool generates a file: `diligence_memo.md` containing:
- Executive summary
- Burn rate assessment
- Runway analysis
- Capital efficiency metrics
- Milestone alignment evaluation
- Investment recommendations

---

## 📁 Project Structure

```
vc-diligence/
├── main.py                  # Main orchestration script
├── company.py               # Company profile extraction
├── finance.py               # Financial calculations
├── memo.py                  # Memo generation
├── minimax_helper.py        # MiniMax API integration
├── benchmarks.json          # Industry benchmark data
├── test_startup.txt         # Sample startup description
├── financials.csv           # Sample financial data
├── realestate_pitch.txt     # Real estate startup example
├── homebase_financials.csv  # Real estate financials example
└── .env                     # API credentials (create this)
```

---

## 📊 CSV Format

Your financial CSV should have these columns:

```csv
month,expenses,cash_balance
2025-01,83160,800000
2025-02,84833,716840
...
```

**Required columns:**
- `month`: Format YYYY-MM
- `expenses`: Monthly expenses in dollars
- `cash_balance`: Remaining cash at end of month

---

## 💡 Example Run

```bash
$ python3 main.py

============================================================
VC Diligence Pipeline
============================================================
Step 1: Reading startup description...
Description or file path: realestate_pitch.txt
  Done.
  
Step 2: Analyzing company description...
  Done.
  
Step 3: Extracted company profile:
---
  business_model: SaaS
  customer_type: B2B
  stage: seed
  milestone: reach $150K MRR in 18 months
  mentioned_competitors: ['Roofstock', 'Fundrise']
---

Step 6: Reading financial data...
CSV file path [financials.csv]: homebase_financials.csv

Step 8: Financial metrics:
---
  Monthly burn: 105,247.50
  Runway (months): 22.84
  Downside scenario burn: 126,297.00
  Runway at downside (months): 19.03
---

Step 10: Complete.
============================================================
Success!
Memo saved to: /path/to/diligence_memo.md
============================================================
```

---

## 🔧 Configuration

### Benchmark Data
Edit `benchmarks.json` to customize industry benchmarks:

```json
{
  "seed_b2b_saas": {
    "burn_range": [60000, 120000],
    "target_runway_months": 12,
    "burn_per_employee": 15000
  }
}
```

### MiniMax Model
Change the AI model in `minimax_helper.py`:
```python
def chat_completion(system_prompt, user_prompt, model="MiniMax-M2"):
```

---

## 🐛 Troubleshooting

### "MINIMAX_API_KEY not found"
**Fix:** Ensure your `.env` file exists and has no quotes around values:
```
MINIMAX_API_KEY=sk-xxxxx
MINIMAX_GROUP_ID=123456
```

### "Invalid API key" (Error 2049)
**Fix:** 
1. Check your API key is correct
2. Verify Group ID matches your API key
3. Go to MiniMax dashboard and regenerate if needed

### "Module not found: requests"
**Fix:** Install dependencies:
```bash
pip3 install requests python-dotenv pandas
```

### Python version error
**Fix:** Upgrade to Python 3.10+:
```bash
brew install python@3.11
```
Or download from [python.org](https://www.python.org/downloads/)

---

## 🎯 Use Cases

- **VC Firms**: Automate first-pass financial diligence
- **Accelerators**: Screen applicants at scale
- **Angel Investors**: Quick sanity checks on financials
- **Founders**: Self-assess before fundraising
- **Investment Committees**: Generate consistent analysis reports

---

## 🛠️ Tech Stack

- **Python 3.11**: Core language
- **MiniMax API**: AI text analysis and generation
- **OpenCorporates API**: Competitor research
- **pandas**: Financial data processing
- **python-dotenv**: Environment configuration

---

## 📝 Sample Output

The tool generates memos like this:

```markdown
# Financial Diligence Memo — Seed B2B SaaS

## Executive summary
Current monthly burn ($105k) sits within the seed B2B SaaS benchmark 
range. Runway (22.8 months) exceeds the 12-month seed target, providing 
adequate time to reach the $150K MRR milestone...

## 1. Burn assessment
- Monthly burn: $105,247
- Benchmark: $60k–$120k
- Assessment: Within normal range for seed stage
...
```

---

## 🤝 Contributing

Contributions welcome! Areas for improvement:
- Additional benchmark categories
- PDF report generation
- Multi-currency support
- Visualization dashboards
- API endpoint wrapper

---

## 📄 License

MIT License - feel free to use for personal or commercial projects.

---

## 🙏 Acknowledgments

- Built with [MiniMax AI](https://www.minimax.chat/)
- Company data from [OpenCorporates](https://opencorporates.com/)
- Benchmarks based on industry standards from Y Combinator, a16z, and Sequoia

---

## 📧 Contact

For questions or feedback, open an issue on GitHub.

---

**Built with ❤️ for the VC community**
