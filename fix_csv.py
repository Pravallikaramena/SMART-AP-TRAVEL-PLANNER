import pandas as pd
import os

csv_path = r'datasets\AP_DATASET.CSV'
source_csv = r'datasets\upload.CSV'

# Load the source data
df = pd.read_csv(source_csv, sep=None, engine='python', encoding='utf-8-sig')
df.columns = df.columns.str.strip()
for col in df.select_dtypes(include=['object']):
    df[col] = df[col].astype(str).str.strip()

print(f"Loaded {len(df)} rows.")

# ==========================================================
# 1. Broad City Mapping ( Krishna -> Vijayawada etc.)
# ==========================================================
DISTRICT_TO_CITY = {
    'Krishna': 'Vijayawada', 'NTR': 'Vijayawada',
    'East Godavari': 'Rajahmundry', 'West Godavari': 'Eluru',
    'Chittoor': 'Tirupati', 'Tirupati': 'Tirupati',
    'Visakhapatnam': 'Visakhapatnam', 'Anakapalli': 'Visakhapatnam',
    'Vizianagaram': 'Vizianagaram'
}

def map_city(row):
    d = str(row['District_Name']).strip()
    return DISTRICT_TO_CITY.get(d, row['City_Name'])

df['City_Name'] = df.apply(map_city, axis=1)

# ==========================================================
# 2. Add New High-Quality Spots (With Canonical Names)
# ==========================================================
# Re-adding them at the top with standardized names we want to keep
new_spots = [
    ["Vijayawada", "Krishna", "Indrakeeladri", 16.5111, 80.6067, "Sri Kanaka Durga Temple", "Famous Temple", "Hotel Ilapuram", 5.0, "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", 5.0],
    ["Tirupati", "Chittoor", "Tirumala", 13.6833, 79.4300, "Sri Venkateswara Swamy Temple (Tirumala)", "N/A", "Tirupati", 5.0, "N/A", "N/A", 0, "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", 5.0],
    ["Visakhapatnam", "Visakhapatnam", "Simhachalam Hill", 17.7667, 83.25, "Sri Varaha Lakshmi Narasimha Swamy Temple", "Sacred Hill Temple", "Novotel Visakhapatnam", 5.0, "Simhachalam", "Tiffins", 4.5, "Simhachalam", "Tiffins", "Simhachalam", "Meals", "Simhachalam", "Novotel", "Simhachalam PS", "Main Road", 5.0],
]
# ... and other brochure spots from previous turn ...
extra_brochures = [
    ["Tirupati", "Chittoor", "Tiruchanur", 13.6162, 79.4447, "Sri Padmavathi Ammavari Temple", "Tiruchanur Ruins", "Hotel Grand Ridge", 4.9, "Near Tiruchanur", "SR Prime", 4.7, "Main Road", "Tiffins", "Nearby", "Sri Sai Meals", "Main Road", "Hotel Grand Ridge", "Tiruchanur Police Station", "Main Road", 4.9],
    ["Tirupati", "Chittoor", "Kapila Theertham", 13.6517, 79.4183, "Sri Kapileswara Swamy Temple", "Natural Waterfalls", "Fortune Select", 4.9, "Kapila Theertham", "Flavours", 4.6, "Waterfall Road", "Tiffins", "Kapila Theertham Entrance", "Sudarshan", "Nearby", "Fortune Select", "Alipiri Police Station", "Alipiri Road", 4.9],
    ["Tirupati", "Chittoor", "Chandragiri", 13.5833, 79.3167, "Chandragiri Fort", "Light & Sound Show", "Local Residency", 4.9, "Chandragiri", "Fort Views", 4.3, "Fort Road", "Local Tiffins", "Chandragiri", "Fort Cafe", "Fort Road", "Boutique Hotel", "Chandragiri PHC", "Fort Area", 4.9],
    ["Tirupati", "Chittoor", "Hare Krishna Nagar", 13.6500, 79.4300, "ISKCON Temple Tirupati", "Lotus Architecture", "Iskcon Guesthouse", 4.9, "Tirupati Outer Ring", "Lotus Restaurant", 4.9, "Iskcon Campus", "Iskcon Tiffins", "Main Entrance", "Iskcon Meals", "Inside Temple", "Iskcon Guesthouse", "Alipiri Police", "Alipiri", 4.9],
    ["Tirupati", "Chittoor", "Tirupati Main", 13.6267, 79.4167, "Sri Govindaraja Swamy Temple", "Historical Tower", "Hotel Bliss", 4.9, "Temple Road", "Bliss Restaurant", 4.7, "Inner Ring Road", "Railway Station Tiffins", "Tirupati Station", "Standard Meals", "Temple entrance", "Minerva Grand", "Tirupati Town Police", "Station road", 4.9],
    ["Visakhapatnam", "Visakhapatnam", "Beach Road", 17.7065, 83.2956, "RK Beach & Submarine Museum", "Iconic Beach", "Hotel Pearl", 4.8, "Beach Road", "Coastal Kitchen", 4.6, "Beach Road", "Local Tiffins", "Beach Road", "Seafood", "Beach Road", "Hotel Pearl", "Beach Road PS", "Beach Road", 4.8],
    ["Visakhapatnam", "Visakhapatnam", "Kailasagiri", 17.7583, 83.3729, "Kailasagiri Park", "Hilltop Park & Ropeway", "Green Park Hotel", 4.7, "Kailasagiri", "Hill Cafe", 4.3, "Kailasagiri Road", "Tiffins", "Park Entrance", "Snacks", "Kailasagiri", "Green Park", "Rushikonda PS", "Main Road", 4.7],
]

df_new = pd.DataFrame(new_spots + extra_brochures, columns=df.columns)

# ==========================================================
# 3. Intelligent De-Duplication (Merging Sri vs Non-Sri)
# ==========================================================
# We merge the datasets FIRST
final_df = pd.concat([df_new, df], ignore_index=True)

# For De-duplication, we create a normalized key:
# Remove "Sri", "Temple", extra spaces, lowercase
def get_clean_key(name):
    s = str(name).lower()
    if "simhachalam" in s or "varaha lakshmi narasimha" in s:
        return "simhachalam_temple"
    s = s.replace("sri", "").replace("temple", "").replace("swamy", "").replace("(", "").replace(")", "")
    return "".join(s.split())

final_df['norm_key'] = final_df['Tourist_Place'].apply(get_clean_key)

# Drop duplicates based on City_Name and Normalized Key
# Keep the first one (which will be OUR manual high-quality entry)
final_df = final_df.drop_duplicates(subset=['City_Name', 'norm_key'], keep='first')

# Delete our temporary key
final_df = final_df.drop(columns=['norm_key'])

# Final Save
final_df.to_csv(csv_path, index=False)
print(f"Final dataset ready with {len(final_df)} rows. Duplicates merged.")
