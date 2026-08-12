import os
import json
import pandas as pd
import numpy as np
import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Data Science Job Postings Analytics",
    page_icon="🧹",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for glassmorphism dark mode UI
st.markdown("""
<style>
    .main {
        background-color: #0f172a;
        color: #f8fafc;
    }
    .metric-card {
        background: rgba(30, 41, 59, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        text-align: center;
    }
    .metric-val {
        font-size: 2rem;
        font-weight: 700;
        color: #6366f1;
    }
    .metric-lbl {
        font-size: 0.875rem;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 10px 16px;
        background-color: #1e293b;
        color: #94a3b8;
    }
    .stTabs [aria-selected="true"] {
        background-color: #6366f1 !important;
        color: #ffffff !important;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    raw_path = os.path.join(base_dir, 'data', 'raw_ds_jobs.csv')
    clean_path = os.path.join(base_dir, 'data', 'cleaned_ds_jobs.csv')
    report_path = os.path.join(base_dir, 'reports', 'data_quality_report.json')
    
    df_raw = pd.read_csv(raw_path)
    df_clean = pd.read_csv(clean_path)
    
    report = {}
    if os.path.exists(report_path):
        with open(report_path, 'r') as f:
            report = json.load(f)
            
    return df_raw, df_clean, report

df_raw, df_clean, report = load_data()

st.title("🧹 Data Science Job Postings — Cleaning & Analytics Dashboard")
st.caption("Interactive Portfolio App demonstrating automated Data Wrangling, Regex Extraction, and Salary Analytics")

# Sidebar Filters
st.sidebar.header("🔍 Global Dataset Filters")

selected_seniority = st.sidebar.multiselect(
    "Filter Seniority Level:",
    options=list(df_clean['seniority'].dropna().unique()),
    default=list(df_clean['seniority'].dropna().unique())
)

selected_states = st.sidebar.multiselect(
    "Filter US States:",
    options=list(df_clean['job_state'].dropna().unique()),
    default=['CA', 'NY', 'MA', 'VA', 'IL'] if 'CA' in df_clean['job_state'].values else list(df_clean['job_state'].dropna().unique())[:5]
)

# Apply Sidebar Filters
df_filtered = df_clean[
    (df_clean['seniority'].isin(selected_seniority)) &
    (df_clean['job_state'].isin(selected_states))
]

# Tabs Layout
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Pipeline Health & Audit", 
    "📈 Salary & Skill Analytics", 
    "🧮 Interactive Salary Estimator", 
    "📁 Clean Dataset Viewer"
])

with tab1:
    st.subheader("Data Cleaning Health Summary")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f'<div class="metric-card"><div class="metric-val">{len(df_raw)}</div><div class="metric-lbl">Raw Job Postings</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="metric-card"><div class="metric-val">{len(df_clean["avg_salary_k"].dropna())}</div><div class="metric-lbl">Cleaned Salary Records</div></div>', unsafe_allow_html=True)
    with col3:
        avg_sal = df_clean['avg_salary_k'].mean()
        st.markdown(f'<div class="metric-card"><div class="metric-val">${int(avg_sal)}K</div><div class="metric-lbl">Avg Annual Salary</div></div>', unsafe_allow_html=True)
    with col4:
        top_skill = "Python"
        st.markdown(f'<div class="metric-card"><div class="metric-val">{int(df_clean["skill_python"].sum())}</div><div class="metric-lbl">Python Job Mentions</div></div>', unsafe_allow_html=True)

    st.divider()
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("### 🛠️ Key Data Transformations Executed")
        st.markdown("""
        - **Salary Parsing**: Extracted `min_salary_k`, `max_salary_k`, and `avg_salary_k` using Regex, converted hourly rates ($24/hr $\\rightarrow$ $50K/yr), and removed `(Glassdoor est.)` text.
        - **Company Name Sanitization**: Stripped ratings embedded in company strings (e.g., `Healthfirst\\n3.1`).
        - **Location & HQ Parsing**: Extracted `job_city`, `job_state`, `hq_state`, and calculated `same_state` residency matching.
        - **Skill Extraction**: Created binary flags for `Python`, `SQL`, `AWS`, `Spark`, `Tableau`, `Excel`, `Machine Learning`, `Deep Learning`.
        """)
        
    with col_b:
        st.markdown("### 📋 Before vs After Missing Value Resolution")
        st.markdown("""
        - **Raw Dataset**: Contain `'-1'` placeholders for Company Rating, Size, Revenue, Founded Year.
        - **Cleaned Dataset**: Converted `-1` placeholders to `NaN` to prevent biased statistical averages.
        """)

with tab2:
    st.subheader("Data Science Compensation & Market Demand")
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("#### Salary Distribution by Seniority")
        st.bar_chart(df_filtered.groupby('seniority')['avg_salary_k'].mean())
        
    with c2:
        st.markdown("#### Technical Skill Demand Frequency")
        skill_cols = [c for c in df_clean.columns if c.startswith('skill_')]
        skill_sum = df_filtered[skill_cols].sum()
        skill_sum.index = [c.replace('skill_', '').replace('_', ' ').title() for c in skill_sum.index]
        st.bar_chart(skill_sum)

with tab3:
    st.subheader("🧮 Custom Data Science Salary Calculator")
    st.write("Select your profile options to estimate your expected annual market salary ($K USD):")
    
    calc_col1, calc_col2, calc_col3 = st.columns(3)
    with calc_col1:
        user_seniority = st.selectbox("Seniority Level", options=['Junior', 'Mid-Level', 'Senior', 'Manager', 'Director'])
    with calc_col2:
        user_state = st.selectbox("Job State Location", options=sorted(list(df_clean['job_state'].dropna().unique())))
    with calc_col3:
        user_skills = st.multiselect("Your Technical Skills", options=['Python', 'SQL', 'AWS', 'Spark', 'Machine Learning', 'Tableau'], default=['Python', 'SQL'])
        
    # Simple Estimation Logic
    base_salary = df_clean[df_clean['seniority'] == user_seniority]['avg_salary_k'].median()
    if pd.isna(base_salary):
        base_salary = df_clean['avg_salary_k'].median()
        
    state_df = df_clean[df_clean['job_state'] == user_state]['avg_salary_k']
    state_bonus = (state_df.mean() - df_clean['avg_salary_k'].mean()) if len(state_df) > 0 else 0
    skill_bonus = len(user_skills) * 4.5
    
    estimated_val = base_salary + (state_bonus * 0.5) + skill_bonus
    
    st.success(f"### Estimated Annual Salary Range: **${int(estimated_val - 12)}K — ${int(estimated_val + 15)}K USD**")
    st.caption("Based on benchmark statistics from 672 Glassdoor Data Science job listings.")

with tab4:
    st.subheader("📁 Explore Cleaned Dataset")
    st.dataframe(df_filtered, use_container_width=True)
    
    csv_bytes = df_clean.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Cleaned Dataset CSV",
        data=csv_bytes,
        file_name="cleaned_ds_jobs.csv",
        mime="text/csv"
    )
