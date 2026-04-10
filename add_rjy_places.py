import pandas as pd

# Data to append
data = [
    {'Tourist_Place': 'Kambala Park', 'City_Name': 'Rajahmundry', 'Area_Name': 'Kambalacheruvu', 'Rating': 4.6, 'Latitude': 17.0050, 'Longitude': 81.7800, 'Category': 'Park', 'District_Name': 'East Godavari'},
    {'Tourist_Place': 'Happy Street Glow Garden', 'City_Name': 'Rajahmundry', 'Area_Name': 'Morampudi', 'Rating': 4.5, 'Latitude': 17.0125, 'Longitude': 81.7850, 'Category': 'Park', 'District_Name': 'East Godavari'},
    {'Tourist_Place': 'Godavari Arch Bridge & Barrage', 'City_Name': 'Rajahmundry', 'Area_Name': 'Dowleswaram', 'Rating': 4.9, 'Latitude': 16.9826, 'Longitude': 81.8035, 'Category': 'View Point', 'District_Name': 'East Godavari'}
]

# Read existing csv
df = pd.read_csv('datasets/AP_DATASET.CSV')

# Determine if these already exist to prevent duplicates
existing_places = df['Tourist_Place'].tolist()
filtered_data = [row for row in data if row['Tourist_Place'] not in existing_places]

if filtered_data:
    # Create a DataFrame from the new data
    new_df = pd.DataFrame(filtered_data)

    # Fill missing columns in new_df with default values or NaN
    for col in df.columns:
        if col not in new_df.columns:
            new_df[col] = ''  # or whatever default is appropriate
            
    # Keep only columns that exist in the original DF
    new_df = new_df[df.columns]

    # Append and save
    final_df = pd.concat([df, new_df], ignore_index=True)
    final_df.to_csv('datasets/AP_DATASET.CSV', index=False)
    
    # Also overwrite upload.CSV to keep it in sync
    final_df.to_csv('datasets/upload.CSV', index=False)
    print(f"Added {len(filtered_data)} new places to AP_DATASET.CSV")
else:
    print("Places already exist in AP_DATASET.CSV")
