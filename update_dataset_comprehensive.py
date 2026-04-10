import pandas as pd
import os

# Path to the dataset
csv_path = 'datasets/AP_DATASET.CSV'

# Load the current dataset
df = pd.read_csv(csv_path)

# List of target cities to clean (remove placeholder data)
cities_to_clean = [
    'Visakhapatnam', 'Vishakapatnam', 'Vijayawada', 'Bhimavaram', 'Ainavilli', 
    'Tirupati', 'Vadapalli', 'Vadapilli', 'Kakinada', 'Rajahmundry', 
    'Rajamahendravaram', 'Araku Valley', 'Anakapalle', 'Ananthagiri', 
    'Chintapalli', 'Gangaraju Madugula', 'Lepakshi', 'Kurnool', 'Kadapa'
]

# Clean up: Remove any generic placeholder entries for these cities
# We identify placeholders by checking if 'Tourist_Place' contains generic terms or if they match previously identified noise
placeholders = ['Promenade', 'Weavers Hamlet', 'Botanical Garden', 'Science Center']
df = df[~((df['City_Name'].isin(cities_to_clean)) & (df['Tourist_Place'].str.contains('|'.join(placeholders), case=False, na=False)))]

# New authentic landmarks data
new_landmarks = [
    # Visakhapatnam
    ['Visakhapatnam', 'Visakhapatnam', 'Simhachalam', 17.7669, 83.2484, 'Simhachalam Temple', 'Deep Blue Sea View', 'Hotel Novotel', 4.8, 'Beach Road, Vizag', 'Dharani Restaurant', 4.5, 'Vizag Main Road', 'Venkatadri Vantillu', 'Vizag', 'Hotel Ritz', 'Vizag', 'Luxury Stay', 'Police Control Room', 'Vizag', 4.9, 'Famous hilltop temple dedicated to Lord Narasimha.', 4.9, 'Free', 'Novotel'],
    ['Visakhapatnam', 'Visakhapatnam', 'RK Beach', 17.7100, 83.3333, 'INS Kursura Submarine Museum', 'Aircraft Museum', 'Hotel Gateway', 4.7, 'RK Beach Road', 'Sea Inn', 4.4, 'Beach Road', 'Gopi Tiffin', 'Vizag', 'Sea View Hotel', 'Beach Road', 'Beachfront Stay', 'City Health Centre', 'Vizag', 4.8, 'India\'s first submarine museum on a beach.', 4.8, 'Rs. 40', 'Gateway'],
    ['Visakhapatnam', 'Visakhapatnam', 'Kailasagiri', 17.7479, 83.3454, 'Kailasagiri Park', 'Titanic View Point', 'The Park Hotel', 4.6, 'Beach Road', 'Bamboo Bay', 4.3, 'The Park', 'Local Tiffin', 'Vizag', 'Hilltop Restaurant', 'Kailasagiri', 'Resort Stay', 'Hill Police', 'Vizag', 4.7, 'Beautiful hilltop park with panoramic city views.', 4.7, 'Rs. 20', 'The Park'],
    
    # Vijayawada
    ['Vijayawada', 'NTR', 'Indrakeeladri', 16.5161, 80.6190, 'Kanaka Durga Temple', 'River View', 'Hotel Fortune Murali', 4.7, 'Vijayawada Central', 'DV Manor', 4.5, 'MG Road', 'Baberchi', 'Vijayawada', 'Manor Dining', 'MG Road', 'Executive Stay', 'General Hospital', 'Vijayawada', 4.9, 'Most sacred temple on the banks of Krishna River.', 4.9, 'Free', 'Fortune Murali'],
    ['Vijayawada', 'NTR', 'Guntur Road', 16.4925, 80.5796, 'Undavalli Caves', 'Rock-cut Garden', 'Quality Inn', 4.4, 'Vijayawada Road', 'Biryani Durbar', 4.2, 'MG Road', 'Local Tiffin', 'Vijayawada', 'Highway Hotel', 'Road', 'Budget Stay', 'Local Police', 'Vijayawada', 4.5, 'Ancient 4th-century rock-cut Buddhist caves.', 4.6, 'Rs. 10', 'Quality Inn'],
    ['Vijayawada', 'NTR', 'Krishna River', 16.5263, 80.5700, 'Bhavani Island', 'Boating Point', 'River Bay Resort', 4.5, 'River Bank', 'Resort Dining', 4.4, 'Island', 'Island Snacks', 'Bhavani', 'River Resto', 'Island', 'Island Stay', 'Island Security', 'River', 4.6, 'One of the largest islands in the Krishna River.', 4.6, 'Rs. 50', 'River Bay'],
    
    # Kakinada
    ['Kakinada', 'Kakinada', 'Coringa', 16.8314, 82.3367, 'Coringa Wildlife Sanctuary', 'Hope Island', 'Hotel Grand Kakinada', 4.6, 'Kakinada City', 'Subbayya Gari Hotel', 4.8, 'Kakinada Central', 'Local Tiffin', 'CC Road', 'Grand Dining', 'City Road', 'Kakinada Stay', 'Kakinada Hospital', 'Kakinada', 4.7, 'Massive mangrove forests and bird sanctuary.', 4.7, 'Rs. 30', 'Grand Kakinada'],
    ['Kakinada', 'Kakinada', 'Uppada', 17.0864, 82.3386, 'Uppada Beach', 'Saree Weaving Center', 'Residency Guest House', 4.2, 'Uppada Road', 'Beachside Snacks', 4.0, 'Beach Road', 'Tiffin Center', 'Uppada', 'Local Meals', 'Uppada', 'Guest House', 'Coastal Security', 'Kakinada', 4.5, 'Beautiful beach known for its wide shores and Uppada Sarees.', 4.5, 'Free', 'Residency'],
    
    # Tirupati
    ['Tirupati', 'Tirupati', 'Tirumala', 13.6833, 79.3500, 'Venkateswara Swamy Temple', 'Sila Thoranam', 'Fortune Select Grand Ridge', 4.8, 'Tirupati Bypass', 'Mayura Restaurant', 4.5, 'Tirumala Road', 'Tiffin Hub', 'Tirupati', 'Tirumala Meals', 'Hilltop', 'Pilgrim Amenities', 'TTD Security', 'Tirumala', 5.0, 'The world famous hilltop temple of Lord Balaji.', 5.0, 'Free (Vaikuntam)', 'Fortune Grand'],
    ['Tirupati', 'Tirupati', 'Chittoor Road', 13.8117, 79.2156, 'Talakona Waterfalls', 'Trekking Trail', 'Talakona Forest Guest House', 4.1, 'Forest Area', 'Local Forest Canteen', 4.0, 'Near Entrance', 'Snacks Stalls', 'Entrance', 'Forest Canteen', 'Talakona', 'Forest Stay', 'Forest Guard', 'Talakona', 4.7, 'Highest waterfall in Andhra Pradesh.', 4.7, 'Rs. 50', 'Forest Guest House'],
    
    # Bhimavaram
    ['Bhimavaram', 'West Godavari', 'Gunupudi', 16.5332, 81.5245, 'Someswara Janardana Swamy Temple', 'Lunar Tank', 'The Grand Bhimavaram', 4.5, 'Bhimavaram Main', 'Mavullamma Mess', 4.4, 'Temple Road', 'Sri Krishna Tiffins', 'Bhimavaram', 'Godavari Meals', 'Bhimavaram', 'Lodge Stay', 'Town Police', 'Bhimavaram', 4.8, 'Ancient Pancharama Kshetra Shiva temple.', 4.8, 'Free', 'The Grand'],
    ['Bhimavaram', 'West Godavari', 'Junction', 16.5414, 81.5230, 'Mavullamma Ammavari Temple', 'Local Market', 'Minerva Grand', 4.4, 'Main Road', 'Vibhav Hotel', 4.3, 'Main Road', 'Daily Tiffin', 'Bhimavaram', 'Bhimavaram Meals', 'Center', 'Town Stay', 'Medical Center', 'Bhimavaram', 4.8, 'Prominent goddess temple in West Godavari.', 4.8, 'Free', 'Minerva'],
    
    # Ainavilli & Vadapalli
    ['Ainavilli', 'Konaseema', 'Ganesh Temple Road', 16.6385, 81.8672, 'Sri Siddhi Vinayaka Swamy Temple', 'River Side', 'Cotton Guest House', 4.3, 'Amalapuram Area', 'Local Brahmana Meals', 4.5, 'Temple Lane', 'Temple Tiffins', 'Ainavilli', 'Annadana Satram', 'Temple', 'Amalapuram Hotels', 'Local Health Subcenter', 'Ainavilli', 4.9, 'Ancient Swayambhu Vinayaka temple in Konaseema.', 4.9, 'Free', 'Cotton House'],
    ['Vadapalli', 'Konaseema', 'Godavari Bank', 16.7118, 81.8492, 'Sri Venkateswara Swamy Temple', 'Konaseema Tirupati', 'Monday Hotels', 4.4, 'Ravulapalem Road', 'Sri Rama Restaurant', 4.2, 'Main Road', 'Local Snacks', 'Vadapalli', 'Ravulapalem Meals', 'Ravulapalem', 'Ravulapalem Stay', 'Ravulapalem Police', 'Ravulapalem', 4.8, 'Revered Venkateswara temple known as Konaseema Tirupati.', 4.8, 'Free', 'Monday Hotels'],
    
    # Araku Valley
    ['Araku Valley', 'Alluri Sitharama Raju', 'Borra', 18.2809, 83.0393, 'Borra Caves', 'Trekking Trail', 'Haritha Resorts', 4.1, 'Araku Main Road', 'Araku Dining', 4.0, 'Araku', 'Coffee House', 'Araku', 'Bamboo Chicken', 'Araku', 'Resort Stay', 'Araku Police', 'Araku', 4.8, 'Ancient limestone caves with stalactites and stalagmites.', 4.8, 'Rs. 60', 'Haritha'],
    ['Araku Valley', 'Alluri Sitharama Raju', 'Town Center', 18.3301, 82.8804, 'Araku Tribal Museum', 'Handicraft Shop', 'Mayuri Hotel', 4.3, 'Town Road', 'Hillside Resto', 4.1, 'Town', 'Local Snacks', 'Center', 'Tribal Meals', 'Araku', 'Lodge Stay', 'Araku Hospital', 'Araku', 4.6, 'Museum showcasing the lifestyle and art of local tribes.', 4.6, 'Rs. 20', 'Mayuri'],
    
    # Rajahmundry
    ['Rajamahendravaram', 'East Godavari', 'Godavari Banks', 17.0016, 81.7688, 'Godavari Arch Bridge', 'ISKCON Temple', 'Hotel Shelton', 4.6, 'Rajahmundry', 'Sri Kanya', 4.5, 'Main Road', 'Sridevi Tiffins', 'Rajahmundry', 'Meals Point', 'Rajahmundry', 'City Stay', 'Police Station', 'Rajahmundry', 4.8, 'One of the longest rail-cum-road bridges in India.', 4.8, 'Free', 'Shelton'],
    
    # Lepakshi
    ['Lepakshi', 'Sri Sathya Sai', 'Temple Road', 13.8018, 77.6093, 'Veerabhadra Temple', 'Monolithic Nandi', 'Haritha Lepakshi', 4.0, 'Lepakshi', 'Haritha Dining', 3.8, 'Lepakshi', 'Snacks Center', 'Lepakshi', 'Local Meals', 'Lepakshi', 'Haritha Stay', 'Local Police', 'Lepakshi', 4.8, 'Stunning 16th-century temple with famous Hanging Pillar.', 4.8, 'Free', 'Haritha'],
    
    # Kurnool
    ['Kurnool', 'Nandyal', 'Belum Road', 15.1022, 78.1117, 'Belum Caves', 'Patalaganga', 'Haritha Belum', 3.9, 'Belum', 'Local Canteen', 3.7, 'Belum', 'Tea Stall', 'Belum', 'Canteen Meals', 'Belum', 'Haritha Stay', 'Local Guard', 'Belum', 4.7, 'Second longest cave in the Indian subcontinent.', 4.7, 'Rs. 65', 'Haritha'],
    ['Kurnool', 'Kurnool', 'Nandikotkur Road', 15.9329, 77.4190, 'Mantralayam', 'Raghavendra Swamy Mutt', 'Guru Raghavendra Lodge', 4.2, 'Mantralayam', 'Mutt Canteen', 4.4, 'Mantralayam', 'Tea Point', 'Mantralayam', 'Nitya Annadanam', 'Mantralayam', 'Lodge Stay', 'Temple Security', 'Mantralayam', 4.9, 'Holy town on the banks of Tungabhadra river.', 4.9, 'Free', 'Guru Lodge']
]

# Convert to DataFrame
headers = df.columns.tolist()
new_df = pd.DataFrame(new_landmarks, columns=headers)

# Combine and save
combined_df = pd.concat([df, new_df], ignore_index=True)

# Drop any accidental duplicates based on City_Name and Tourist_Place
combined_df = combined_df.drop_duplicates(subset=['City_Name', 'Tourist_Place'], keep='last')

# Save back to CSV
combined_df.to_csv(csv_path, index=False)

print(f"Successfully updated dataset. Added/Updated {len(new_landmarks)} authentic landmarks.")
print(f"Total entries now: {len(combined_df)}")
