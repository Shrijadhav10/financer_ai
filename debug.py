from data_loader import load_data
from categorizer import CATEGORY_MAP
import pandas as pd

documents, all_data = load_data("expense.xlsx")

print("Total rows:", len(all_data))
print("Missing dates:", all_data['date'].isna().sum())

print("\nSample data:")
print(all_data.head())

print("\nColumns:")
print(all_data.columns)

# Load data
documents, df = load_data("expense.xlsx")

print("\n✅ DATA LOADED")
print("Total rows:", len(df))

# -------------------------------
# 1. BASIC INFO
# -------------------------------
print("\n📊 BASIC INFO")
print(df.info())

# -------------------------------
# 2. TOP RAW EXPENSE VALUES
# -------------------------------
print("\n🔍 TOP RAW EXPENSE VALUES")
print(df['expense'].value_counts().head(20))

# -------------------------------
# 3. CATEGORY DISTRIBUTION
# -------------------------------
print("\n📊 CATEGORY DISTRIBUTION")
print(df['category'].value_counts().head(20))

# -------------------------------
# 4. UNMAPPED / UNKNOWN VALUES
# -------------------------------
known_categories = set(CATEGORY_MAP.keys())

unknown = df[~df['category'].isin(known_categories)]

print("\n🚨 UNMAPPED VALUES (TOP 30)")
print(unknown['category'].value_counts().head(30))

# -------------------------------
# 5. TOTAL SPEND BY CATEGORY
# -------------------------------
print("\n💰 TOTAL SPEND BY CATEGORY")
print(df.groupby('category')['price'].sum().sort_values(ascending=False).head(20))

# -------------------------------
# 6. CHECK SMALL / NOISY ENTRIES
# -------------------------------
print("\n🧹 POSSIBLE NOISE (LOW FREQUENCY)")
low_freq = df['expense'].value_counts()
print(low_freq[low_freq < 5].head(20))

# -------------------------------
# 7. SAMPLE UNKNOWN ROWS
# -------------------------------
print("\n📌 SAMPLE UNKNOWN ROWS")
print(unknown[['expense', 'price']].head(20))

# -------------------------------
# 8. DATE RANGE CHECK
# -------------------------------
print("\n📅 DATE RANGE")
print("Min date:", df['date'].min())
print("Max date:", df['date'].max())