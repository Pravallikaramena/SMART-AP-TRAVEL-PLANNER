import pandas as pd
import os

csv_path = r'datasets\AP_DATASET.CSV'
backup_path = r'datasets\AP_DATASET_BACKUP.CSV'

if not os.path.exists(backup_path):
    print(f"Error: Backup {backup_path} not found.")
    exit(1)

# Read the data
df = pd.read_csv(csv_path)
df_backup = pd.read_csv(backup_path)

# 1. Restore Tirumala Temple
main_temple_name = "Sri Venkateswara Swamy Temple (Tirumala)"
# Target in backup: Sri Venkateswara Temple (Tirumala) in Tirupati/Chittoor
is_backup_temple = (df_backup['Tourist_Place'].astype(str).str.contains("Venkateswara Temple", case=False, na=False)) & \
                  (df_backup['City_Name'].astype(str).str.contains("Tirupati|Tirumala", case=False, na=False))

main_df = df_backup[is_backup_temple].head(1).copy()

if not main_df.empty:
    main_df.iloc[0, main_df.columns.get_loc('Tourist_Place')] = main_temple_name
    main_df.iloc[0, main_df.columns.get_loc('Rating')] = 5.0
    print(f"Restored main temple: {main_temple_name}")
else:
    print("Warning: Could not find main temple in backup.")

# 2. Identify the nearby spots that are currently competing
nearby_places = [
    "ISKCON Temple Tirupati",
    "Sri Kapileswara Swamy Temple",
    "Sri Padmavathi Ammavari Temple"
]

# Ensure they have slightly lower rating than the main temple (4.9)
mask_nearby = df['Tourist_Place'].isin(nearby_places)
df.loc[mask_nearby, 'Rating'] = 4.9

# 3. Handle duplicates: remove any main temple entries that might still be in df
is_main_in_df = (df['Tourist_Place'].astype(str).str.contains("Venkateswara Swamy Temple", case=False, na=False)) & \
                (df['City_Name'].astype(str).str.contains("Tirumala|Tirupati", case=False, na=False))
df = df[~is_main_in_df]

# 4. Final Ordering: Main Temple FIRST, then everything else
final_df = pd.concat([main_df, df], ignore_index=True)

# 5. Clean whitespace
for col in final_df.select_dtypes(include=['object']):
    final_df[col] = final_df[col].astype(str).str.strip()

# Save
final_df.to_csv(csv_path, index=False)

print(f"Successfully restored {main_temple_name} and set it as #1.")
