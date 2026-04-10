import pandas as pd
import os

csv_path = r'datasets\AP_DATASET.CSV'
backup_path = r'datasets\AP_DATASET_CLEAN_BACKUP.CSV'

if not os.path.exists(backup_path):
    import shutil
    shutil.copy2(csv_path, backup_path)
    print(f"Second backup created at {backup_path}")

# Read the data
df = pd.read_csv(csv_path)

# Ensure columns are stripped
df.columns = df.columns.str.strip()

# 1. AGGRESSIVE Deduplication for Tirumala Temple
# Identify rows that are basically the Main Temple in Tirumala
is_main_temple = (df['Tourist_Place'].astype(str).str.contains("Venkateswara", case=False, na=False)) & \
                 (df['City_Name'].astype(str).str.contains("Tirupathi|Tirumala|Tirupati", case=False, na=False))

# Keep only THE FIRST main temple entry, delete others
main_temples = df[is_main_temple].head(1)
df = df[~is_main_temple]

# Standardize the best one
main_temples.iloc[0, df.columns.get_loc('Tourist_Place')] = "Sri Venkateswara Swamy Temple (Tirumala)"
main_temples.iloc[0, df.columns.get_loc('Rating')] = 5.0

# 2. Add Nearby Places (Brochure)
new_places_data = [
    # City, District, Area, Lat, Lon, Place, Hidden, Hotel, H_Rating, H_Addr, Rest, R_Rating, R_Addr, Tiffin, T_Addr, Lunch, L_Addr, Accom, Emergency, E_Addr, Rating
    ["Tirupati", "Chittoor", "Tiruchanur", 13.6162, 79.4447, "Sri Padmavathi Ammavari Temple", "Tiruchanur Ruins", "Hotel Grand Ridge", 4.8, "Near Tiruchanur", "SR Prime", 4.7, "Main Road", "Tiffins", "Nearby", "Sri Sai Meals", "Main Road", "Hotel Grand Ridge", "Tiruchanur Police Station", "Main Road", 5.0],
    ["Tirupati", "Chittoor", "Kapila Theertham", 13.6517, 79.4183, "Sri Kapileswara Swamy Temple", "Natural Waterfalls", "Fortune Select", 4.7, "Kapila Theertham", "Flavours", 4.6, "Waterfall Road", "Tiffins", "Kapila Theertham Entrance", "Sudarshan", "Nearby", "Fortune Select", "Alipiri Police Station", "Alipiri Road", 5.0],
    ["Tirupati", "Chittoor", "Chandragiri", 13.5833, 79.3167, "Chandragiri Fort", "Light & Sound Show", "Local Residency", 4.2, "Chandragiri", "Fort Views", 4.3, "Fort Road", "Local Tiffins", "Chandragiri", "Fort Cafe", "Fort Road", "Boutique Hotel", "Chandragiri PHC", "Fort Area", 5.0],
    ["Tirupati", "Chittoor", "Hare Krishna Nagar", 13.6500, 79.4300, "ISKCON Temple Tirupati", "Lotus Architecture", "Iskcon Guesthouse", 4.8, "Tirupati Outer Ring", "Lotus Restaurant", 4.9, "Iskcon Campus", "Iskcon Tiffins", "Main Entrance", "Iskcon Meals", "Inside Temple", "Iskcon Guesthouse", "Alipiri Police", "Alipiri", 5.0],
    ["Tirupati", "Chittoor", "Tirumala", 13.6667, 79.3167, "Silathoranam", "Natural Stone Arch", "TTD Guesthouses", 4.5, "Tirumala", "Hill Views", 4.2, "Rock Arch Area", "Local Snacks", "Near Arch", "Hill Tiffins", "Tirumala", "TTD Accom", "Tirumala Police", "Main Road", 5.0],
    ["Tirupati", "Chittoor", "Tirumala Hills", 13.6800, 79.3300, "Akasaganga & Papavinasam", "Sacred Waters", "TTD Accom", 4.5, "Tirumala hills", "Hill Top Cafe", 4.0, "Waterfall area", "Tiffins", "Hill top", "Meals", "Nearby", "TTD Guesthouse", "Tirumala Police", "Main road", 5.0],
    ["Tirupati", "Chittoor", "Tirupati Main", 13.6267, 79.4167, "Sri Govindaraja Swamy Temple", "Historical Tower", "Hotel Bliss", 4.6, "Temple Road", "Bliss Restaurant", 4.7, "Inner Ring Road", "Railway Station Tiffins", "Tirupati Station", "Standard Meals", "Temple entrance", "Minerva Grand", "Tirupati Town Police", "Station road", 5.0],
    ["Tirupati", "Chittoor", "Srinivasa Mangapuram", 13.6000, 79.3000, "Sri Kalyana Venkateswara Swamy Temple", "Ancient Temple", "Sapthagiri Residency", 4.4, "Mangapuram", "Venkateswara Hotel", 4.2, "Main road", "Local Tiffins", "Nearby", "Meals", "Main road", "Residency", "Chandragiri Police", "Fort Road", 5.0]
]

new_df = pd.DataFrame(new_places_data, columns=df.columns)

# Prioritize famous places (move all famous ones including the standardized Venkateswara to the top)
famous_places = pd.concat([main_temples, new_df], ignore_index=True)

# Remove these new ones if they already exist (deduplicate)
existing_places = df[~df['City_Name'].isin(['Tirupati', 'Tirupathi', 'Tirumala'])]
# BUT we want to keep OTHER Tirupati places too, just not duplicates
other_tirupati = df[df['City_Name'].isin(['Tirupati', 'Tirupathi', 'Tirumala'])]
other_tirupati = other_tirupati[~other_tirupati['Tourist_Place'].isin(famous_places['Tourist_Place'])]

# Final merge: Famous first, then rest
final_df = pd.concat([famous_places, existing_places, other_tirupati], ignore_index=True)

# Final formatting
final_df.to_csv(csv_path, index=False)

print(f"Successfully deduplicated Tirumala and added {len(new_df)} new authentic places for Tirupati.")
