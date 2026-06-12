import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import os

df = pd.read_csv("data/naukri_cleaned.csv")
os.makedirs("charts", exist_ok=True)
sns.set_theme(style="whitegrid")

# Salary-disclosed subset (only ~1200 rows have salary)
sal_df = df[df['sal_mid'].notna()]
print(f"Rows with salary: {len(sal_df)}")

#Chart 1 — Which role pays most? (salary-disclosed only)

role_sal = (sal_df.groupby('title_clean')['sal_mid']
            .agg(['mean','count'])
            .query('count >= 5')
            .sort_values('mean', ascending=True)
            .reset_index())

fig, ax = plt.subplots(figsize=(11, 7))
bars = ax.barh(role_sal['title_clean'], role_sal['mean'],
               color=sns.color_palette('Blues_d', len(role_sal)))
ax.set_xlabel('Average Salary (LPA)', fontsize=11)
ax.set_title('Average Salary by Role\n(Naukri Dec 2024 — disclosed salaries only)', fontsize=13, fontweight='bold')
for bar in bars:
    ax.text(bar.get_width()+0.2, bar.get_y()+bar.get_height()/2,
            f'₹{bar.get_width():.1f}L', va='center', fontsize=9)
plt.tight_layout()
plt.savefig("charts/chart1_salary_by_role.png", dpi=150)
plt.close()
print("Chart 1 done")

#Chart 2 — Experience vs salary (boxplot)
exp_order = ['Fresher (0-1)','Junior (1-3)','Mid (3-5)','Senior (5-8)','Lead (8+)']
plot_df = sal_df[sal_df['experience_clean'].isin(exp_order)]

fig, ax = plt.subplots(figsize=(12, 6))
sns.boxplot(data=plot_df, x='experience_clean', y='sal_mid',
            order=exp_order, hue='experience_clean', palette='coolwarm',
            legend=False, ax=ax)
ax.set_title('Salary by Experience Level', fontsize=13, fontweight='bold')
ax.set_xlabel('Experience')
ax.set_ylabel('Salary (LPA)')
plt.tight_layout()
plt.savefig("charts/chart2_exp_vs_salary.png", dpi=150)
plt.close()
print("Chart 2 done")

#Chart 3 — Most in-demand skills
skill_cols = [c for c in df.columns if c.startswith('skill_')]
skill_counts = df[skill_cols].sum().sort_values(ascending=True)
labels = [s.replace('skill_','').replace('_',' ').title() for s in skill_counts.index]

fig, ax = plt.subplots(figsize=(11, 7))
ax.barh(labels, skill_counts.values,
        color=sns.color_palette('Oranges_d', len(skill_counts)))
ax.set_xlabel('Number of Job Listings', fontsize=11)
ax.set_title('Most In-Demand Skills — Naukri Data Science Jobs', fontsize=13, fontweight='bold')
for i, v in enumerate(skill_counts.values):
    ax.text(v+5, i, str(int(v)), va='center', fontsize=9, fontweight='bold')
plt.tight_layout()
plt.savefig("charts/chart3_skills.png", dpi=150)
plt.close()
print("Chart 3 done")

#Chart 4 — Jobs by city (volume)
city_counts = (df[~df['city'].isin(['Remote','Unknown'])]
               ['city'].value_counts().head(12))

fig, ax = plt.subplots(figsize=(11, 7))
bars = ax.barh(city_counts.index[::-1], city_counts.values[::-1],
               color=sns.color_palette('viridis', len(city_counts)))
ax.set_xlabel('Number of Job Listings', fontsize=11)
ax.set_title('Data Science Job Listings by City', fontsize=13, fontweight='bold')
for bar in bars:
    ax.text(bar.get_width()+5, bar.get_y()+bar.get_height()/2,
            str(int(bar.get_width())), va='center', fontsize=9)
plt.tight_layout()
plt.savefig("charts/chart4_jobs_by_city.png", dpi=150)
plt.close()
print("Chart 4 done")

#Chart 5 — Top 15 hiring companies
top_companies = df['companyName'].value_counts().head(15)

fig, ax = plt.subplots(figsize=(11, 7))
bars = ax.barh(top_companies.index[::-1], top_companies.values[::-1],
               color='#457b9d')
ax.set_xlabel('Number of Job Listings', fontsize=11)
ax.set_title('Top 15 Companies Hiring Data Professionals', fontsize=13, fontweight='bold')
for bar in bars:
    ax.text(bar.get_width()+1, bar.get_y()+bar.get_height()/2,
            str(int(bar.get_width())), va='center', fontsize=9)
plt.tight_layout()
plt.savefig("charts/chart5_top_companies.png", dpi=150)
plt.close()
print("Chart 5 done")

#Chart 6 — Salary transparency: disclosed vs not
labels = ['Not Disclosed\n(12,414 jobs)', 'Salary Disclosed\n(~1,200 jobs)']
sizes  = [df['sal_mid'].isna().sum(), df['sal_mid'].notna().sum()]
colors = ['#e63946', '#457b9d']

fig, ax = plt.subplots(figsize=(8, 6))
wedges, texts, autotexts = ax.pie(sizes, labels=labels, colors=colors,
                                   autopct='%1.1f%%', startangle=90,
                                   textprops={'fontsize': 12})
ax.set_title('Salary Transparency in Indian DS Job Market\n(Key Data Quality Finding)', 
             fontsize=13, fontweight='bold')
plt.tight_layout()
plt.savefig("charts/chart6_salary_transparency.png", dpi=150)
plt.close()
print("Chart 6 done")

#Chart 7 — Experience distribution (how many jobs per level)
exp_order = ['Fresher (0-1)','Junior (1-3)','Mid (3-5)','Senior (5-8)','Lead (8+)']
exp_counts = df[df['experience_clean'].isin(exp_order)]['experience_clean'].value_counts().reindex(exp_order)

fig, ax = plt.subplots(figsize=(10, 6))
colors = ['#2ecc71','#3498db','#e67e22','#e74c3c','#9b59b6']
bars = ax.bar(exp_counts.index, exp_counts.values, color=colors, width=0.5)
ax.set_ylabel('Number of Jobs', fontsize=11)
ax.set_title('Job Openings by Experience Level', fontsize=13, fontweight='bold')
for bar in bars:
    ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+10,
            str(int(bar.get_height())), ha='center', fontsize=10, fontweight='bold')
plt.tight_layout()
plt.savefig("charts/chart7_exp_distribution.png", dpi=150)
plt.close()
print("Chart 7 done")

#Chart 8 — Company rating distribution
rated = df[df['company_rating'].notna()]

fig, ax = plt.subplots(figsize=(10, 6))
ax.hist(rated['company_rating'], bins=20, color='#457b9d', edgecolor='white')
ax.set_xlabel('Company Rating (AmbitionBox)', fontsize=11)
ax.set_ylabel('Number of Companies', fontsize=11)
ax.set_title('Distribution of Company Ratings — Naukri DS Jobs', fontsize=13, fontweight='bold')
ax.axvline(rated['company_rating'].mean(), color='red', linestyle='--',
           label=f"Mean: {rated['company_rating'].mean():.2f}")
ax.legend()
plt.tight_layout()
plt.savefig("charts/chart8_company_ratings.png", dpi=150)
plt.close()
print("Chart 8 done")
print("\nAll charts done!")