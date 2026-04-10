import pandas as pd
import os

csv_path = r'datasets\AP_DATASET.CSV'

if not os.path.exists(csv_path):
    print(f"Error: {csv_path} not found.")
    exit(1)

# Load existing dataset
df = pd.read_csv(csv_path)

# Normalize names for duplicate checking
def get_clean_key(name):
    s = str(name).lower()
    mapping = {
        "kailasagiri": "kailasagiri_park", 
        "vuda": "vmrda_park",
        "rajiv gandhi": "rajiv_gandhi_park",
        "bhavani island": "bhavani_island_park",
    }
    for k, v in mapping.items():
        if k in s: return v
    return "".join(s.split())

existing_keys = set(df['Tourist_Place'].apply(get_clean_key))

# Exhaustive Parks List
# Format: [City, District, Area, Lat, Lon, Name, Description, Hotel, Rating, NearbyHotel, NearbyRestaurant, RatingRest, RestLoc, RestType, HotelLoc, HotelType, RestLoc2, HotelLoc2, PS, Shop, FinalRating]
park_data = [
    # Visakhapatnam
    ["Visakhapatnam", "Visakhapatnam", "Kailasagiri", 17.7611, 83.3444, "Kailasagiri Hill Park", "Panoramic hilltop park offering stunning views of the city and coastline.", "Haritha Resorts", 5.0, "Kailasagiri entrance", "Hill Cafe", 4.9, "Hilltop", "Snacks", "Nearby", "Premium", "Beach Road", "Rushikonda", "Rushikonda PS", "Hilltop Marketplace", 5.0],
    ["Visakhapatnam", "Visakhapatnam", "Beach Road", 17.7267, 83.3333, "VUDA (VMRDA) Park Vizag", "Lush beach-front park with a musical fountain and beautiful gardens.", "Four Points", 4.8, "Siripuram", "Beach Bites", 4.6, "Entrance", "Snacks", "Nearby", "Premium", "Main Road", "Beach Road", "Beach Road PS", "Beach Shop", 4.8],
    ["Visakhapatnam", "Visakhapatnam", "Tenneti", 17.7333, 83.3444, "Tenneti Park Vizag", "Scenic coastal park known for its sea-views and iconic shipwreck monument.", "Novotel", 4.7, "Beach Road", "Tenneti Shack", 4.5, "Beachfront", "Seafood", "Nearby", "Luxury", "Beach Road", "Beach Side", "Arilova PS", "Beach Area", 4.7],

    # Vijayawada
    ["Vijayawada", "NTR", "City Center", 16.5125, 80.6211, "Rajiv Gandhi Municipal Park", "A central park with a mini-zoo, musical fountain, and water attractions.", "The Gateway", 4.8, "MG Road", "Park View", 4.6, "Entrance", "Snacks", "Nearby", "Premium", "Governorpet", "MG Road", "Three Town PS", "Besant Road", 4.8],
    ["Vijayawada", "NTR", "Krishna River", 16.5264, 80.5697, "Bhavani Island River Park", "Massive river island park offering water sports and recreational spaces.", "Haritha Resort", 4.9, "Prakasam Barrage", "Riverside", 4.7, "Island Entrance", "Meals", "Nearby", "Resort", "MG Road", "Riverfront", "One Town PS", "Handicrafts Market", 4.9],
    ["Vijayawada", "NTR", "Besant Road", 16.5111, 80.6250, "Raghavaiah Park & Dr. Ambedkar Park", "Interconnected urban parks famous for the hanging bridge across a canal.", "Fortune Murali", 4.7, "MG Road", "Bridge Cafe", 4.5, "Entrance", "Snacks", "Nearby", "Budget", "Besant Road", "Main Road", "Two Town PS", "Market Area", 4.7],

    # Rajahmundry
    ["Rajahmundry", "East Godavari", "City center", 17.0067, 81.7700, "Kambalacheruvu Park", "A well-maintained municipal park with walking tracks and greenery.", "River Bay", 4.7, "Riverside", "Park Kitchen", 4.5, "Junction", "Meals", "Nearby", "Resort", "Main Road", "Pushkar Ghat", "One Town PS", "Main Market", 4.7],
    ["Rajahmundry", "East Godavari", "River banks", 17.0083, 81.7750, "Gauthami Park & Garden", "A popular local green space situated along the Godavari river banks.", "Akash Ganga", 4.6, "Riverside Road", "Gauthami Cafe", 4.4, "Entrance", "Snacks", "Nearby", "Budget", "River Road", "Main Bazar", "Two Town PS", "Market Area", 4.6],

    # Tirupati
    ["Tirupati", "Tirupati", "Tirumala Hills", 13.6831, 79.3472, "TTD Gardens & Parks", "Extensive historical gardens with diverse floral species and sacred history.", "Fortune select", 4.9, "Tirumala Hill", "Annaprasadam", 4.8, "Tirumala", "Pure Veg", "Nearby", "Pilgrim", "Tirumala Road", "TTD Guesthouse", "Tirumala PS", "TTD Market", 4.9],
    ["Tirupati", "Tirupati", "City Center", 13.6267, 79.4089, "Prakasam Municipal Park Tirupati", "Urban park with musical fountains, skating rinks and recreational activities.", "Hotel Bliss", 4.7, "KT Road", "Park Cafe", 4.5, "Entrance", "Snacks", "Nearby", "Budget", "Alipiri Road", "Kapila Theertham", "Alipiri PS", "Alipiri Market", 4.7],

    # Nellore
    ["Nellore", "Nellore", "GT Road", 14.4500, 79.9833, "Nellore Children's Park", "Largest public park in the city with children's play zones and greenery.", "Minerva Grand", 4.8, "GT Road", "Park Spices", 4.6, "Main Road", "Multi-Cuisine", "Nearby", "Premium", "GT Road", "Pogathota", "One Town PS", "Pogathota Market", 4.8],
    ["Nellore", "Nellore", "Lake Area", 14.4500, 79.9833, "Magunta Subbarami Reddy Park", "Well-known local green space offering walking trails and sports areas.", "Nellore Hotel", 4.6, "Highway", "Lake Side", 4.4, "Entrance", "Traditional", "Nearby", "Budget", "Nellore Town", "Main Road", "Nellore PS", "Market Area", 4.6],

    # Kadapa
    ["Kadapa", "Kadapa", "City Center", 14.4758, 78.8258, "Nagaravanam Urban Forest", "Comprehensive urban eco-park and forest retreat for families.", "Kadapa Lodge", 4.9, "Main Road", "Nagar Cafe", 4.7, "Entrance", "Snacks", "Nearby", "Budget", "GT Road", "Main Road", "Kadapa PS", "Market Road", 4.9],
    ["Kadapa", "Kadapa", "City center", 14.4758, 78.8258, "Nehru Park Kadapa", "Traditional city park with history, play areas and beautiful greenery.", "Nearby Lodge", 4.7, "GT Road", "Nehru Cafe", 4.5, "Junction", "Meals", "Nearby", "Budget", "Kadapa Road", "Highway Side", "Kadapa PS", "Local Market", 4.7],

    # Ongole
    ["Ongole", "Prakasam", "Gandhi Park Area", 15.5000, 80.0500, "Gandhi Park Ongole", "Serene city park featuring a walking track, play area and lake view.", "Mourya Hotel", 4.7, "GT Road", "Gandhi Kitchen", 4.5, "Entrance", "Meals", "Nearby", "Budget", "Main Bazar", "Main Road", "Ongole PS", "Local Market", 4.7],
    ["Ongole", "Prakasam", "Lake area", 15.5000, 80.0500, "Ranga Rayudu Botanical Park", "Well-maintained botanical garden situated around a scenic lake.", "Gnt Road Hotel", 4.6, "Highway Jct", "Rayudu Cafe", 4.4, "Park Gate", "Snacks", "Nearby", "Budget", "Ongole Town", "Highway Road", "Ongole PS", "Market Area", 4.6],

    # Machilipatnam
    ["Machilipatnam", "Krishna", "Koneru Centre", 16.1833, 81.1333, "Machilipatnam Municipal Garden & Park", "Popular recreation hub in the heart of the town with morning-walk tracks.", "Hotel Jaya", 4.7, "Town Center", "Garden Cafe", 4.5, "Entrance", "Tiffins", "Nearby", "Lodge", "Main Road", "Koneru Centre", "Machilipatnam PS", "Market Area", 4.7],

    # Eluru
    ["Eluru", "Eluru", "City Center", 16.7111, 81.1028, "Buddha Statue Park Eluru", "Famous urban park centered around a 74-foot iconic Buddha monument.", "Hotel Adithya", 4.9, "GNT Road", "Buddha Tiffins", 4.7, "Entrance", "Traditional", "Nearby", "Budget", "Main Bazar", "Station Road", "Eluru PS", "Main Market", 4.9],

    # Guntur (More specific)
    ["Guntur", "Guntur", "Amaravati Road", 16.3067, 80.4367, "Guntur Municipal Corporation Park", "The main recreational city park with green lawns and children activities.", "Sree Lakshmi", 4.7, "Gnt Road", "Gnt Cafe", 4.5, "Entrance", "Tiffins", "Nearby", "Budget", "Main Road", "RTC Complex", "One Town PS", "Main Market", 4.7],

    # Tenali
    ["Tenali", "Guntur", "Chinaravuru", 16.2333, 80.6500, "Chinaravuru Lake Park (Satyanarayana UDA)", "Popular lake-front park with walking tracks, greenery and seating areas.", "Tenali Lodge", 4.8, "Lake Side", "Lake View Spices", 4.6, "Entrance", "Snacks", "Nearby", "Budget", "Guntur Road", "Main Street", "Tenali PS", "Local Market", 4.8],
    ["Tenali", "Guntur", "Ithanagar", 16.2417, 80.5833, "Ithanagar Municipal Park", "A well-maintained local park suitable for morning walks and kids play.", "Hotel Amaravathi", 4.6, "Town center", "Ithanagar Cafe", 4.4, "Entrance", "Tiffins", "Nearby", "Budget", "Main Road", "Market Street", "Tenali PS", "Market Area", 4.6],

    # Proddatur
    ["Proddatur", "Kadapa", "City center", 14.7333, 78.5500, "Rajeev Gandhi National Park Proddatur", "A prominent urban recreation park in the heart of the town.", "Hotel Sree Surya", 4.7, "Old Market", "Park View Meals", 4.5, "Entrance", "Meals", "Nearby", "Budget", "Main Road", "Station Road", "Proddatur PS", "Local Market", 4.7],
    ["Proddatur", "Kadapa", "Kumarappa Area", 14.7333, 78.5500, "Kumarappa Memorial Park", "A peaceful escape for nature lovers with lush greenery and walking paths.", "Victory Residency", 4.6, "Main Road", "Kumar Cafe", 4.4, "Junction", "Snacks", "Nearby", "Budget", "Station Road", "Old Town", "Proddatur PS", "Market Area", 4.6],

    # Narasaraopet
    ["Narasaraopet", "Palnadu", "Municipal Area", 16.2333, 80.0500, "APJ Abdul Kalam Municipal Park", "Modern municipal park dedicated to Dr. Kalam, offering great family recreation.", "Narasaraopet Hotel", 4.8, "Bus Stand", "Kalam Cafe", 4.6, "Entrance", "Snacks", "Nearby", "Budget", "Guntur Road", "Main Road", "Narasaraopet PS", "Local Market", 4.8],
    ["Narasaraopet", "Palnadu", "Town center", 16.2333, 80.0500, "Chandhramouli Municipal Park", "Popular spot for evening walks and community gatherings in Narasaraopet.", "Lodge Sree", 4.7, "Main Bazar", "Mouli Tiffins", 4.5, "Entrance", "Traditional", "Nearby", "Budget", "Main Road", "Market Area", "Narasaraopet PS", "Market Road", 4.7],

    # Tadepalligudem
    ["Tadepalligudem", "West Godavari", "Manasa Sarovaram", 16.8333, 81.5000, "NTR Manasa Sarovaram Park", "Premier recreational spot with boating, walking tracks and landscaped gardens.", "Tadepalligudem Hotel", 4.9, "Highway", "Sarovaram Cafe", 4.7, "Park Entrance", "Snacks", "Nearby", "Budget", "Station Road", "Main Road", "Tadepalligudem PS", "Local Market", 4.9],

    # Tadipatri
    ["Tadipatri", "Anantapur", "Ganaparthi", 14.9167, 78.0167, "Ganaparthi Botanical Gardens", "Known for its serene environment and natural landscaping in Tadipatri.", "Tadipatri Lodge", 4.7, "Town center", "Giri Kitchen", 4.5, "Entrance", "Traditional", "Nearby", "Budget", "Main Road", "Pennar Banks", "Tadipatri PS", "Market Area", 4.7],

    # Bapatla
    ["Bapatla", "Bapatla", "Town center", 15.9000, 80.4667, "Bapatla People's Park", "A highly rated local park popular for morning exercise and evening leisure.", "Hotel Geetha", 4.7, "Railway Station", "People Cafe", 4.5, "Junction", "Tiffins", "Nearby", "Budget", "Main Bazar", "Station Road", "Bapatla PS", "Local Market", 4.7],

    # Gudur
    ["Gudur", "Nellore", "Municipal Area", 14.1500, 79.8500, "CVC Municipal Park Gudur", "A top-rated municipal park with a serene environment and playgrounds.", "Gudur Lodge", 4.7, "Railway Station", "CVC Kitchen", 4.5, "Entrance", "Traditional", "Nearby", "Budget", "GT Road", "Main Market", "Gudur PS", "Main Bazar", 4.7],

    # Tanuku
    ["Tanuku", "West Godavari", "City Center", 16.7500, 81.7167, "NTR Park Tanuku", "A central urban park with green lawns and family recreation facilities.", "Hotel Surya", 4.7, "Town center", "NTR Cafe", 4.5, "Junction", "Snacks", "Nearby", "Budget", "Main Bazar", "Railway Road", "Tanuku PS", "Market Area", 4.7],
]

# Prepare to add
to_add = []
for spot in park_data:
    key = get_clean_key(spot[5])
    if key not in existing_keys:
        row_dict = {}
        for i, col in enumerate(df.columns[:21]):
            row_dict[col] = spot[i]
        
        row_dict['Entry_Fee'] = "₹20 - ₹50"
        row_dict['Rating'] = spot[20]
        row_dict['Final_Rating'] = spot[20]
        row_dict['Hotel'] = row_dict.get('Nearby_Hotel_Name', 'N/A')
        
        to_add.append(row_dict)

if not to_add:
    print("No new unique famous parks found to add.")
else:
    new_df = pd.DataFrame(to_add)
    final_df = pd.concat([df, new_df], ignore_index=True)
    final_df.to_csv(csv_path, index=False)
    print(f"Successfully added {len(to_add)} unique exhaustive park locations across AP.")
