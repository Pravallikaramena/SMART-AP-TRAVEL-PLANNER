import pandas as pd
import os

csv_path = r'datasets\AP_DATASET.CSV'
backup_path = r'datasets\AP_DATASET_BACKUP.CSV'

if not os.path.exists(backup_path):
    import shutil
    shutil.copy2(csv_path, backup_path)
    print(f"Backup created at {backup_path}")

# List of famous temples to prioritize
famous_names = [
    "Sri Siddhi Vinayaka Swamy Temple",
    "Sri Jagan Mohini Kesava Swamy Temple",
    "Sri Venkateswara Swamy Temple (Tirumala)",
    "Sri Mallikarjuna Swamy Temple",
    "Sri Kanaka Durga Temple",
    "Sri Satyanarayana Swamy Temple",
    "Sri Varaha Lakshmi Narasimha Swamy Temple",
    "Sri Bhramaramba Mallikarjuna Swamy Temple",
    "Sri Veerabhadra Swamy Temple",
    "Sri Lakshmi Narasimha Swamy Temple",
    "Sri Panakala Lakshmi Narasimha Swamy Temple",
    "Sri Venkateswara Swamy Temple (Dwaraka Tirumala)",
    "Sri Ksheera Ramalingeswara Swamy Temple",
    "Sri Someswara Swamy Temple",
    "Sri Amareswara Swamy Temple",
    "Sri Bhimeswara Swamy Temple",
    "Sri Kalahasteeswara Swamy Temple",
    "Sri Mukhalingeswara Swamy Temple",
    "Ahobilam Nava Narasimha Temples"
]

# Read the data
df = pd.read_csv(csv_path)

# 1. Clean duplicated places (case-insensitive and strip)
df['Tourist_Place_Clean'] = df['Tourist_Place'].astype(str).str.strip().str.lower()
df = df.drop_duplicates(subset=['Tourist_Place_Clean'], keep='first')

# 2. Identify famous temples and elevate them
# We'll create a masking logic
is_famous = df['Tourist_Place'].astype(str).str.contains('|'.join([f"^{n}$" for n in famous_names]), case=False, na=False, regex=True)

# Also catch near-matches for Tirumala
is_famous |= df['Tourist_Place'].astype(str).str.contains("Venkateswara", case=False, na=False) & df['City_Name'].astype(str).str.contains("Tirumala|Tirupati", case=False, na=False)
is_famous |= df['Tourist_Place'].astype(str).str.contains("Ainavilli.*Temple", case=False, na=False)

# 3. Set ratings
df.loc[is_famous, 'Rating'] = 5.0

# 4. LOWER ratings of generic-sounding places in those same cities to ensure famous ones win the ai_score
famous_cities = df[is_famous]['City_Name'].unique()
generic_keywords = ["Viewpoint", "Trail", "Monolith", "Monument", "Grove", "Museum", "Promenade", "Bridge", "Canal", "Layout", "Phase", "Market", "Center"]

mask_generic = (df['City_Name'].isin(famous_cities)) & \
               (df['Tourist_Place'].astype(str).str.contains('|'.join(generic_keywords), case=False, na=False)) & \
               (~is_famous)

df.loc[mask_generic, 'Rating'] = 4.0

# 5. Bring famous temples to the TOP
top_df = df[is_famous].copy()
rest_df = df[~is_famous].copy()

# Sort top_df by name to keep it neat
top_df = top_df.sort_values(by='City_Name')

# Combine
final_df = pd.concat([top_df, rest_df], ignore_index=True)

# Remove the temporary helper column
final_df = final_df.drop(columns=['Tourist_Place_Clean'])

# Save
final_df.to_csv(csv_path, index=False)

print(f"Successfully cleaned and prioritized {len(top_df)} famous temples.")
print(f"Updated ratings for generic spots in {len(famous_cities)} cities.")
