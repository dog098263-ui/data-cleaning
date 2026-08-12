import json
import pandas as pd
import numpy as np

def generate_audit_report(raw_filepath: str, clean_filepath: str, report_filepath: str) -> dict:
    """Generate before-and-after data health metrics and save to JSON."""
    raw_df = pd.read_csv(raw_filepath)
    clean_df = pd.read_csv(clean_filepath)
    
    # Calculate nulls and placeholder count (-1) in raw
    raw_placeholders = (raw_df.astype(str) == '-1').sum().to_dict()
    raw_nulls = raw_df.isnull().sum().to_dict()
    
    # Calculate clean features data health
    clean_nulls = clean_df.isnull().sum().to_dict()
    
    # Skill statistics
    skill_cols = [col for col in clean_df.columns if col.startswith('skill_')]
    skill_counts = {col.replace('skill_', '').title(): int(clean_df[col].sum()) for col in skill_cols}
    
    # Summary stats
    salary_valid = clean_df['avg_salary_k'].dropna()
    salary_stats = {
        'min_k': float(salary_valid.min()),
        'max_k': float(salary_valid.max()),
        'mean_k': float(round(salary_valid.mean(), 2)),
        'median_k': float(salary_valid.median()),
        'valid_records': int(len(salary_valid)),
        'missing_records': int(clean_df['avg_salary_k'].isnull().sum())
    }
    
    report = {
        'total_raw_records': int(len(raw_df)),
        'total_cleaned_records': int(len(clean_df)),
        'raw_columns': list(raw_df.columns),
        'cleaned_columns': list(clean_df.columns),
        'placeholders_removed': raw_placeholders,
        'clean_null_counts': clean_nulls,
        'salary_summary_k_usd': salary_stats,
        'skill_demand_counts': skill_counts,
        'seniority_breakdown': clean_df['seniority'].value_counts().to_dict(),
        'top_10_states': clean_df['job_state'].value_counts().head(10).to_dict()
    }
    
    with open(report_filepath, 'w') as f:
        json.dump(report, f, indent=4)
        
    print(f"📊 Audit Report generated and saved to {report_filepath}")
    return report

if __name__ == '__main__':
    generate_audit_report(
        raw_filepath='../data/raw_ds_jobs.csv',
        clean_filepath='../data/cleaned_ds_jobs.csv',
        report_filepath='../reports/data_quality_report.json'
    )
