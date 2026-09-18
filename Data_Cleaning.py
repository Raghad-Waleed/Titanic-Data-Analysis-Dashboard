import pandas as pd
import numpy as np
#قراءة البيانات 
df = pd.read_csv('File 3.csv', sep=';')
print("Data Unclean:")
print(df.head())

# remove dublicates
df = df.drop_duplicates()

# Handle the Nulls
df['Age'] = df['Age'].fillna(df['Age'].median())
df['Fare'] = df['Fare'].fillna(df['Fare'].median())

# drop cabin columns
df = df.drop(columns=['Cabin'])
df = df.dropna()

# Formatting & Trimming
cols_to_trim = ['PassengerId', 'Survived', 'Pclass']
for col in cols_to_trim:
    df[col] = df[col].astype(str).str.strip()

df['Sex'] = df['Sex'].astype(str).str.strip().str.capitalize()

# Handling Logical Errors
df = df[df['Age'] >= 0]
df = df[df['Fare'] >= 0]

df = df[df['Sex'].isin(['Male', 'Female'])]

# Save the Final Result
df.to_csv('cleaned_data_final.csv', index=False)

print("Data successfully cleaned!")
print(f"Number of remaining rows ready for analysis: {len(df)}")

print("\n--- Data After Cleaning (First 10 Rows) ---")
print(df.head())
