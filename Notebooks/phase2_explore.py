#"The original dataset contained 40 columns, many of which were URLs, logos, IDs, and metadata not useful for analysis. I selected 8 business-relevant columns such as title, salary, experience, location, skills, company rating, and posting date to simplify analysis and improve data quality."
import pandas as pd
import numpy as np

df = pd.read_csv("data/naukri_data_scientist.csv")
print("Raw shape:", df.shape)

# Keep only the 8 useful columns
cols_to_keep = [
    'title', 'companyName', 'location', 'experience',
    'salary', 'tagsAndSkills', 
    'ambitionBoxData/AggregateRating',
    'createdDate'
]

df = df[cols_to_keep].copy()

# Rename for easier use
df.rename(columns={
    'ambitionBoxData/AggregateRating': 'company_rating',
    'tagsAndSkills': 'skills'
}, inplace=True)

print("After column drop:", df.shape)

# remove duplicate block b

before = len(df)
df.drop_duplicates(inplace=True)
print(f"Duplicates removed: {before - len(df)}")

# Remove unpaid rows (internships — different population)
df = df[df['salary'] != 'Unpaid']

# Remove USD rows (only 9 — too few, different context)
# We'll handle this by keeping INR-equivalent ones

# Fix bad date (1970 is clearly wrong)
df['createdDate'] = pd.to_datetime(df['createdDate'], errors='coerce')
df = df[df['createdDate'].dt.year >= 2020]
print("After bad row removal:", len(df))

#clean job titles-block c
def clean_title(t):
    t = str(t).lower()
    # Remove noise like "// Bangalore", "- 3 yrs plus"
    import re
    t = re.sub(r'[/\\|].*', '', t).strip()
    t = re.sub(r'-\s*\d+.*', '', t).strip()
    
    if 'business analyst' in t:          return 'Business Analyst'
    elif 'data engineer' in t or 'de -' in t: return 'Data Engineer'
    elif 'senior data scientist' in t:   return 'Senior Data Scientist'
    elif 'data scientist' in t:          return 'Data Scientist'
    elif 'data analyst' in t:            return 'Data Analyst'
    elif 'machine learning' in t or 'ml engineer' in t: return 'ML Engineer'
    elif 'data architect' in t:          return 'Data Architect'
    elif 'big data' in t:                return 'Big Data Engineer'
    elif 'analyst' in t:                 return 'Analyst'
    elif 'developer' in t:               return 'Developer'
    else:                                return 'Other'

df['title_clean'] = df['title'].apply(clean_title)
print("\nCleaned title distribution:")
print(df['title_clean'].value_counts())

#roup the messy experience column into simple, readable buckets like Entry, Mid, and Senior,block :d
def clean_experience(e):
    if pd.isna(e): return 'Unknown'
    e = str(e).lower().replace('yrs','').replace('yr','').strip()
    
    # Extract minimum years from range like "3-5"
    import re
    nums = re.findall(r'\d+', e)
    if not nums: return 'Unknown'
    
    min_exp = int(nums[0])
    if min_exp == 0:   return 'Fresher (0-1)'
    elif min_exp <= 2: return 'Junior (1-3)'
    elif min_exp <= 4: return 'Mid (3-5)'
    elif min_exp <= 7: return 'Senior (5-8)'
    else:              return 'Lead (8+)'

df['experience_clean'] = df['experience'].apply(clean_experience)
print("\nExperience distribution:")
print(df['experience_clean'].value_counts())

#clean salary
def parse_salary(s):
    if pd.isna(s) or 'not disclosed' in str(s).lower():
        return None, None, None
    
    import re
    s = str(s).lower().replace('lacs pa','').replace('lpa','').strip()
    nums = re.findall(r'\d+\.?\d*', s)
    
    if len(nums) >= 2:
        low  = float(nums[0])
        high = float(nums[1])
        mid  = round((low + high) / 2, 1)
        return low, high, mid
    elif len(nums) == 1:
        val = float(nums[0])
        return val, val, val
    return None, None, None

df['sal_min'], df['sal_max'], df['sal_mid'] = zip(*df['salary'].apply(parse_salary))

disclosed = df['sal_mid'].notna().sum()
total = len(df)
print(f"\nSalary disclosed: {disclosed} / {total} ({round(disclosed/total*100,1)}%)")
print(f"Salary NOT disclosed: {total - disclosed}")
print(f"\nAmong disclosed — salary range:")
print(df['sal_mid'].describe())

#Block F — Clean location
def extract_city(loc):
    if pd.isna(loc): return 'Unknown'
    loc = str(loc)
    
    # Remove "Hybrid - " prefix
    loc = loc.replace('Hybrid - ', '').replace('hybrid - ', '')
    
    # Take only first city if multiple listed
    city = loc.split(',')[0].strip()
    
    # Standardize spellings
    city_map = {
        'Bengaluru': 'Bangalore',
        'bangalore': 'Bangalore',
        'bengaluru': 'Bangalore',
        'Mumbai (All Areas)': 'Mumbai',
        'New Delhi': 'Delhi',
        'gurugram': 'Gurgaon',
        'Gurugram': 'Gurgaon',
    }
    return city_map.get(city, city)

df['city'] = df['location'].apply(extract_city)
print("\nTop cities after cleaning:")
print(df['city'].value_counts().head(10))

#Create skill flag columns

top_skills = [
    'Python', 'SQL', 'Machine Learning', 'Deep Learning',
    'Power BI', 'Tableau', 'NLP', 'Azure', 'AWS',
    'Spark', 'TensorFlow', 'PyTorch', 'Excel', 'Statistics'
]

for skill in top_skills:
    col = f"skill_{skill.lower().replace(' ','_')}"
    df[col] = df['skills'].str.contains(skill, case=False, na=False).astype(int)

print("\nSkill demand:")
skill_cols = [c for c in df.columns if c.startswith('skill_')]
print(df[skill_cols].sum().sort_values(ascending=False))

#Save
df.to_csv("data/naukri_cleaned.csv", index=False)
print("\nSaved! Final shape:", df.shape)
print("Columns:", df.columns.tolist())