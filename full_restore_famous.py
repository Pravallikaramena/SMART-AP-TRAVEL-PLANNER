import pandas as pd
import os

csv_path = r'datasets\AP_DATASET.CSV'
backup_path = r'datasets\AP_DATASET_BACKUP.CSV' # Original 6891-row backup

if not os.path.exists(backup_path):
    print(f"Error: Original backup {backup_path} not found.")
    exit(1)

# 1. Load Original Dataset
df_original = pd.read_csv(backup_path)
df_original.columns = df_original.columns.str.strip()
print(f"Loaded original backup with {len(df_original)} rows.")

# 2. Strategic Mapping: Map NTR district cities to "Vijayawada" to "unlock" the 4000+ rows
mask_vj = df_original['District_Name'].astype(str).str.contains("NTR", case=False, na=False)
df_original.loc[mask_vj, 'City_Name'] = "Vijayawada"
print(f"Mapped {sum(mask_vj)} rows in NTR district to 'Vijayawada' for better search visibility.")

# Similarly for Tirupati/Chittoor area if needed
mask_tiru = (df_original['District_Name'].astype(str).str.contains("Chittoor|Tirupati", case=False, na=False)) & \
            (df_original['Area_Name'].astype(str).str.contains("Tirumala|Tirupati|Alipiri", case=False, na=False))
df_original.loc[mask_tiru, 'City_Name'] = "Tirupati"

# 3. List of Famous Temples and Places I've added/curated
famous_places_list = [
    ["Tirupati", "Chittoor", "Tirumala Hills", 13.6833, 79.4300, "Sri Venkateswara Swamy Temple (Tirumala)", "N/A", "Tirupati", 5.0, "N/A", "N/A", 0, "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", 5.0],
    ["Ainavilli", "Konaseema", "Ainavilli Temple Area", 16.6622, 82.0129, "Sri Siddhi Vinayaka Swamy Temple", "N/A", "Amalapuram", 5.0, "N/A", "N/A", 0, "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", 5.0],
    ["Vijayawada", "NTR", "Indrakeeladri", 16.5161, 80.6067, "Sri Kanaka Durga Temple", "N/A", "Vijayawada", 5.0, "N/A", "N/A", 0, "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", 5.0],
    ["Srisailam", "Nandyal", "Srisailam Temple Road", 16.0740, 78.8650, "Sri Bhramaramba Mallikarjuna Swamy Temple", "N/A", "N/A", 5.0, "N/A", "N/A", 0, "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", 5.0],
    ["Ryali", "Konaseema", "Ryali Temple Area", 16.7833, 81.8833, "Sri Jagan Mohini Kesava Swamy Temple", "N/A", "Rajahmundry", 5.0, "N/A", "N/A", 0, "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", 5.0],
    ["Vadapalli", "Konaseema", "Vadapalli Temple Area", 16.7167, 81.9167, "Sri Lakshmi Narasimha Swamy Temple", "N/A", "Rajahmundry", 5.0, "N/A", "N/A", 0, "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", 5.0],
    ["Annavaram", "Kakinada", "Ratnagiri Hill", 17.2833, 82.4167, "Sri Satyanarayana Swamy Temple", "N/A", "Tuni", 5.0, "N/A", "N/A", 0, "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", 5.0],
    ["Simhachalam", "Visakhapatnam", "Simhachalam Hill", 17.7667, 83.2500, "Sri Varaha Lakshmi Narasimha Swamy Temple", "N/A", "N/A", 5.0, "N/A", "N/A", 0, "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", 5.0],
    ["Mangalagiri", "Guntur", "Mangalagiri Hill", 16.4333, 80.5667, "Sri Panakala Lakshmi Narasimha Swamy Temple", "N/A", "Vijayawada", 5.0, "N/A", "N/A", 0, "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", 5.0],
    ["Tirupati", "Chittoor", "Tiruchanur", 13.6162, 79.4447, "Sri Padmavathi Ammavari Temple", "Tiruchanur Ruins", "Hotel Grand Ridge", 4.9, "Near Tiruchanur", "SR Prime", 4.7, "Main Road", "Tiffins", "Nearby", "Sri Sai Meals", "Main Road", "Hotel Grand Ridge", "Tiruchanur Police Station", "Main Road", 4.9],
    ["Tirupati", "Chittoor", "Kapila Theertham", 13.6517, 79.4183, "Sri Kapileswara Swamy Temple", "Natural Waterfalls", "Fortune Select", 4.9, "Kapila Theertham", "Flavours", 4.6, "Waterfall Road", "Tiffins", "Kapila Theertham Entrance", "Sudarshan", "Nearby", "Fortune Select", "Alipiri Police Station", "Alipiri Road", 4.9],
    ["Tirupati", "Chittoor", "Hare Krishna Nagar", 13.6500, 79.4300, "ISKCON Temple Tirupati", "Lotus Architecture", "Iskcon Guesthouse", 4.9, "Tirupati Outer Ring", "Lotus Restaurant", 4.9, "Iskcon Campus", "Iskcon Tiffins", "Main Entrance", "Iskcon Meals", "Inside Temple", "Iskcon Guesthouse", "Alipiri Police", "Alipiri", 4.9]
]

df_famous = pd.DataFrame(famous_places_list, columns=df_original.columns)

# Combine: Famous first, then ALL original rows
final_df = pd.concat([df_famous, df_original], ignore_index=True).drop_duplicates(subset=['Tourist_Place'], keep='first')

# 4. Final Formatting
for col in final_df.select_dtypes(include=['object']):
    final_df[col] = final_df[col].astype(str).str.strip()

# Save
final_df.to_csv(csv_path, index=False)

print(f"Successfully restored full dataset with {len(final_df)} rows.")
print(f"Fixed visibility for Vijayawada (NTR district) and Tirupati area.")
