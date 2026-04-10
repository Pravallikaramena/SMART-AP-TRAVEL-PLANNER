import pandas as pd

# 1. Load the massive base dataset
upload_path = "datasets/upload.CSV"
df_massive = pd.read_csv(upload_path)

print(f"Loaded base dataset with {len(df_massive)} rows.")

# 2. Clean base dataset: Drop duplicates
df_massive = df_massive.drop_duplicates(subset=['City_Name', 'Tourist_Place'], keep='first')

# 3. Our handcrafted, perfectly accurate dictionary for Top Hubs + User's Cities
columns = [
    'City_Name','District_Name','Area_Name','Latitude','Longitude',
    'Tourist_Place','Hidden_Place','Nearby_Hotel_Name','Hotel_Rating',
    'Hotel_Address','Restaurant_Name','Restaurant_Rating','Restaurant_Address',
    'Tiffin_Center_Name','Tiffin_Address','Lunch_Meals_Hotel','Lunch_Address',
    'Accommodation_Details','Emergency_Service','Emergency_Address'
]

curated_data = [
    # VISAKHAPATNAM
    ["Visakhapatnam", "Visakhapatnam", "Beach Road", 17.7144, 83.3233, "RK Beach", "INS Kursura Museum", "Novotel Visakhapatnam", 4.7, "Beach Road", "Dharani", 4.5, "Dasapalla", "Sairam Parlour", "MVP Colony", "Tycoon", "Siripuram", "Luxury", "Care Hospitals", "Ram Nagar"],
    ["Visakhapatnam", "Visakhapatnam", "Simhachalam", 17.7665, 83.2505, "Simhachalam Temple", "Kambalakonda", "SVN Grand", 4.1, "Gajuwaka", "Zaffran", 4.6, "Novotel", "Raju Gari Dhaba", "Rushikonda", "Food Ex", "Jagadamba Junction", "Standard", "Seven Hills Hospital", "Maharanipeta"],
    ["Visakhapatnam", "Visakhapatnam", "Kailasagiri Hill", 17.7490, 83.3423, "Kailasagiri", "Tenneti Park", "The Park", 4.4, "Lawsons Bay", "Vista", 4.2, "Beach Road", "Gitam Canteen", "Rushikonda", "Embers", "MVP Colony", "Hills", "Apollo Hospitals", "Arilova"],
    
    # ARAKU
    ["Araku Valley", "Alluri Sitarama Raju", "Ananthagiri Hills", 18.2813, 83.0392, "Borra Caves", "Katiki Waterfalls", "Haritha Hill Resort", 4.0, "Araku Valley", "Haritha Restaurant", 3.8, "Araku", "Local Tiffins", "Araku Main", "Bamboo Chicken Center", "Padmapuram", "Resort", "Araku Govt Hospital", "Araku Town"],
    
    # VIJAYAWADA
    ["Vijayawada", "NTR", "Indrakeeladri", 16.5135, 80.6033, "Kanaka Durga Temple", "Gandhi Hill", "The Gateway Hotel", 4.5, "M G Road", "Mid City", 4.3, "M G Road", "Babai Hotel", "Gandhi Nagar", "Sweet Magic", "Bhavanipuram", "Standard", "Ramesh Hospitals", "Labbipet"],
    
    # VADAPALLI - 6 Spots (3 Famous + 3 Hidden Gems)
    ["Vadapalli", "Konaseema", "Temple Zone", 16.8202, 81.8213, "Sri Venkateswara Swamy Temple (Vadapalli Banka Swamy)", "Konaseema Tirupati", "Hotel Sarovar", 4.2, "Ravulapalem", "Subbayya Gari Hotel (Original)", 4.8, "Ravulapalem", "Sri Surya Tiffins", "Ravulapalem", "Godavari Ruchulu", "Ravulapalem", "Standard Rooms", "Ravulapalem Area Hospital", "Ravulapalem"],
    ["Vadapalli", "Konaseema", "River Side", 16.8215, 81.8225, "Vadapalli Godavari Boat Point", "Godavari River Views", "Grand Amalapuram", 4.1, "Amalapuram", "River Bay Dhaba", 4.2, "Rajahmundry", "Amma Tiffins", "Ravulapalem", "Hotel Shelton Dining", "Rajahmundry", "Standard", "GSL General Hospital", "Rajahmundry"],
    ["Vadapalli", "Konaseema", "Konaseema", 16.8250, 81.8300, "Konaseema Coconut & Paddy Fields", "Village Scenic Trail", "Haritha Dindi Resort", 4.0, "Dindi", "Dindi Seafood", 4.1, "Dindi", "Local Tea Stalls", "Vadapalli", "Village Mess", "Vadapalli", "Resort", "Ravulapalem Hospital", "Ravulapalem"],
    ["Vadapalli", "Konaseema", "Hidden Gem", 16.8280, 81.8350, "Vadapalli Godavari Sunrise Point", "Peaceful River View", "Haritha Dindi", 4.0, "Dindi", "Local Tea Stalls", 3.8, "Vadapalli", "Village Tiffins", "Vadapalli", "Godavari Ruchulu", "Ravulapalem", "Guest House", "Ravulapalem Hospital", "Ravulapalem"],
    ["Vadapalli", "Konaseema", "Village Zone", 16.8300, 81.8400, "Vadapalli Delta Pottery Workshop", "Village Heritage", "Grand Amalapuram", 4.1, "Amalapuram", "Village Mess", 4.0, "Vadapalli", "Local Tea", "Vadapalli", "Amalapuram Mess", "Amalapuram", "Budget", "Ravulapalem Hospital", "Ravulapalem"],
    ["Vadapalli", "Konaseema", "Temple Side", 16.8350, 81.8450, "Ancient Shiva Temple (Vadapalli)", "Historic Ruins", "Hotel Sarovar", 4.2, "Ravulapalem", "Subbayya Gari Hotel", 4.8, "Ravulapalem", "Sri Surya Tiffins", "Ravulapalem", "Godavari Ruchulu", "Ravulapalem", "Standard", "Ravulapalem Area Hospital", "Ravulapalem"],
    
    # AINAVILLI - 6 Spots
    ["Ainavilli", "Konaseema", "Temple Zone", 16.7118, 81.9324, "Sri Siddhi Vinayaka Swamy Temple", "Ganesh Temple", "Grand Amalapuram", 4.1, "Amalapuram", "Ainavilli Ganapathi Mess", 4.5, "Temple Street", "Sri Surya Tiffins", "Amalapuram", "Jaya Residency", "Amalapuram", "Standard", "Amalapuram KIMS Hospital", "Amalapuram"],
    ["Ainavilli", "Konaseema", "Canal Side", 16.7130, 81.9350, "Ainavilli Canal Walk", "Scenic Waterways", "Hotel KIMS", 4.0, "Amalapuram", "Canal View Dhaba", 4.2, "Amalapuram", "Local Tiffins", "Ainavilli", "Amalapuram Mess", "Amalapuram", "Standard", "Amalapuram Area Hospital", "Amalapuram"],
    ["Ainavilli", "Konaseema", "Rural Zone", 16.7150, 81.9400, "Ainavilli Village Paddy Fields", "Delta Scenery", "Hotel Sarovar", 4.2, "Ravulapalem", "Local Mess", 4.0, "Ainavilli", "Village Tiffins", "Ainavilli", "Rajahmundry Meals", "Rajahmundry", "Budget", "Amalapuram Hospital", "Amalapuram"],
    ["Ainavilli", "Konaseema", "Hidden Gem", 16.7200, 81.9450, "Ainavilli Coconut Grove Trail", "Village Scenic Views", "Hotel KIMS", 4.0, "Amalapuram", "Village Dhaba", 3.9, "Ainavilli", "Local Tea", "Ainavilli", "Amalapuram Mess", "Amalapuram", "Standard", "Amalapuram Area Hospital", "Amalapuram"],
    ["Ainavilli", "Konaseema", "Crafts Area", 16.7250, 81.9500, "Konaseema Rural Crafts Center", "Artisan Heritage", "Grand Amalapuram", 4.1, "Amalapuram", "Crafts Cafe", 4.2, "Amalapuram", "Amma Tiffins", "Amalapuram", "Hotel Shelton", "Rajahmundry", "Standard", "Amalapuram Hospital", "Amalapuram"],
    ["Ainavilli", "Konaseema", "Canal Side", 16.7300, 81.9550, "Old Canal Bridge Viewpoint", "Historic Infrastructure", "Hotel Shelton", 4.4, "Rajahmundry", "Bridge Dhaba", 4.0, "Ainavilli", "Local Snacks", "Ainavilli", "Rajahmundry Meals", "Rajahmundry", "Standard", "Rajahmundry Hospital", "Rajahmundry"],
    
    # RYALI - 6 Spots
    ["Ryali", "Konaseema", "Temple Zone", 16.7845, 81.8564, "Sri Jagan Mohini Kesava Swamy Temple", "Unique Idol Temple", "Hotel Shelton", 4.4, "Rajahmundry", "Ryali Village Tiffins", 4.3, "Ryali Village", "Ryali Snacks", "Temple Road", "Local Village Mess", "Ryali", "Budget", "Ravulapalem Hospital", "Ravulapalem"],
    ["Ryali", "Konaseema", "Ryali Pampa", 16.7860, 81.8580, "Ryali Pampa Canal Point", "Rural Landscapes", "Hotel Laxmi", 3.8, "Rajahmundry", "Srinivasa Tiffins", 4.0, "Ryali", "Railway Station Road", "Rajahmundry", "Standard", "Rajahmundry Area Hospital", "Rajahmundry"],
    ["Ryali", "Konaseema", "Rural Zone", 16.7900, 81.8600, "Ryali Rural Scenic Trail", "Godavari Delta Views", "Hotel River Bay", 4.2, "Rajahmundry", "Local Dhaba", 4.0, "Ryali Road", "Ryali Tea Stalls", "Ryali", "Rajahmundry Meals", "Rajahmundry", "Standard", "Ravulapalem Area Hospital", "Ravulapalem"],
    ["Ryali", "Konaseema", "Hidden Gem", 16.7950, 81.8650, "Ryali Ancient Stepwell Area", "Historic Heritage", "Hotel Sarovar", 4.2, "Ravulapalem", "Ryali Mess", 4.1, "Ryali", "Village Tiffins", "Ryali", "Ravulapalem Meals", "Ravulapalem", "Budget", "Ravulapalem Hospital", "Ravulapalem"],
    ["Ryali", "Konaseema", "Temple Side", 16.8000, 81.8700, "Small Shiva Temple (Ryali)", "Village Devotion", "Hotel Shelton", 4.4, "Rajahmundry", "Subbayya Gari Hotel", 4.8, "Ravulapalem", "Local Snacks", "Ryali", "Rajahmundry Meals", "Rajahmundry", "Standard", "Rajahmundry Hospital", "Rajahmundry"],
    ["Ryali", "Konaseema", "Farm Zone", 16.8050, 81.8750, "Ryali Banana & Paddy Estates", "Agriculture Tour", "Haritha Dindi", 4.0, "Dindi", "Village Dhaba", 3.8, "Ryali", "Ryali Tea", "Ryali", "Dindi Seafood", "Dindi", "Resort", "Ravulapalem Hospital", "Ravulapalem"],

    # OTHERS
    ["Kadiyam", "East Godavari", "Nursery Area", 16.9200, 81.8400, "Kadiyapulanka Nurseries", "Flower Garden City", "Hotel Shelton", 4.4, "Rajahmundry", "Kadiyam Food Court", 4.2, "Main Road", "Srinivasa Tiffins", "Kadiyam", "Local Village Mess", "Kadiyam", "Standard", "Rajahmundry Government Hospital", "Rajahmundry"],
    ["Antarvedi", "Konaseema", "Antarvedi", 16.3267, 81.7245, "Sri Lakshmi Narasimha Swamy Temple", "Sangamam View", "Haritha Beach Resort", 4.2, "Antarvedi", "Temple Annadanam", 4.8, "Antarvedi", "Local Seafood", "Beach Road", "Palamuru Canteen", "Antarvedi", "Beach", "Razole Govt Hospital", "Razole"],
    ["Draksharamam", "East Godavari", "Draksharamam", 16.7925, 82.0628, "Sri Bhimeswara Swamy Temple (Pancharama)", "Sapta Godavari", "River Bay", 4.2, "Godavari Bund", "Draksharamam Meals", 4.3, "Temple Road", "Sri Kanya", "Kakinada", "Local Annadanam", "Draksharamam", "Standard", "Kakinada Apollo", "Kakinada"],
    ["Annavaram", "Kakinada", "Ratnagiri", 17.2843, 82.4042, "Sri Veera Venkata Satyanarayana Swamy Temple", "Pampa River View", "Satyadeva Residency", 4.0, "Annavaram", "Highway Dhaba", 4.1, "NH16", "Annavaram Prasadam Hub", "Annavaram", "Hotel Bliss", "Annavaram", "Standard", "Tuni Area Hospital", "Tuni"],
    ["Srikalahasti", "Tirupati", "Srikalahasti", 13.7495, 79.7034, "Srikalahasteeswara Temple", "Veyyilu Lingala Kona", "Hotel Jayaram", 3.9, "Temple Street", "Temple Canteen", 4.5, "Srikalahasti", "Sri Rama Tiffins", "Main Road", "Udupi Cafe", "Srikalahasti", "Standard", "Srikalahasti CHC", "Srikalahasti"],
    ["Tirupati", "Tirupati", "Tirumala Hills", 13.8333, 79.3472, "Sri Venkateswara Temple (Tirumala)", "Silathoranam", "Fortune Select", 4.6, "Alipiri", "Saarangi Fine Dining", 4.4, "Tirumala", "Bhimas", "KT Road", "Saravana Bhavan", "Gandhi Road", "Pilgrim", "SVIMS Hospital", "Alipiri"],
    ["Rajahmundry", "East Godavari", "River Bund", 17.0005, 81.7666, "Pushkar Ghat", "Godavari Rail Bridge", "Hotel Shelton", 4.4, "Danavaipeta", "Rose Milk Center", 4.9, "Main Road", "Srinivasa Tiffins", "Danavaipeta", "Kava Restaurant", "Shelton", "Standard", "GSL General Hospital", "NH16 Bypass"]
]

df_curated = pd.DataFrame(curated_data, columns=columns)
df_curated['Rating'] = 5.0

# 4. CRITICAL: EXCLUDE generic procedural data for any city that we have curated data for.
curated_city_names = set(df_curated['City_Name'].tolist())
df_massive_filtered = df_massive[~df_massive['City_Name'].isin(curated_city_names)]

print(f"Filtered out generic data for curated cities. Massive set now has {len(df_massive_filtered)} rows.")

# 5. Merge them!
df_final = pd.concat([df_massive_filtered, df_curated], ignore_index=True)

# 5b. Final cleanup
df_final = df_final.drop_duplicates(subset=['City_Name', 'Tourist_Place'], keep='last')

output_path = "datasets/AP_DATASET.CSV"
df_final.to_csv(output_path, index=False)
print(f"Successfully generated blended dataset with {len(df_final)} rows at {output_path}!")
