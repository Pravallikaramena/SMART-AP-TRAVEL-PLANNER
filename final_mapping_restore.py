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

# 2. MASSIVE MAPPING FOR SEARCH VISIBILITY
# This "unlocks" thousands of rows that were categorized by small town but searched by city name.

# Vijayawada (NTR District or Area contains Vijayawada)
mask_vj = (df_original['District_Name'].astype(str).str.contains("NTR", case=False, na=False)) | \
          (df_original['Area_Name'].astype(str).str.contains("Vijayawada", case=False, na=False))
df_original.loc[mask_vj, 'City_Name'] = "Vijayawada"

# Vizianagaram (Area contains Vizianagaram)
mask_viz = (df_original['Area_Name'].astype(str).str.contains("Vizianagaram", case=False, na=False))
df_original.loc[mask_viz, 'City_Name'] = "Vizianagaram"

# Tirupati (Chittoor/Tirupati District or Area contains Tirupati/Tirumala)
mask_tiru = (df_original['District_Name'].astype(str).str.contains("Chittoor|Tirupati", case=False, na=False)) | \
            (df_original['Area_Name'].astype(str).str.contains("Tirupati|Tirumala", case=False, na=False))
df_original.loc[mask_tiru, 'City_Name'] = "Tirupati"

print(f"Mapping complete. 'Vijayawada' now has {sum(mask_vj)} entries. 'Vizianagaram' now has {sum(mask_viz)} entries.")

# 3. New Tirupati Brochure Spots (Curated)
new_places = [
    ["Tirupati", "Chittoor", "Tirumala Hills", 13.6833, 79.4300, "Sri Venkateswara Swamy Temple (Tirumala)", "N/A", "Tirupati", 5.0, "N/A", "N/A", 0, "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", 5.0],
    ["Tirupati", "Chittoor", "Tiruchanur", 13.6162, 79.4447, "Sri Padmavathi Ammavari Temple", "Tiruchanur Ruins", "Hotel Grand Ridge", 4.9, "Near Tiruchanur", "SR Prime", 4.7, "Main Road", "Tiffins", "Nearby", "Sri Sai Meals", "Main Road", "Hotel Grand Ridge", "Tiruchanur Police Station", "Main Road", 4.9],
    ["Tirupati", "Chittoor", "Kapila Theertham", 13.6517, 79.4183, "Sri Kapileswara Swamy Temple", "Natural Waterfalls", "Fortune Select", 4.9, "Kapila Theertham", "Flavours", 4.6, "Waterfall Road", "Tiffins", "Kapila Theertham Entrance", "Sudarshan", "Nearby", "Fortune Select", "Alipiri Police Station", "Alipiri Road", 4.9],
    ["Tirupati", "Chittoor", "Chandragiri", 13.5833, 79.3167, "Chandragiri Fort", "Light & Sound Show", "Local Residency", 4.9, "Chandragiri", "Fort Views", 4.3, "Fort Road", "Local Tiffins", "Chandragiri", "Fort Cafe", "Fort Road", "Boutique Hotel", "Chandragiri PHC", "Fort Area", 4.9],
    ["Tirupati", "Chittoor", "Hare Krishna Nagar", 13.6500, 79.4300, "ISKCON Temple Tirupati", "Lotus Architecture", "Iskcon Guesthouse", 4.9, "Tirupati Outer Ring", "Lotus Restaurant", 4.9, "Iskcon Campus", "Iskcon Tiffins", "Main Entrance", "Iskcon Meals", "Inside Temple", "Iskcon Guesthouse", "Alipiri Police", "Alipiri", 4.9],
    ["Tirupati", "Chittoor", "Tirumala", 13.6667, 79.3167, "Silathoranam", "Natural Stone Arch", "TTD Guesthouses", 4.9, "Tirumala", "Hill Views", 4.2, "Rock Arch Area", "Local Snacks", "Near Arch", "Hill Tiffins", "Tirumala", "TTD Accom", "Tirumala Police", "Main Road", 4.9],
    ["Tirupati", "Chittoor", "Tirumala Hills", 13.6800, 79.3300, "Akasaganga & Papavinasam", "Sacred Waters", "TTD Accom", 4.9, "Tirumala hills", "Hill Top Cafe", 4.0, "Waterfall area", "Tiffins", "Hill top", "Meals", "Nearby", "TTD Guesthouse", "Tirumala Police", "Main road", 4.9],
    ["Tirupati", "Chittoor", "Tirupati Main", 13.6267, 79.4167, "Sri Govindaraja Swamy Temple", "Historical Tower", "Hotel Bliss", 4.9, "Temple Road", "Bliss Restaurant", 4.7, "Inner Ring Road", "Railway Station Tiffins", "Tirupati Station", "Standard Meals", "Temple entrance", "Minerva Grand", "Tirupati Town Police", "Station road", 4.9],
    ["Tirupati", "Chittoor", "Srinivasa Mangapuram", 13.6000, 79.3000, "Sri Kalyana Venkateswara Swamy Temple", "Ancient Temple", "Sapthagiri Residency", 4.9, "Mangapuram", "Venkateswara Hotel", 4.2, "Main road", "Local Tiffins", "Nearby", "Meals", "Main road", "Residency", "Chandragiri Police", "Fort Road", 4.9]
]

df_new = pd.DataFrame(new_places, columns=df_original.columns)

# 4. Final Combine: New spots + All mapped original spots
# (We don't deduplicate here except for exactly matching names of our new spots)
new_names = df_new['Tourist_Place'].tolist()
df_original_clean = df_original[~df_original['Tourist_Place'].astype(str).str.strip().isin(new_names)]

final_df = pd.concat([df_new, df_original_clean], ignore_index=True)

# 5. Clean strings
for col in final_df.select_dtypes(include=['object']):
    final_df[col] = final_df[col].astype(str).str.strip()

# Save
final_df.to_csv(csv_path, index=False)

print(f"Successfully restored and fixed mapping. Final row count: {len(final_df)}.")
