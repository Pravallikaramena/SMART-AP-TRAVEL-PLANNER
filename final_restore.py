import pandas as pd
import os

source_csv = r'datasets\upload.CSV'
target_csv = r'datasets\AP_DATASET.CSV'

if not os.path.exists(source_csv):
    print(f"Error: {source_csv} not found.")
    exit(1)

# Load the original 6,874-row dataset
print("Loading original clean dataset...")
try:
    df = pd.read_csv(source_csv)
    # Strip whitespace from column names just in case
    df.columns = df.columns.str.strip()
    print(f"Loaded {len(df)} rows from {source_csv}")
except Exception as e:
    print(f"Failed to load source CSV: {e}")
    exit(1)

# New Tirupati Brochure Spots
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

# Create a DataFrame for new spots (only columns that also exist in df)
df_new = pd.DataFrame(new_places, columns=df.columns)

# We want to remove any old spots that exactly match the names of our new high-priority spots to avoid "Double Vision"
new_spot_names = df_new['Tourist_Place'].str.lower().str.strip()
df = df[~df['Tourist_Place'].astype(str).str.lower().str.strip().isin(new_spot_names)]

# Combine our new data (at top) with the original 6000+ rows
final_df = pd.concat([df_new, df], ignore_index=True)

# Important Map Fix for Search Visibility:
# Update City_Name to "Vijayawada" where District is NTR, to unlock Vijayawada results
mask_vj = (final_df['District_Name'].astype(str).str.contains("NTR", case=False, na=False)) | (final_df['Area_Name'].astype(str).str.contains("Vijayawada", case=False, na=False))
final_df.loc[mask_vj, 'City_Name'] = "Vijayawada"

# Do same for Vizianagaram
mask_vz = (final_df['Area_Name'].astype(str).str.contains("Vizianagaram", case=False, na=False))
final_df.loc[mask_vz, 'City_Name'] = "Vizianagaram"

# Do same for Tirupati (mapped from Chittoor)
mask_tr = (final_df['District_Name'].astype(str).str.contains("Chittoor|Tirupati", case=False, na=False)) | (final_df['Area_Name'].astype(str).str.contains("Tirupati|Tirumala", case=False, na=False))
final_df.loc[mask_tr, 'City_Name'] = "Tirupati"

# Clean all string columns (removes trailing tabs/spaces that can mess up headers)
for col in final_df.select_dtypes(include=['object']):
    final_df[col] = final_df[col].astype(str).str.strip()

print(f"Data combined and normalized. Saving exactly {len(final_df)} rows to target CSV.")

# Force comma separation explicitly
final_df.to_csv(target_csv, index=False, sep=',')
print("Done! The dataset is ready with comma (,) delimiter.")
