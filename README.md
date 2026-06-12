# 📊 India Data Science Job Market Analysis — Naukri Dec 2024

**Tools:** Python · SQL (MySQL) · Power BI  
**Libraries:** Pandas · Matplotlib · Seaborn  
**Dataset:** 13,691 real job listings from Naukri.com (Scraped December 2024)  
**Source:** [Kaggle — Naukri Jobs Dataset](https://www.kaggle.com/datasets/muhammetakkurt/naukri-jobs-dataset)  
**Author:** Prathiksha | [LinkedIn](https://linkedin.com/in/prathiksha23) | [GitHub](https://github.com/Prathiksha2349)

---

## 📋 Project Overview & Objectives
This project analyzes the Indian Data Science job market using a real-world dataset of **13,691 job listings** to uncover which roles, cities, skills, and companies dominate hiring. It follows an end-to-end analytics pipeline: exploratory data analysis (EDA), data cleaning via Python Regex, relational modeling in MySQL, and business intelligence reporting in Power BI.

### 🧠 Key Exploratory Data Analysis Findings
* **The Volume:** The dataset contains 13,691 job postings and 40 operational attributes.
* **The Salary Gap:** More than 90% of active job postings choose to hide salary information.
* **Data Quality Issues:** Location and experience fields contain multiple inconsistent text formats. Junk attributes (URLs, internal IDs) were stripped entirely.
* **Role Inconsistencies:** Business Analyst and Data Engineer roles appear more frequently than core Data Scientist titles within the general data scraping parameters.

---

## 🔍 8 Core Business Questions Answered

| # | Question | Chart Reference |
|---|----------|-----------------|
| 1 | Which job role pays the highest average salary? | `charts/chart1_salary_by_role.png` |
| 2 | How dramatically does experience affect salary curves? | `charts/chart2_exp_vs_salary.png` |
| 3 | What core technologies and tools do companies demand most? | `charts/chart3_skills.png` |
| 4 | Which city acts as the absolute geographic hub for data roles? | `charts/chart4_jobs_by_city.png` |
| 5 | Which top 15 corporate entities hire the most data professionals? | `charts/chart5_top_companies.png` |
| 6 | How transparent is the salary disclosure across different sectors? | `charts/chart6_salary_transparency.png` |
| 7 | Which specific experience bands hold the highest volume of openings? | `charts/chart7_exp_distribution.png` |
| 8 | How are employee sentiment and company ratings distributed? | `charts/chart8_company_ratings.png` |

---

## 🧹 Data Cleaning Challenges & Solutions

| Problem Encountered | Engineering Solution Applied |
|:---|:---|
| **90.3% Missing Salaries** (12,414 rows) | Isolated the ~1,200 disclosed records for pure benchmarking; treated salary opacity as an explicit market trend. |
| **Messy Salary Formats** (e.g., `"12-15 Lacs PA"`, `"Unpaid"`) | Parsed via Regular Expressions (`re`) to extract clean, numerical columns for minimum, maximum, and midpoint values. |
| **50+ Varied Experience Strings** (e.g., `"3-8 Yrs"`) | Extracted minimum experience years via Regex and partitioned observations into 5 uniform target bands (Fresher, Junior, Mid, Senior, Lead). |
| **Noisy, Raw Job Titles** (e.g., `// Bangalore`, `- 3 yrs plus`) | Programmatically stripped text noise and mapped hundreds of variations into 10 structured categories. |
| **Compound Location Strings** | Filtered out `"Hybrid - "` prefixes, split multi-city chains, extracted primary hiring city hubs, and standardized spellings. |
| **Comma-Separated Skill Tags** | One-hot encoded the text clusters into **14 independent binary skill flag columns** for fast aggregation. |
| **3,460 Null Company Ratings** | Excluded missing records from numerical calculations; conducted ratings distribution queries strictly on validated subsets. |
| **Date Field Outlier** (`1970-01-01`) | Coerced errors into NaT objects using Pandas and filtered out invalid historical data rows. |

---

## 📌 Key Insights

* 📢 **Salary Transparency Gap:** Only **9.7%** of listings disclose active salary brackets. The overwhelming majority choose hidden corporate budgeting during recruitment.
* 💰 **Highest Paying Career Path:** Data Architects command the highest average salary bands, followed directly by Senior Data Scientists.
* 📈 **The Experience Premium:** Clear positive correlation between experience buckets and wage ranges, showing a near 4x scaling multiplier from Fresher to Lead tiers.
* 🛠️ **The Tool Baseline:** SQL and Python form the absolute core data stack requirement across job listings, closely supported by Machine Learning frameworks.
* 📍 **Geographic Monopolies:** Bangalore massively outpaces all competing metros, accounting for nearly double the job listings of secondary hubs like Chennai.
* 🏢 **Top Hiring Vector:** Corporate recruitment is heavily driven by large global capability centers (GCCs) and technical consulting firms.
* 🎯 **Mid-Level Sweet Spot:** The 3–5 year experience band shows the single highest concentration of open job listings, signaling strong market demand for self-sufficient analysts.

---

## 📂 Repository File Structure

```text
naukri-ds-job-analysis/
├── data/
│   ├── naukri_data_scientist.csv     ← Raw Scraped Dataset (Kaggle)
│   └── naukri_cleaned.csv            ← Cleaned Production Dataset (28 engineered columns)
├── notebooks/
│   ├── phase1_explore.py             ← Initial EDA & Null Analysis
│   ├── phase2_cleaning.py            ← Advanced Text Parsing & Column Transformation
│   └── phase3_analysis.py            ← Python Chart Generation Code
├── sql/
│   └── queries.sql                   ← 10 Analytical Business Queries
├── charts/                           ← 8 Automated Matplotlib/Seaborn Chart Outputs (.png)
├── powerbi/
│   └── dashboard.pbix                ← Interactive Business Intelligence Dashboard
└── README.md                         ← Project Documentation & Portfolios
```

---

## ⚙️ Execution Pipeline

```bash
# 1. Install Required Core Libraries
pip install pandas numpy matplotlib seaborn

# 2. Execute Data Pipeline
python notebooks/phase1_explore.py
python notebooks/phase2_cleaning.py
python notebooks/phase3_analysis.py

# 3. Database & Dashboarding Layer
# - Migrate 'data/naukri_cleaned.csv' into MySQL Workspace -> Run 'sql/queries.sql'
# - Open 'powerbi/dashboard.pbix' -> Refresh data source point to view visualizations
```

---

## 🛠️ Core Skills Demonstrated
`Python Programming` `Pandas` `Data Cleaning` `Regular Expressions (Regex)` `Data Engineering` `Exploratory Data Analysis (EDA)` `Matplotlib` `Seaborn` `MySQL Workbench` `Relational Aggregations` `Power BI` `Business Intelligence`

---

## 🎙️ Pitching This Project in an Interview
> *"I built an analytics pipeline evaluating 13,691 real-world Data Science job listings scraped from Naukri.com. The primary engineering roadblock was that over 90% of salaries were hidden. I managed this transparently by routing salary-disclosed metrics into a dedicated testing path while treating market opacity itself as a distinct analytical finding. I used Python regex to normalize 50+ divergent experience strings, extracted primary hubs from composite location rows, and mapped multi-variable tool text into 14 explicit binary skill matrices. This data engine was subsequently queried via MySQL and translated into an interactive Power BI dashboard for business reporting."*
