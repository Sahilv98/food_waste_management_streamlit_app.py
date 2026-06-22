import sqlite3
import pandas as pd

# connect to database
conn = sqlite3.connect("database/food_waste.db")

## load all 4 datasets into dataframes
providers = pd.read_csv("data/providers_data.csv")
receivers = pd.read_csv("data/receivers_data.csv")
food_listings = pd.read_csv("data/food_listings_data.csv")
claim_data = pd.read_csv("data/claims_data.csv")

print(claim_data)

## ------------------Preprocessing--------------------------
# 1. Drop Duplicates
providers.drop_duplicates(inplace=True)
receivers.drop_duplicates(inplace=True)
food_listings.drop_duplicates(inplace=True)
claim_data.drop_duplicates(inplace=True)

# fixing date formats
food_listings['Expiry_Date'] = pd.to_datetime(food_listings['Expiry_Date'],errors='coerce')
claim_data['Timestamp'] = pd.to_datetime(claim_data['Timestamp'],errors='coerce')

# fixing length of contact column in providers
providers['Contact'] = providers['Contact'].astype(str)
providers['Contact'] = providers['Contact'].apply(lambda x: "Unknown" if len(x.strip())<7 else x)

print(providers)

# 4. Standardize text columns to strip whitespace
for df in [providers, receivers, food_listings, claim_data]:
    df.columns = df.columns.str.strip()
    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].str.strip()

## _______PUSH to SQlite_________________________
providers.to_sql("providers", conn, if_exists="replace", index=False)
receivers.to_sql("receivers", conn, if_exists="replace", index=False)
food_listings.to_sql("food_listings", conn, if_exists="replace", index=False)
claim_data.to_sql("claims", conn, if_exists="replace", index=False)

print("✅ All 4 tables loaded and preprocessed successfully!")

print(f"Length of providers: {len(providers)}")
print(f"Length of receivers: {len(receivers)}")
print(f"Length of food_listing: {len(food_listings)}")
print(f"Length of claim_data: {len(claim_data)}")

conn.close()


