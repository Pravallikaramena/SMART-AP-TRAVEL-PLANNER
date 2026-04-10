import pandas as pd
import os

csv_path = 'datasets/AP_DATASET.CSV'
df = pd.read_csv(csv_path)

# Second batch of authentic landmarks
batch2_landmarks = [
    # Srikakulam
    ['Srikakulam', 'Srikakulam', 'Arasavalli', 18.2917, 83.9100, 'Arasavalli Sun Temple', 'Sun Ray Point', 'Hotel Nagavali', 4.3, 'Srikakulam City', 'Srikakulam Mess', 4.2, 'Main Road', 'Teja Tiffins', 'Srikakulam', 'Local Meals', 'Town', 'Lodge Stay', 'Srikakulam Hospital', 'Town', 4.8, 'Ancient Sun temple where rays hit the deity twice a year.', 4.8, 'Free', 'Nagavali'],
    ['Srikakulam', 'Srikakulam', 'Srikurmam', 18.2725, 83.9904, 'Srikurmam Temple', 'Turtle Conservation', 'Residency Lodge', 4.0, 'Kurmam Road', 'Temple Canteen', 4.1, 'Temple Lane', 'Local Snacks', 'Kurmam', 'Annadana Satram', 'Temple', 'Lodge Stay', 'Temple Security', 'Kurmam', 4.7, 'Only temple in the world dedicated to Kurma avatar of Vishnu.', 4.7, 'Free', 'Residency'],
    
    # Vizianagaram
    ['Vizianagaram', 'Vizianagaram', 'Korukonda', 18.1158, 83.4158, 'Ramanarayanam', 'Theme Park', 'Hotel Mayuri', 4.2, 'Vizianagaram Bypass', 'Local Restaurant', 4.0, 'Main Road', 'Vizag Tiffins', 'Vizianagaram', 'Annapurna Meals', 'Vizianagaram', 'City Stay', 'Police Station', 'Vizianagaram', 4.7, 'Stunning bow-shaped Rama temple complex with theme park.', 4.7, 'Rs. 20', 'Mayuri'],
    ['Vizianagaram', 'Vizianagaram', 'Vizianagaram Fort', 18.1100, 83.4100, 'Vizianagaram Fort', 'Historical Artifacts', 'Grand Residency', 4.1, 'Fort Road', 'Bobbili Mess', 4.3, 'Fort Area', 'Local Tiffins', 'Fort', 'Munnuru Meals', 'Vizianagaram', 'Fort Stay', 'City Police', 'Vizianagaram', 4.5, 'Historic fort of the Rajas of Vizianagaram built in 1713.', 4.5, 'Free', 'Grand Residency'],
    
    # Srikalahasti
    ['Srikalahasti', 'Tirupati', 'Temple Road', 13.7500, 79.7000, 'Srikalahasteeswara Temple', 'Patala Ganapathi', 'Hotel MGM Grand', 4.5, 'Srikalahasti Central', 'Srikalahasti Mess', 4.4, 'Temple Road', 'Local Tiffin', 'Srikalahasti', 'Annadana Satram', 'Temple', 'MGM Grand Stay', 'Srikalahasti Hospital', 'Town', 4.9, 'One of the Pancha Bhoota Sthalams (Vayu Linga).', 4.9, 'Free', 'MGM Grand'],
    
    # Ahobilam
    ['Ahobilam', 'Nandyal', 'Nallamala hills', 15.1333, 78.7167, 'Ahobilam Temple Complex', 'Nava Narasimha', 'Haritha Ahobilam', 4.0, 'Ahobilam', 'Local Canteen', 3.8, 'Ahobilam', 'Snacks Hub', 'Ahobilam', 'Temple Meals', 'Ahobilam', 'Haritha Stay', 'Forest Security', 'Ahobilam', 4.8, 'Major pilgrimage site with nine Narasimha temples.', 4.8, 'Free', 'Haritha'],
    
    # Ongole
    ['Ongole', 'Prakasam', 'Kothapatnam Beach', 15.4333, 80.1667, 'Kothapatnam Beach', 'Sea View Point', 'Hotel Galaxy', 4.1, 'Ongole Road', 'Beachfront Resto', 3.9, 'Beach Road', 'Tiffin Center', 'Ongole', 'Local Meals', 'Ongole', 'Galaxy Stay', 'Ongole Hospital', 'Town', 4.6, 'Quiet and serene beach known for its clear waters.', 4.6, 'Free', 'Galaxy'],
    
    # Madanapalle
    ['Madanapalle', 'Annamayya', 'Horsley Hills', 13.6514, 78.4114, 'Horsley Hills', 'View Point', 'Haritha Horsley Hills', 4.2, 'Hilltop', 'Hilltop Restaurant', 4.0, 'Hilltop', 'Local Tiffin', 'Hilltop', 'Haritha Meals', 'Hilltop', 'Haritha Stay', 'Hill Security', 'Hilltop', 4.7, 'The "Ooty of Andhra Pradesh", a scenic hill station.', 4.7, 'Rs. 20', 'Haritha'],
    
    # Guntur (Amaravati)
    ['Guntur', 'Guntur', 'Amaravati', 16.5750, 80.3583, 'Amaravati Buddhist Stupa', 'Museum', 'Hotel Grand Amaravati', 4.1, 'Amaravati Road', 'Local Canteen', 4.0, 'Amaravati', 'Local Tiffins', 'Guntur', 'Meals Point', 'Guntur', 'Amaravati Stay', 'Guntur Police', 'Guntur', 4.7, 'Massive ancient Buddhist stupa built in the 2nd century BCE.', 4.7, 'Rs. 25', 'Grand Amaravati'],
    
    # More Visakhapatnam
    ['Visakhapatnam', 'Visakhapatnam', 'Yarada', 17.6583, 83.2778, 'Yarada Beach', 'Hill Side Point', 'Local Guest House', 3.8, 'Yarada Road', 'Beach Snacks', 3.7, 'Yarada Beach', 'Tiffin Center', 'Yarada', 'Beach Side Meals', 'Yarada', 'Beach House Stay', 'Coast Guard', 'Near Yarada', 4.7, 'Secluded beach surrounded by green hills.', 4.7, 'Free', 'Yarada Guest'],
    ['Visakhapatnam', 'Visakhapatnam', 'Tenneti Park', 17.7400, 83.3500, 'Tenneti Park', 'Shipwreck View', 'The Gateway Hotel', 4.7, 'Beach Road', 'Bamboo Bay', 4.4, 'Hotel Area', 'Local Snacks', 'Park Street', 'Cafe Coffee Day', 'Beach Road', 'Luxury Stay', 'Police Station', 'Beach Road', 4.6, 'Beautiful park overlooking the sea with a famous shipwreck.', 4.6, 'Free', 'Gateway'],
    
    # More Vijayawada
    ['Vijayawada', 'NTR', 'Moghalrajapuram', 16.5050, 80.6400, 'Moghalrajapuram Caves', 'Ancient Architecture', 'Hotel Fortune Murali', 4.6, 'Vijayawada Central', 'DV Manor', 4.5, 'MG Road', 'Baberchi', 'Vijayawada', 'Manor Dining', 'MG Road', 'Executive Stay', 'General Hospital', 'Vijayawada', 4.5, 'Ancient caves featuring a stunning statue of Nataraja.', 4.5, 'Rs. 10', 'Fortune Murali']
]

headers = df.columns.tolist()
b2_df = pd.DataFrame(batch2_landmarks, columns=headers)

# Combine and save
combined_df = pd.concat([df, b2_df], ignore_index=True)
combined_df = combined_df.drop_duplicates(subset=['City_Name', 'Tourist_Place'], keep='last')
combined_df.to_csv(csv_path, index=False)

print(f"Successfully added {len(batch2_landmarks)} more authentic landmarks.")
print(f"Grand Total entries: {len(combined_df)}")
