import pandas as pd
import os

csv_path = r'datasets\AP_DATASET.CSV'

if not os.path.exists(csv_path):
    print(f"Error: {csv_path} not found.")
    exit(1)

# Load existing dataset
df = pd.read_csv(csv_path)

# Normalize names for duplicate checking/matching
def get_clean_key(name):
    s = str(name).lower()
    return "".join(s.split())

# Iconic landmarks to BOOST/FIX with 5.0 rating
iconic_landmarks = [
    ["Visakhapatnam", "Visakhapatnam", "Beach Road", 17.7065, 83.2956, "RK Beach", "Iconic Vizag Beach & Promenade"],
    ["Visakhapatnam", "Visakhapatnam", "Beach Road", 17.7125, 83.3139, "INS Kurusura Submarine Museum", "Decommissioned Submarine Museum"],
    ["Visakhapatnam", "Visakhapatnam", "Beach Road", 17.7117, 83.3083, "VMRDA VUDA Park", "Musical Fountain & Urban Park"],
    ["Visakhapatnam", "Visakhapatnam", "Dairy Farm", 17.7667, 83.3, "Indira Gandhi Zoological Park", "Largest Zoo in AP"],
    ["Visakhapatnam", "Visakhapatnam", "Hilltop", 17.7583, 83.3729, "Kailasagiri Park", "Panoramic Hilltop View & Ropeway"],
    ["Visakhapatnam", "Visakhapatnam", "Beach Side", 17.6767, 83.2917, "Dolphin's Nose", "Iconic Hill Resembling Dolphin Nose"],
    ["Vijayawada", "NTR", "Krishna River", 16.5167, 80.6, "Prakasam Barrage", "Iconic Bridge Across Krishna River"],
    ["Vijayawada", "NTR", "Undavalli", 16.4917, 80.5833, "Undavalli Caves", "Monolithic Rock-Cut Temple Architecture"],
    ["Vijayawada", "NTR", "Krishna River", 16.5167, 80.6, "Bhavani Island", "Riverfront Island Resort"],
    ["Vijayawada", "NTR", "Kondapalli", 16.6333, 80.5333, "Kondapalli Fort", "Historical Fort & Toys Village"],
    ["Vijayawada", "NTR", "One Town", 16.5111, 80.6067, "Gandhi Hill", "First Gandhi Memorial in India"],
    ["Vijayawada", "NTR", "M G Road", 16.5167, 80.6167, "Bapu Museum (Victoria Museum)", "Ancient Artefacts & Sculpture Garden"],
    ["Rajahmundry", "East Godavari", "River Road", 17.0, 81.7667, "Godavari Arch Bridge", "Asia's Second Longest Arch Bridge"],
    ["Rajahmundry", "East Godavari", "River Cruise", 17.2, 81.3, "Papi Kondalu", "Scenic River Gorge & Boat Cruise"],
    ["Rajahmundry", "East Godavari", "Gouthami Ghat", 17.0, 81.8, "ISKCON Rajahmundry", "Spiritual & Cultural Center"],
    ["Kurnool", "Kurnool", "Panyam", 15.1, 78.1, "Belum Caves", "Largest & Longest Cave System in India"],
    ["Kurnool", "Kurnool", "Kurnool City", 15.8, 78.0, "Konda Reddy Fort", "Historical Medieval Fort Icon"],
    ["Kurnool", "Kurnool", "Orvakal", 15.6, 78.2, "Orvakal Rock Garden", "Unique Igneous Rock Formations"],
    ["Tirupati", "Tirupati", "Srikalahasti", 13.75, 79.7, "Sri Kalahasti Temple", "Ancient Vayu Lingam Temple"],
    ["Tirupati", "Tirupati", "Alipiri", 13.6517, 79.4183, "Kapila Theertham Waterfalls", "Sacred Waterfall & Temple"],
    ["Tirupati", "Tirupati", "Chandragiri", 13.5833, 79.3167, "Chandragiri Fort & Museum", "Vijayanagara Imperial Fort"],
]

# Ensure Entry_Fee column exists
if 'Entry_Fee' not in df.columns:
    df['Entry_Fee'] = "N/A"

new_rows = []
for spot in iconic_landmarks:
    city, district, area, lat, lon, name, desc = spot
    key = get_clean_key(name)
    
    # 1. Update existing matches
    mask = df['Tourist_Place'].str.contains(name, case=False, na=False)
    if df[mask].any().any():
        df.loc[mask, 'Rating'] = 5.0
        df.loc[mask, 'Final_Rating'] = 5.0
        df.loc[mask, 'Description'] = desc
        # Update entry fee for temples
        if any(k in name for k in ["Temple", "Mosque", "Church", "Dargah", "Devipuram", "ISKCON"]):
            df.loc[mask, 'Entry_Fee'] = "Free"
    else:
        # Create a new record using dict for alignment
        rating_val = 5.0
        fee = "Free" if any(k in name for k in ["Temple", "Mosque", "Church", "Dargah", "Devipuram", "ISKCON"]) else "Paid/NA"
        
        row_dict = {col: "N/A" for col in df.columns}
        row_dict.update({
            'City_Name': city, 'District_Name': district, 'Area_Name': area,
            'Latitude': lat, 'Longitude': lon, 'Tourist_Place': name,
            'Description': desc, 'Rating': rating_val, 'Final_Rating': rating_val,
            'Entry_Fee': fee, 'Hotel': "Nearby Hotel"
        })
        new_rows.append(row_dict)

if new_rows:
    new_df = pd.DataFrame(new_rows)
    df = pd.concat([df, new_df], ignore_index=True)

# Final cleanup: Standardize ratings (some had 11.2)
df['Rating'] = pd.to_numeric(df['Rating'], errors='coerce').fillna(4.0)
df['Final_Rating'] = pd.to_numeric(df['Final_Rating'], errors='coerce').fillna(4.0)
df.loc[df['Rating'] > 5.0, 'Rating'] = 5.0
df.loc[df['Final_Rating'] > 5.0, 'Final_Rating'] = 5.0

# Final Save
df.to_csv(csv_path, index=False)
print(f"Iconic Boost applied! Final row count: {len(df)}")
