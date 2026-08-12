#!/usr/bin/env python3
"""
Master Data Cleaning & Wrangling Pipeline Execution Script
"""
import os
import sys

# Ensure src directory is in path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from cleaner import run_cleaning_pipeline
from audit import generate_audit_report
from visualize import generate_all_visualizations

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    raw_path = os.path.join(base_dir, 'data', 'raw_ds_jobs.csv')
    clean_path = os.path.join(base_dir, 'data', 'cleaned_ds_jobs.csv')
    report_path = os.path.join(base_dir, 'reports', 'data_quality_report.json')
    charts_dir = os.path.join(base_dir, 'charts')

    print("🚀 STEP 1: Running Data Cleaning & Feature Extraction Pipeline...")
    clean_df = run_cleaning_pipeline(raw_path, clean_path)

    print("\n📊 STEP 2: Generating Data Health & Quality Audit Report...")
    report = generate_audit_report(raw_path, clean_path, report_path)

    print("\n🎨 STEP 3: Rendering High-Impact Dark-Theme Visualizations...")
    generate_all_visualizations(clean_path, charts_dir)

    print("\n✨ PIPELINE COMPLETE! All outputs generated cleanly.")
    print(f"📁 Cleaned Data: {clean_path}")
    print(f"📁 Audit Report: {report_path}")
    print(f"📁 Charts Directory: {charts_dir}")

if __name__ == '__main__':
    main()
