import re
import pandas as pd
import numpy as np

def clean_salary(df: pd.DataFrame) -> pd.DataFrame:
    """Extract min, max, average salary in $K (USD), handling hourly vs annual pay."""
    df = df.copy()
    
    # Identify hourly rate indicators
    df['is_hourly'] = df['Salary Estimate'].apply(lambda x: 1 if 'per hour' in str(x).lower() else 0)
    df['is_employer_provided'] = df['Salary Estimate'].apply(lambda x: 1 if 'employer provided' in str(x).lower() else 0)
    
    # Strip out extra text
    salary = df['Salary Estimate'].astype(str)
    salary = salary.apply(lambda x: x.split('(')[0]) # Remove (Glassdoor est.)
    salary = salary.apply(lambda x: x.lower().replace('per hour', '').replace('employer provided salary:', '').replace('$', '').replace('k', '').strip())
    
    def parse_salary_range(val):
        if val == '-1' or val == '' or 'unknown' in val:
            return np.nan, np.nan, np.nan
        
        # Regex to find numbers
        numbers = re.findall(r'\d+', val)
        if len(numbers) >= 2:
            min_s = float(numbers[0])
            max_s = float(numbers[1])
            avg_s = (min_s + max_s) / 2.0
            return min_s, max_s, avg_s
        elif len(numbers) == 1:
            val_s = float(numbers[0])
            return val_s, val_s, val_s
        return np.nan, np.nan, np.nan

    salary_parsed = salary.apply(parse_salary_range)
    df['min_salary_k'] = [s[0] for s in salary_parsed]
    df['max_salary_k'] = [s[1] for s in salary_parsed]
    df['avg_salary_k'] = [s[2] for s in salary_parsed]
    
    # Adjust hourly rates to annual (assuming 2080 hrs/yr -> multiply by ~2.08)
    # e.g., $25/hr -> $52K/yr
    hourly_mask = df['is_hourly'] == 1
    df.loc[hourly_mask, 'min_salary_k'] = df.loc[hourly_mask, 'min_salary_k'] * 2.08
    df.loc[hourly_mask, 'max_salary_k'] = df.loc[hourly_mask, 'max_salary_k'] * 2.08
    df.loc[hourly_mask, 'avg_salary_k'] = df.loc[hourly_mask, 'avg_salary_k'] * 2.08

    return df

def clean_company_name_and_rating(df: pd.DataFrame) -> pd.DataFrame:
    """Separate rating embedded in company name and handle missing ratings."""
    df = df.copy()
    
    # Replace invalid ratings (-1.0) with NaN
    df['Rating'] = df['Rating'].apply(lambda x: np.nan if x < 0 else x)
    
    def parse_company(row):
        name = str(row['Company Name'])
        rating = row['Rating']
        if pd.isna(rating) or '\n' not in name:
            return name.strip()
        # Company name formatted like "Healthfirst\n3.1"
        return name.split('\n')[0].strip()

    df['company_name_clean'] = df.apply(parse_company, axis=1)
    return df

def clean_location_and_hq(df: pd.DataFrame) -> pd.DataFrame:
    """Parse city and state for job location and headquarters."""
    df = df.copy()
    
    def parse_city_state(val):
        val = str(val).strip()
        if val == '-1' or val == 'Unknown' or val == '':
            return np.nan, np.nan
        parts = val.split(',')
        if len(parts) >= 2:
            city = parts[0].strip()
            state = parts[1].strip().split(' ')[0] # Extract 2-letter code
            return city, state
        elif val == 'United States' or val == 'Remote':
            return 'Remote', 'US'
        return val, np.nan

    df['job_city'], df['job_state'] = zip(*df['Location'].apply(parse_city_state))
    df['hq_city'], df['hq_state'] = zip(*df['Headquarters'].apply(parse_city_state))
    
    df['same_state'] = df.apply(
        lambda r: 1 if pd.notna(r['job_state']) and pd.notna(r['hq_state']) and r['job_state'] == r['hq_state'] else 0,
        axis=1
    )
    return df

def clean_company_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate company age and parse min/max company size."""
    df = df.copy()
    
    current_year = 2026
    df['Founded'] = pd.to_numeric(df['Founded'], errors='coerce')
    df['company_age'] = df['Founded'].apply(lambda x: current_year - x if pd.notna(x) and x > 1700 else np.nan)
    
    def parse_size(val):
        val = str(val).lower()
        if '-1' in val or 'unknown' in val or val == '':
            return np.nan, np.nan
        if '10000+' in val:
            return 10000, 50000
        numbers = re.findall(r'\d+', val)
        if len(numbers) >= 2:
            return float(numbers[0]), float(numbers[1])
        elif len(numbers) == 1:
            return float(numbers[0]), float(numbers[0])
        return np.nan, np.nan

    sizes = df['Size'].apply(parse_size)
    df['min_company_size'] = [s[0] for s in sizes]
    df['max_company_size'] = [s[1] for s in sizes]
    
    return df

def extract_skills_and_roles(df: pd.DataFrame) -> pd.DataFrame:
    """Extract key tech skills and classify job titles & seniority."""
    df = df.copy()
    desc = df['Job Description'].astype(str).str.lower()
    
    df['skill_python'] = desc.apply(lambda x: 1 if 'python' in x else 0)
    df['skill_sql'] = desc.apply(lambda x: 1 if 'sql' in x else 0)
    df['skill_excel'] = desc.apply(lambda x: 1 if 'excel' in x else 0)
    df['skill_aws'] = desc.apply(lambda x: 1 if 'aws' in x or 'amazon web services' in x or 'cloud' in x else 0)
    df['skill_spark'] = desc.apply(lambda x: 1 if 'spark' in x or 'pyspark' in x else 0)
    df['skill_hadoop'] = desc.apply(lambda x: 1 if 'hadoop' in x else 0)
    df['skill_tableau'] = desc.apply(lambda x: 1 if 'tableau' in x or 'power bi' in x or 'powerbi' in x else 0)
    df['skill_machine_learning'] = desc.apply(lambda x: 1 if 'machine learning' in x or 'ml' in x or 'scikit' in x else 0)
    df['skill_deep_learning'] = desc.apply(lambda x: 1 if 'deep learning' in x or 'pytorch' in x or 'tensorflow' in x or 'keras' in x else 0)
    
    def parse_seniority(title):
        title = str(title).lower()
        if any(w in title for w in ['sr', 'senior', 'principal', 'lead', 'head', 'staff']):
            return 'Senior'
        elif any(w in title for w in ['jr', 'junior', 'associate', 'entry']):
            return 'Junior'
        elif any(w in title for w in ['manager', 'lead']):
            return 'Manager'
        elif any(w in title for w in ['director', 'vp']):
            return 'Director'
        return 'Mid-Level'

    def parse_simplified_role(title):
        title = str(title).lower()
        if 'data scientist' in title or 'data science' in title:
            return 'Data Scientist'
        elif 'data engineer' in title:
            return 'Data Engineer'
        elif 'analyst' in title or 'analytics' in title:
            return 'Data Analyst'
        elif 'machine learning' in title or 'ml' in title:
            return 'ML Engineer'
        elif 'manager' in title:
            return 'Manager'
        elif 'director' in title:
            return 'Director'
        return 'Other DS Role'

    df['seniority'] = df['Job Title'].apply(parse_seniority)
    df['simplified_role'] = df['Job Title'].apply(parse_simplified_role)
    
    return df

def run_cleaning_pipeline(input_filepath: str, output_filepath: str) -> pd.DataFrame:
    """Run full cleaning pipeline on raw dataset."""
    df_raw = pd.read_csv(input_filepath)
    
    # Drop empty index columns if present
    if 'index' in df_raw.columns:
        df_raw = df_raw.drop(columns=['index'])
        
    df_clean = clean_salary(df_raw)
    df_clean = clean_company_name_and_rating(df_clean)
    df_clean = clean_location_and_hq(df_clean)
    df_clean = clean_company_metrics(df_clean)
    df_clean = extract_skills_and_roles(df_clean)
    
    # Save cleaned dataset
    df_clean.to_csv(output_filepath, index=False)
    print(f"✅ Successfully cleaned dataset: {len(df_clean)} rows saved to {output_filepath}")
    return df_clean

if __name__ == '__main__':
    run_cleaning_pipeline(
        input_filepath='../data/raw_ds_jobs.csv',
        output_filepath='../data/cleaned_ds_jobs.csv'
    )
