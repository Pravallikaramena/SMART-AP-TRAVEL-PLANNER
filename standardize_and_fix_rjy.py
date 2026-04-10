import pandas as pd
import os

csv_path = r'datasets\AP_DATASET.CSV'

if not os.path.exists(csv_path):
    print(f"Error: {csv_path} not found.")
    exit(1)

# Step 1: Detect delimiter and read correctly
# The user's last upload was Tab-Separated (TSV) based on diagnostic
try:
    df = pd.read_csv(csv_path, sep='\t', engine='python')
    if 'City_Name' not in df.columns:
         # Try comma if tab failed
         df = pd.read_csv(csv_path)
except Exception as e:
    print("Fallback to normal read_csv...")
    df = pd.read_csv(csv_path)

print(f"Initial row count: {len(df)}")
print(f"Current Columns: {df.columns.tolist()}")

# Step 2: Fix Rajahmundry ISKCON duplicate
# Identify the duplicate (usually one with missing/distorted area)
rjy_iskcon_mask = (df['City_Name'] == 'Rajahmundry') & (df['Tourist_Place'].str.contains('ISKCON|Iskcon', case=False, na=False))
rjy_iskcon_count = len(df[rjy_iskcon_mask])

if rjy_iskcon_count > 1:
    # Keep the best one (usually first)
    best_iskcon_idx = df[rjy_iskcon_mask].index[0]
    df.loc[best_iskcon_idx, 'Area_Name'] = 'Gouthami Ghat'
    df.loc[best_iskcon_idx, 'Rating'] = 5.0
    df.loc[best_iskcon_idx, 'Final_Rating'] = 5.0
    df.loc[best_iskcon_idx, 'Entry_Fee'] = 'Free'
    
    # Remove the extra ones
    others = df[rjy_iskcon_mask].index[1:]
    df = df.drop(others)
    print(f"Removed {len(others)} duplicate ISKCON(s) from Rajahmundry.")

# Step 3: Add 'Cotton Museum (Dowleswaram Barrage)' as a replacement/flagship
cotton_museum = {
    'City_Name': 'Rajahmundry', 'District_Name': 'East Godavari', 'Area_Name': 'Dowleswaram',
    'Latitude': 16.9400, 'Longitude': 81.7822, 'Tourist_Place': 'Sir Arthur Cotton Museum & Barrage',
    'Description': 'Historical Museum documenting the Irrigation Wonder of Godavari', 
    'Rating': 5.0, 'Final_Rating': 5.0, 'Entry_Fee': 'Paid', 'Hotel': 'Rive Bay Resort'
}

# Ensure row alignment with columns
row_dict = {col: 'N/A' for col in df.columns}
row_dict.update(cotton_museum)
new_row_df = pd.DataFrame([row_dict])
df = pd.concat([df, new_row_df], ignore_index=True)
print("Added Cotton Museum as Rajahmundry flagship.")

# Step 4: Final Standardization (Clean up all 7,000+ rows)
# Clean up nan in ratings for new rows (Paderu, etc.)
df['Rating'] = pd.to_numeric(df['Rating'], errors='coerce').fillna(4.0)
df['Final_Rating'] = pd.to_numeric(df['Final_Rating'], errors='coerce').fillna(4.0)
df.loc[df['Rating'] > 5.0, 'Rating'] = 5.0
df.loc[df['Final_Rating'] > 5.0, 'Final_Rating'] = 5.0

# Ensure 'Entry_Fee' column is healthy
if 'Entry_Fee' not in df.columns:
    df['Entry_Fee'] = 'Paid/NA'
    
# Apply 'Free' to all religious spots globally
rel_keywords = ["Temple", "Mosque", "Church", "Dargah", "Devipuram", "ISKCON"]
for kw in rel_keywords:
    df.loc[df['Tourist_Place'].str.contains(kw, case=False, na=False), 'Entry_Fee'] = 'Free'

# Save back as proper COMMA-separated CSV
df.to_csv(csv_path, index=False)
print(f"Final Standardization Applied! Row count: {len(df)}")
