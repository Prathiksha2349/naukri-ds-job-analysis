import pandas as pd

df = pd.read_csv("Data/naukri_data_scientist.csv")

print("Shape:", df.shape)
print("\nColumns:", df.columns.tolist())
print("\nNulls:\n", df.isnull().sum())

# These are the 4 most important columns to understand
print("\n--- SALARY ---")
print(df['salary'].value_counts().head(15))

print("\n--- EXPERIENCE ---")
print(df['experience'].value_counts().head(15))

print("\n--- LOCATION ---")
print(df['location'].value_counts().head(15))

print("\n--- TITLE ---")
print(df['title'].value_counts().head(15))