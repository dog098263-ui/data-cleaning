import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set dark aesthetic plotting style
plt.style.use('dark_background')
plt.rcParams['font.sans-serif'] = 'Helvetica'
plt.rcParams['axes.edgecolor'] = '#333333'
plt.rcParams['axes.linewidth'] = 0.8

PRIMARY_COLOR = '#6366f1'
ACCENT_COLORS = ['#6366f1', '#ec4899', '#10b981', '#f59e0b', '#8b5cf6', '#06b6d4', '#f43f5e']

def plot_salary_by_seniority(df: pd.DataFrame, output_dir: str):
    """1. Salary distribution boxplot by Seniority level."""
    plt.figure(figsize=(10, 6))
    
    order = ['Junior', 'Mid-Level', 'Senior', 'Manager', 'Director']
    existing_order = [o for o in order if o in df['seniority'].unique()]
    
    ax = sns.boxplot(
        data=df, 
        x='seniority', 
        y='avg_salary_k', 
        order=existing_order,
        palette='magma',
        boxprops=dict(alpha=0.8)
    )
    
    plt.title('Data Science Annual Salary ($K USD) by Seniority Level', fontsize=14, fontweight='bold', pad=15, color='#ffffff')
    plt.xlabel('Seniority Level', fontsize=12, fontweight='bold', color='#a1a1aa')
    plt.ylabel('Average Annual Salary ($K)', fontsize=12, fontweight='bold', color='#a1a1aa')
    plt.grid(axis='y', linestyle='--', alpha=0.3)
    
    # Add median labels
    medians = df.groupby('seniority')['avg_salary_k'].median()
    for i, label in enumerate(existing_order):
        if label in medians and pd.notna(medians[label]):
            median_val = medians[label]
            ax.text(i, median_val + 3, f"${int(median_val)}K", horizontalalignment='center', size=10, color='#ffffff', weight='semibold')
            
    plt.tight_layout()
    output_path = os.path.join(output_dir, 'salary_distribution_by_seniority.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"📊 Saved: {output_path}")

def plot_top_demanded_skills(df: pd.DataFrame, output_dir: str):
    """2. Bar chart of top demanded technical skills in job descriptions."""
    skill_cols = [c for c in df.columns if c.startswith('skill_')]
    skill_counts = df[skill_cols].sum().sort_values(ascending=True)
    
    # Clean column names
    skill_names = [c.replace('skill_', '').replace('_', ' ').title() for c in skill_counts.index]
    
    plt.figure(figsize=(10, 6))
    bars = plt.barh(skill_names, skill_counts.values, color='#6366f1', edgecolor='#818cf8', linewidth=1)
    
    plt.title('Most In-Demand Skills in Data Science Job Postings', fontsize=14, fontweight='bold', pad=15, color='#ffffff')
    plt.xlabel('Number of Job Mentioned In (out of 672)', fontsize=12, fontweight='bold', color='#a1a1aa')
    plt.ylabel('Technical Skill', fontsize=12, fontweight='bold', color='#a1a1aa')
    plt.grid(axis='x', linestyle='--', alpha=0.3)
    
    # Value annotations
    total_jobs = len(df)
    for bar in bars:
        width = bar.get_width()
        pct = (width / total_jobs) * 100
        plt.text(width + 8, bar.get_y() + bar.get_height()/2, f"{int(width)} ({pct:.1f}%)", 
                 va='center', ha='left', fontsize=10, color='#e4e4e7', weight='bold')
        
    plt.xlim(0, max(skill_counts.values) * 1.15)
    plt.tight_layout()
    output_path = os.path.join(output_dir, 'top_demanded_skills.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"📊 Saved: {output_path}")

def plot_top_states_jobs(df: pd.DataFrame, output_dir: str):
    """3. Top States for Data Science Jobs."""
    top_states = df['job_state'].value_counts().head(10).sort_values(ascending=True)
    
    plt.figure(figsize=(10, 6))
    plt.barh(top_states.index, top_states.values, color='#10b981', edgecolor='#34d399', linewidth=1)
    
    plt.title('Top 10 US States for Data Science Job Listings', fontsize=14, fontweight='bold', pad=15, color='#ffffff')
    plt.xlabel('Number of Job Listings', fontsize=12, fontweight='bold', color='#a1a1aa')
    plt.ylabel('State Code', fontsize=12, fontweight='bold', color='#a1a1aa')
    plt.grid(axis='x', linestyle='--', alpha=0.3)
    
    for i, v in enumerate(top_states.values):
        plt.text(v + 1, i, str(v), va='center', fontsize=10, color='#ffffff', weight='bold')
        
    plt.tight_layout()
    output_path = os.path.join(output_dir, 'ds_jobs_by_state.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"📊 Saved: {output_path}")

def plot_salary_by_sector(df: pd.DataFrame, output_dir: str):
    """4. Salary breakdown by Sector."""
    sector_df = df[df['Sector'] != '-1'].groupby('Sector')['avg_salary_k'].agg(['mean', 'count']).reset_index()
    sector_df = sector_df[sector_df['count'] >= 5].sort_values(by='mean', ascending=True).tail(10)
    
    plt.figure(figsize=(11, 6))
    bars = plt.barh(sector_df['Sector'], sector_df['mean'], color='#ec4899', edgecolor='#f472b6', linewidth=1)
    
    plt.title('Top 10 Highest Paying Industry Sectors ($K Avg Annual)', fontsize=14, fontweight='bold', pad=15, color='#ffffff')
    plt.xlabel('Average Annual Salary ($K)', fontsize=12, fontweight='bold', color='#a1a1aa')
    plt.ylabel('Industry Sector', fontsize=12, fontweight='bold', color='#a1a1aa')
    plt.grid(axis='x', linestyle='--', alpha=0.3)
    
    for bar in bars:
        width = bar.get_width()
        plt.text(width + 1.5, bar.get_y() + bar.get_height()/2, f"${width:.1f}K", 
                 va='center', ha='left', fontsize=10, color='#ffffff', weight='bold')
        
    plt.xlim(0, max(sector_df['mean']) * 1.15)
    plt.tight_layout()
    output_path = os.path.join(output_dir, 'salary_by_sector.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"📊 Saved: {output_path}")

def plot_company_rating_vs_salary(df: pd.DataFrame, output_dir: str):
    """5. Scatter plot of Company Rating vs Average Salary."""
    clean_sub = df.dropna(subset=['Rating', 'avg_salary_k', 'company_age'])
    
    plt.figure(figsize=(10, 6))
    scatter = plt.scatter(
        clean_sub['Rating'], 
        clean_sub['avg_salary_k'], 
        c=clean_sub['company_age'],
        cmap='viridis',
        alpha=0.75,
        edgecolors='w',
        linewidth=0.5,
        s=60
    )
    
    cbar = plt.colorbar(scatter)
    cbar.set_label('Company Age (Years)', color='#a1a1aa', weight='bold')
    cbar.ax.yaxis.set_tick_params(color='#ffffff')
    plt.setp(plt.getp(cbar.ax.axes, 'yticklabels'), color='#ffffff')
    
    plt.title('Company Rating vs Average Annual Salary ($K)', fontsize=14, fontweight='bold', pad=15, color='#ffffff')
    plt.xlabel('Glassdoor Company Rating (1.0 to 5.0)', fontsize=12, fontweight='bold', color='#a1a1aa')
    plt.ylabel('Average Annual Salary ($K USD)', fontsize=12, fontweight='bold', color='#a1a1aa')
    plt.grid(True, linestyle='--', alpha=0.25)
    
    plt.tight_layout()
    output_path = os.path.join(output_dir, 'company_rating_vs_salary.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"📊 Saved: {output_path}")

def generate_all_visualizations(clean_csv_path: str, output_dir: str):
    """Run visualization suite on clean dataset."""
    os.makedirs(output_dir, exist_ok=True)
    df = pd.read_csv(clean_csv_path)
    
    plot_salary_by_seniority(df, output_dir)
    plot_top_demanded_skills(df, output_dir)
    plot_top_states_jobs(df, output_dir)
    plot_salary_by_sector(df, output_dir)
    plot_company_rating_vs_salary(df, output_dir)
    print("🎨 All 5 dark-theme chart visualizations generated successfully!")

if __name__ == '__main__':
    generate_all_visualizations(
        clean_csv_path='../data/cleaned_ds_jobs.csv',
        output_dir='../charts'
    )
