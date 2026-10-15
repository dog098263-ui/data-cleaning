# 🧹 Data Cleaning & Preprocessing Pipeline

![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?logo=pandas&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-013243?logo=numpy&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white)
![Status](https://img.shields.io/badge/Status-Complete-brightgreen)

> A production-grade data cleaning and preprocessing pipeline applied to a real-world Data Science job postings dataset — extracting skills, normalizing salaries, parsing locations, and visualizing market insights.

---

## 📌 Project Overview

This project demonstrates a complete data wrangling workflow: ingesting raw, messy job posting data, cleaning it through automated rules, extracting structured features, and presenting the results through an interactive Streamlit dashboard.

| Attribute | Details |
|-----------|---------|
| **Domain** | Data Science Job Market |
| **Dataset** | DS Job Postings (Glassdoor) |
| **Tools** | Python, Pandas, NumPy, Regex, Streamlit |
| **Output** | Clean CSV + 5 visualizations + interactive dashboard |

---

## 🔧 What Gets Cleaned

| Problem | Raw State | Clean State |
|---------|-----------|-------------|
| **Salary Ranges** | `"$80K-$120K (Glassdoor est.)"` | `min_salary=80`, `max_salary=120`, `avg_salary=100` |
| **Company Names** | `"Healthfirst\n3.1"` | `"Healthfirst"` (rating split out) |
| **Invalid Placeholders** | `-1` or `-1.0` as text | Replaced with standard `NaN` |
| **Locations** | `"New York, NY"` | Split into `job_city`, `job_state` |
| **Skill Extraction** | Hidden in raw job description prose | 9 binary skill columns: `Python`, `SQL`, `AWS`, `Spark`, etc. |
| **Seniority Level** | Mixed job titles | Categorized: `Junior`, `Mid-Level`, `Senior`, `Manager`, `Director` |

---

## 📊 Visualizations Generated

1. **Annual Salary Distribution by Seniority Level** — Boxplot comparing compensation tiers
2. **Top Technical Skill Demand** — Python & SQL appear in 72% and 53% of postings
3. **Highest Paying Industry Sectors** — IT, Healthcare, Biotech lead compensation
4. **Top US States by Job Openings** — CA and NY dominate DS job listings
5. **Company Rating vs. Compensation** — Scatter plot colored by company age

---

## 📁 Project Structure

```
data-cleaning/
├── app.py                  # Interactive Streamlit dashboard
├── run_pipeline.py         # Run full cleaning + chart generation pipeline
├── src/                    # Core cleaning modules
├── data/                   # Raw and cleaned datasets
├── charts/                 # Generated chart images (PNG)
├── reports/                # Summary reports
├── requirements.txt        # Python dependencies
└── README.md
```

---

## 🚀 How to Run

```bash
# 1. Clone the repository
git clone https://github.com/dog098263-ui/data-cleaning.git
cd data-cleaning

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the full cleaning pipeline
python run_pipeline.py

# 4. Launch the interactive dashboard
streamlit run app.py
```

---

## 📈 Key Insights from the Data

- **Python** is the #1 most demanded skill (72% of job postings)
- **Senior Data Scientists** earn a median of **$125K/year**
- **California** has 3× more DS job openings than any other state
- Companies with ratings **4.0+** pay on average **18% more**

---

## 🛠 Tech Stack

| Tool | Purpose |
|------|---------|
| `pandas` | Data manipulation & cleaning |
| `numpy` | Numerical operations |
| `re` | Regex-based string parsing |
| `matplotlib` / `seaborn` | Visualization |
| `streamlit` | Interactive web dashboard |

---

## 👤 Author

**Aman Shakil** — [GitHub](https://github.com/dog098263-ui) · [Email](mailto:dog098263@gmail.com)

⭐ *Star this repo if you found it useful!*
