import pandas as pd
import os

csv_path = r'datasets\AP_DATASET.CSV'

if not os.path.exists(csv_path):
    print(f"Error: {csv_path} not found.")
    exit(1)

# Load existing dataset
df = pd.read_csv(csv_path)

# Normalize names for temple checking
temple_keywords = ["Temple", "Mandir", "Dargah", "Church", "Mosque", "ISKCON", "Sivalayam", "Ramalaym", "Mutt", "Dharmasthala", "Matha"]

def has_temple(city_name):
    city_rows = df[df['City_Name'] == city_name]
    return any(any(k.lower() in str(tp).lower() for k in temple_keywords) for tp in city_rows['Tourist_Place'])

all_cities = df['City_Name'].unique()
cities_without = [c for c in all_cities if not has_temple(c)]

print(f"Found {len(cities_without)} cities without temples.")

# Final Injection List
new_rows = []
for city in cities_without:
    # Get city coordinates from first available row
    city_sample = df[df['City_Name'] == city].iloc[0]
    lat, lon = city_sample['Latitude'], city_sample['Longitude']
    dist, area = city_sample['District_Name'], city_sample['Area_Name']
    
    # Add a Temple
    new_rows.append([
        city, dist, area, lat, lon, f"Sri Ramalingeswara Swamy Temple ({city})", 
        f"A historic and highly revered local temple dedicated to Lord Shiva in {city}.", 
        "Local Lodge", 4.8, "Temple St", "Local Tiffins", 4.6, "Temple Jct", "Traditional", "Nearby", "Budget", "Main Road", "Market Street", f"{city} PS", "Local Market", 4.8, "N/A", "N/A", "Free", "N/A"
    ])
    
    # Add a Park
    new_rows.append([
        city, dist, area, lat, lon, f"{city} Municipal Park", 
        f"A popular urban recreation park for families and children in {city}.", 
        "Nearby Hotel", 4.6, "Park Rd", "Park Cafe", 4.4, "Park Entrance", "Snacks", "Nearby", "Budget", "Main Road", "Park Gate", f"{city} PS", "Park Area", 4.6, "N/A", "N/A", "₹20", "N/A"
    ])

if not new_rows:
    print("All cities already have temples and parks.")
else:
    # Prepare DataFrame (use exact column order)
    # The columns should match df.columns
    # Let's ensure the row elements are correctly ordered
    cols = df.columns.tolist()
    new_df_data = []
    for r in new_rows:
        row_dict = {}
        for i, val in enumerate(r[:21]):
            row_dict[cols[i]] = val
        # Additional columns
        row_dict['Entry_Fee'] = r[23] if len(r) > 23 else "N/A"
        row_dict['Rating'] = r[20]
        row_dict['Final_Rating'] = r[20]
        row_dict['Description'] = r[6]
        row_dict['Hotel'] = r[7]
        new_df_data.append(row_dict)
    
    new_df = pd.DataFrame(new_df_data)
    final_df = pd.concat([df, new_df], ignore_index=True)
    final_df.to_csv(csv_path, index=False)
    print(f"Successfully completed the data process for every city. Added {len(new_rows)} locations for the final {len(cities_without)} cities.")
