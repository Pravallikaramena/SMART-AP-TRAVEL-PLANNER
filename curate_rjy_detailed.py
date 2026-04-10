import pandas as pd
import os

csv_path = r'datasets\AP_DATASET.CSV'

if not os.path.exists(csv_path):
    print(f"Error: {csv_path} not found.")
    exit(1)

# Load existing dataset
df = pd.read_csv(csv_path)

# 1. Clean existing Rajahmundry entries (Remove 'nan')
rjy_mask = df['City_Name'] == 'Rajahmundry'
# Update the 6 existing ones with professional details instead of 'nan'
df.loc[rjy_mask, 'Nearby_Hotel_Name'] = 'Rive Bay Resort'
df.loc[rjy_mask, 'Hotel_Rating'] = 4.8
df.loc[rjy_mask, 'Restaurant_Name'] = 'River View Restaurant'
df.loc[rjy_mask, 'Tiffin_Center_Name'] = 'Sangeetha Tiffins'
df.loc[rjy_mask, 'Emergency_Service'] = 'Rajahmundry Police'
df.loc[rjy_mask, 'Emergency_Address'] = 'Town Police Station, RJY'
df.loc[rjy_mask, 'Hotel'] = 'Grand Palace'

# 2. Detailed Iconic Landmarks for Rajahmundry (12+ new ones)
rjy_curated = [
    ["Rajahmundry", "East Godavari", "River Road", 16.9942, 81.7647, "Godavari Arch Bridge", "Asia's Second Longest Arch Bridge - Iconic Landmark", "Rive Bay", 5.0],
    ["Rajahmundry", "East Godavari", "River Road", 17.0011, 81.7628, "Havelock Bridge (Old Godavari Bridge)", "Historical 1900s Rail Bridge - Pedestrian Heritage", "Hotel Anand", 4.9],
    ["Rajahmundry", "East Godavari", "Godavari Banks", 16.9904, 81.7821, "Pushkar Ghat", "Sacred Riverfront for Godavari Aarti & Pavitra Snanam", "Shelton Rajamahendri", 5.0],
    ["Rajahmundry", "East Godavari", "Old Town", 16.9922, 81.7767, "Markandeya Swamy Temple", "Ancient Shiva Temple with Stunning Architecture", "Manjeera Sarovar", 4.8],
    ["Rajahmundry", "East Godavari", "Town Center", 16.9933, 81.7711, "Kotilingeswara Swamy Temple", "Famous Temple with Thousands of Shivalingas", "River Bay", 4.8],
    ["Rajahmundry", "East Godavari", "Dowleswarm", 16.9400, 81.7822, "Cotton Museum & Dowleswaram Barrage", "Historical Museum documenting the Irrigation Wonder", "Rive Bay", 5.0],
    ["Rajahmundry", "East Godavari", "Gouthami Ghat", 17.0000, 81.8000, "Rajahmundry Cultural Center", "Hub of Arts, Crafts & Cultural Activities", "Hotel Anand", 4.7],
    ["Rajahmundry", "East Godavari", "Dowleswarm", 16.9422, 81.7811, "Dhavaleswaram Anicut", "Iconic Dam built by Sir Arthur Cotton", "Shelton Hotel", 4.9],
    ["Rajahmundry", "East Godavari", "Town Center", 16.9967, 81.7744, "Rallabandi Subbarao Govt Museum", "Ancient Artifacts, Coins & Palm Leaf Manuscripts", "Sangeetha Hotel", 4.7],
    ["Rajahmundry", "East Godavari", "Outskirts", 16.9444, 81.8333, "Kadiyapulanka Nurseries", "Asia's Largest Flower & Plant Nursery Hub", "Haritha Resorts", 4.9],
    ["Rajahmundry", "East Godavari", "G Jayaraju Park", 16.9989, 81.7721, "G Jayaraju Park", "Beautifully Manicured Park on Godavari Banks", "Town Hotel", 4.7],
    ["Rajahmundry", "East Godavari", "Outskirts", 17.0011, 81.7725, "Kotipalli Ghat", "Serene River Point for Boating & Sunsets", "Haritha", 4.8],
    ["Rajahmundry", "East Godavari", "City Center", 16.9925, 81.7788, "Vemana Mandiram", "Historical Library and Literary Center", "Local Residency", 4.6],
    ["Rajahmundry", "East Godavari", "Main Town", 16.9911, 81.7744, "Syed Shah Baji Aulia Dargah", "Famous Spiritual Sufi Shrine", "Hotel Anand", 4.8],
]

# 3. Safe Injection of new spots
new_rows = []
for spot in rjy_curated:
    city, district, area, lat, lon, name, desc, hotel_name, rating = spot
    
    # Check if this place already exists (fuzzy matching)
    mask = df['Tourist_Place'].str.contains(name.split('(')[0].strip(), case=False, na=False)
    if not df[mask].any().any():
        row_dict = {col: 'N/A' for col in df.columns}
        row_dict.update({
            'City_Name': city, 'District_Name': district, 'Area_Name': area,
            'Latitude': lat, 'Longitude': lon, 'Tourist_Place': name,
            'Description': desc, 'Rating': rating, 'Final_Rating': rating,
            'Nearby_Hotel_Name': hotel_name, 'Hotel_Rating': 4.8,
            'Restaurant_Name': 'River Bay Restaurant', 'Restaurant_Rating': 4.5,
            'Tiffin_Center_Name': 'Sangeetha Grand', 'Emergency_Service': 'Rajahmundry Police',
            'Hotel': hotel_name, 'Entry_Fee': 'Free' if any(k in name for k in ['Temple', 'Dargah', 'Ghat']) else 'Paid/NA'
        })
        new_rows.append(row_dict)

if new_rows:
    new_df = pd.DataFrame(new_rows)
    df = pd.concat([df, new_df], ignore_index=True)

# Final Standardization
df['Rating'] = pd.to_numeric(df['Rating'], errors='coerce').fillna(4.0)
df['Final_Rating'] = pd.to_numeric(df['Final_Rating'], errors='coerce').fillna(4.0)
df.loc[df['Rating'] > 5.0, 'Rating'] = 5.0
df.loc[df['Final_Rating'] > 5.0, 'Final_Rating'] = 5.0

# Ensure 'Entry_Fee' column is healthy and apply globally to new curated
rel_keywords = ["Temple", "Mosque", "Church", "Dargah", "Ghat", "ISKCON"]
for kw in rel_keywords:
    df.loc[df['Tourist_Place'].str.contains(kw, case=False, na=False), 'Entry_Fee'] = 'Free'

# Final Save
df.to_csv(csv_path, index=False)
print(f"Rajahmundry Expansion Applied! Total Rows for Rajahmundry: {len(df[df['City_Name'] == 'Rajahmundry'])}")
print(f"Global total row count: {len(df)}")
