import pandas as pd

data = [
    {
        'Tourist_Place': 'Ainavilli Godavari Ghat',
        'City_Name': 'Ainavilli',
        'Area_Name': 'Godavari Bank',
        'Rating': 4.7,
        'Latitude': 16.5900,
        'Longitude': 82.0100,
        'Category': 'River Side',
        'District_Name': 'Konaseema',
        'Nearby_Hotel_Name': 'Ainavilli Guest House',
        'Hotel_Rating': 4.5,
        'Restaurant_Name': 'Konaseema Ruchulu',
        'Tiffin_Center_Name': 'Local Tiffins'
    },
    {
        'Tourist_Place': 'Sri Uma Koppeswara Swamy Temple',
        'City_Name': 'Ainavilli',
        'Area_Name': 'Temple Street',
        'Rating': 4.8,
        'Latitude': 16.5850,
        'Longitude': 82.0050,
        'Category': 'Temple',
        'District_Name': 'Konaseema',
        'Nearby_Hotel_Name': 'Temple View Lodge',
        'Hotel_Rating': 4.2,
        'Restaurant_Name': 'Sri Sai Fast Food',
        'Tiffin_Center_Name': 'Temple Tiffins'
    },
    {
        'Tourist_Place': 'Ainavilli Coconut Plantations',
        'City_Name': 'Ainavilli',
        'Area_Name': 'Outskirts',
        'Rating': 4.6,
        'Latitude': 16.5700,
        'Longitude': 81.9900,
        'Category': 'Nature',
        'District_Name': 'Konaseema',
        'Nearby_Hotel_Name': 'Nature Homestay',
        'Hotel_Rating': 4.8,
        'Restaurant_Name': 'Village Dhaba',
        'Tiffin_Center_Name': 'Morning Tiffins'
    }
]

df = pd.read_csv('datasets/AP_DATASET.CSV')

existing_places = df['Tourist_Place'].tolist()
filtered_data = [row for row in data if row['Tourist_Place'] not in existing_places]

if filtered_data:
    new_df = pd.DataFrame(filtered_data)
    for col in df.columns:
        if col not in new_df.columns:
            new_df[col] = ''
    new_df = new_df[df.columns]
    
    final_df = pd.concat([df, new_df], ignore_index=True)
    final_df.to_csv('datasets/AP_DATASET.CSV', index=False)
    final_df.to_csv('datasets/upload.CSV', index=False)
    print(f"Added {len(filtered_data)} new places for Ainavilli")
else:
    print("Places already exist")
