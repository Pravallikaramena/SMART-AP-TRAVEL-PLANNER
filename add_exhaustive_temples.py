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
        "simhachalam": "simhachalam_temple", 
        "kanaka durga": "kanaka_durga_temple",
        "tirumala": "tirumala_temple",
        "iskcon": "iskcon_temple",
    }
    for k, v in mapping.items():
        if k in s: return v
    return "".join(s.split())

existing_keys = set(df['Tourist_Place'].apply(get_clean_key))

# Exhaustive Temples List
# Format: [City, District, Area, Lat, Lon, Name, Description, Hotel, Rating, NearbyHotel, NearbyRestaurant, RatingRest, RestLoc, RestType, HotelLoc, HotelType, RestLoc2, HotelLoc2, PS, Shop, FinalRating]
temple_data = [
    # Visakhapatnam
    ["Visakhapatnam", "Visakhapatnam", "Asilmetta", 17.7117, 83.3050, "Sree Sampath Vinayagara Temple", "Miraculous Ganesha temple, one of the most visited in the city.", "Green Park", 5.0, "RTC Complex", "Green Park Rest", 4.9, "Asilmetta", "Global", "Asilmetta", "Luxury", "Main Junction", "RTC Complex", "II Town PS", "Market", 5.0],
    ["Visakhapatnam", "Visakhapatnam", "Rushikonda", 17.7811, 83.3517, "Rushikonda Venkateswara Swamy Temple", "Serene temple on a hilltop with breathtaking views of the ocean.", "Haritha Resorts", 4.8, "Beach Road", "Beach Tiffins", 4.6, "Hilltop", "Snacks", "Nearby", "Resort", "Beach Side", "Rushikonda", "Rushikonda PS", "Beach Side", 4.8],
    ["Visakhapatnam", "Visakhapatnam", "Beach Road", 17.7125, 83.3211, "Kali Temple Vizag", "Unique modern architecture dedicated to Goddess Kali, located right on the beach road.", "The Park", 4.7, "Beach Road", "Palm Cafe", 4.5, "Beachfront", "Seafood", "Nearby", "Luxury", "Beach Road", "Beach Road", "Beach Road PS", "Park Area", 4.7],

    # Vijayawada
    ["Vijayawada", "NTR", "Indrakeeladri", 16.5189, 80.6214, "Subramanya Swamy Temple", "Sacred temple of Lord Kartikeya on the Indrakeeladri hillock.", "Fortune Murali", 4.8, "Indrakeeladri", "Hill Side Tiffins", 4.6, "Hill Entrance", "Vegetarian", "Nearby", "Premium", "Governorpet", "MG Road", "One Town PS", "Besant Road", 4.8],
    ["Vijayawada", "NTR", "Godavari Banks", 16.5181, 80.6122, "Sri Ramalingeswara Swamy Temple", "Historic Shiva temple known for its divine vibrations and river views.", "The Gateway", 4.7, "Riverside", "River Cafe", 4.5, "Ghat Road", "Meals", "Nearby", "Luxury", "Besant Road", "Main Road", "Three Town PS", "Main Market", 4.7],

    # Guntur (More specific)
    ["Guntur", "Guntur", "Mangalagiri", 16.4386, 80.5606, "Sri Panakala Narasimha Swamy", "Ancient hill temple where devotees offer jaggery water (Panakam) to the deity.", "Lodge Mangalagiri", 5.0, "Hill Base", "Giri Tiffins", 4.8, "Hilltop", "Traditional", "Nearby", "Budget", "Highway Jct", "Main Road", "Mangalagiri PS", "Handloom Market", 5.0],

    # Nellore
    ["Nellore", "Nellore", "Jonnawada", 14.5333, 79.9167, "Jonnawada Kamakshi Temple", "Powerful Goddess temple on the banks of Penna river.", "Nellore Lodge", 4.9, "Main Road", "Temple Meals", 4.7, "Junction", "Pure Veg", "Nearby", "Budget", "Nellore Road", "GT Road", "Nellore PS", "Local Market", 4.9],
    ["Nellore", "Nellore", "Narasimhakonda", 14.4667, 79.8833, "Vedagiri Lakshmi Narasimha Swamy", "Hill temple with seven sacred ponds and historic significance.", "Nellore Hotel", 4.8, "Highway", "Hill Tiffins", 4.6, "Entrance", "Traditional", "Nearby", "Budget", "Nellore Road", "Main Road", "Nellore PS", "Temple Market", 4.8],

    # Rajahmundry
    ["Rajahmundry", "East Godavari", "River Road", 17.0067, 81.7700, "Sri Uma Markandeyeswara Swamy Temple", "One of the most ancient and important Shiva temples in Rajahmundry.", "Hotel River Bay", 4.9, "Pushkar Ghat", "Ghat Meals", 4.7, "Ghat Entrance", "Traditional", "Riverside", "Resort", "Main Road", "Pushkar Ghat", "One Town PS", "Main Bazar", 4.9],
    ["Rajahmundry", "East Godavari", "Godavari banks", 17.0083, 81.7750, "Sri Vallabha Ganapati Temple", "A beautiful temple of Ganesha popular for its architectural beauty.", "Akash Ganga", 4.7, "Riverside", "Ganapati Cafe", 4.5, "Entrance", "Snacks", "Nearby", "Budget", "River Road", "Main Bazar", "Two Town PS", "Market Area", 4.7],

    # Kadapa
    ["Kadapa", "Kadapa", "City Center", 14.4758, 78.8258, "Devuni Kadapa", "Gateway to Tirumala, dedicated to Lord Venkateswara.", "Kadapa Lodge", 5.0, "Main Road", "Devuni Tiffins", 4.8, "Junction", "Pure Veg", "Nearby", "Budget", "GT Road", "Main Road", "Kadapa PS", "Market Road", 5.0],
    ["Kadapa", "Kadapa", "Pushpagiri", 14.6000, 78.7500, "Pushpagiri Temple Complex", "Cluster of ancient temples on a hillock, known for its scenic beauty.", "Nearby Lodge", 4.8, "Hill Base", "Hill Meals", 4.6, "Junction", "Traditional", "Nearby", "Budget", "Kadapa Road", "Highway Side", "Kadapa PS", "Local Market", 4.8],

    # Kurnool
    ["Kurnool", "Kurnool", "Mantralayam", 15.9333, 77.4167, "Mantralayam Raghavendra Swamy Mutt", "Sacred site of Saint Raghavendra Swamy, a major pilgrim destination.", "Mutt Guesthouse", 5.0, "Temple Entrance", "Mutt Meals", 5.0, "Campus", "Pure Veg", "Campus", "Guesthouse", "Main Road", "Town Area", "Mantralayam PS", "Mutt Market", 5.0],
    ["Kurnool", "Nandyal", "Mahanandi", 15.4744, 78.6253, "Nava Nandi Temples", "A cluster of nine sacred Nandi temples around the main Mahanandi temple.", "Haritha Nandyal", 4.9, "Mahanandi Road", "Nandi Tiffins", 4.7, "Entrance", "Traditional", "Nearby", "Budget", "Nandyal Highway", "Main Road", "Mahanandi PS", "Temple Market", 4.9],

    # Anantapur
    ["Anantapur", "Anantapur", "Bugga", 15.0000, 77.5000, "Bugga Ramalingeswara Swamy Temple", "Historic temple known for its natural water spring (Bugga).", "Anantapur Hotel", 4.7, "Highway", "Bugga Cafe", 4.5, "Junction", "Snacks", "Nearby", "Budget", "Main Road", "Anantapur Town", "Anantapur PS", "Local Market", 4.7],

    # Machilipatnam
    ["Machilipatnam", "Krishna", "Chilakalapudi", 16.1833, 81.1333, "Sai Maharaj Devalayam", "Popular modern temple dedicated to Shirdi Sai Baba.", "Hotel Jaya", 4.8, "Town center", "Sai Cafe", 4.6, "Entrance", "Tiffins", "Nearby", "Lodge", "Main Road", "Koneru Centre", "Chilakalapudi PS", "Market Area", 4.8],
    ["Machilipatnam", "Krishna", "Dattashram", 16.1500, 81.2000, "Ancient Shiva Temple Dattashram", "Holy site on the banks of Krishna river where Dattatreya performed penance.", "Beach Resort", 4.7, "Beach Road", "Ashram Meals", 4.5, "Entrance", "Traditional", "Nearby", "Budget", "Beach Front", "Main Road", "Machilipatnam PS", "Local Market", 4.7],

    # Tenali
    ["Tenali", "Guntur", "Vykuntapuram", 16.2333, 80.5833, "Vykuntapuram Venkateswara Temple", "Often called the Mini Tirumala of Tenali region.", "Tenali Lodge", 4.9, "Town center", "Rama Tiffins", 4.7, "Junction", "Pure Veg", "Nearby", "Budget", "Guntur Road", "Main Road", "Tenali PS", "Local Market", 4.9],
    ["Tenali", "Guntur", "Paatha Sivalayam", 16.2417, 80.5833, "Sri Rameswara Swamy Temple", "An ancient Shiva temple with rich spiritual history in Tenali town.", "Hotel Amaravathi", 4.8, "Town Road", "Siva Meals", 4.6, "Entrance", "Traditional", "Nearby", "Budget", "Bridge Road", "Main Bazar", "Tenali PS", "Market Area", 4.8],

    # Kakinada
    ["Kakinada", "Kakinada", "Sarpavaram", 16.9833, 82.2333, "Sarpavaram Sri Bhavannarayana Swamy", "Ancient temple dedicated to Lord Vishnu, known for its architectural beauty.", "Royal Park", 4.8, "Kakinada Road", "Bhavan Meals", 4.6, "Junction", "Traditional", "Nearby", "Premium", "Town Road", "Main Road", "Kakinada PS", "Market", 4.8],
    ["Kakinada", "Kakinada", "Samalkot", 17.0500, 82.1667, "Kumararama Bhimeswara Swamy Temple", "One of the Pancharama Kshetras, a massive temple with majestic architecture.", "Samalkot Lodge", 5.0, "Temple Entrance", "Giri Tiffins", 4.8, "Junction", "Pure Veg", "Nearby", "Budget", "Railway Station", "Main Road", "Samalkot PS", "Local Market", 5.0],

    # Bhimavaram
    ["Bhimavaram", "West Godavari", "Gunupudi", 16.5333, 81.5333, "Sri Someswara Swamy Temple", "A major pilgrim center and one of the Pancharama Kshetras.", "Bhimavaram Hotel", 5.0, "Gunupudi", "Soma Tiffins", 4.8, "Junction", "Traditional", "Nearby", "Budget", "Main Bazar", "Station Road", "Bhimavaram PS", "Local Market", 5.0],

    # Chittoor
    ["Chittoor", "Chittoor", "Town Center", 13.2167, 79.1000, "Gangamma Temple Chittoor", "Ancient temple of Goddess Gangamma, famous for the annual Jathara.", "Chittoor Hotel", 4.8, "Bus Stand", "Ganga Cafe", 4.6, "Entrance", "Snacks", "Nearby", "Budget", "Main Bazar", "Highway side", "Chittoor PS", "Market Area", 4.8],

    # Proddatur
    ["Proddatur", "Kadapa", "Mukthi Rameswaram", 14.7333, 78.5500, "Mukthi Rameswaram Temple", "One of the oldest Shiva temples in Proddatur, believed to have a lingam installed by Lord Rama.", "Hotel Sree Surya", 4.9, "Old Market", "Rameswar Meals", 4.7, "Temple Entrance", "Traditional", "Main Road", "Budget", "Station Road", "Old Town", "Proddatur PS", "Old Market Area", 4.9],
    ["Proddatur", "Kadapa", "Bollavaram", 14.7500, 78.5667, "Bollavaram Venkateswara Temple", "A highly popular local temple dedicated to Lord Venkateswara.", "Victory Residency", 4.8, "Bollavaram", "Bolla Cafe", 4.6, "Temple Jct", "Tiffins", "Nearby", "Budget", "Jammalamadugu Rd", "Main Road", "Proddatur PS", "Local Market", 4.8],

    # Guntakal & Anantapur region
    ["Guntakal", "Anantapur", "Kasapuram", 15.1667, 77.3833, "Nettikanti Anjaneya Swamy Temple", "A very famous 15th-century Hanuman temple established by Sri Vyasaraja.", "Guntakal Lodge", 5.0, "Railway Station", "Hanuma Meals", 4.8, "Temple Entrance", "Traditional", "Town center", "Budget", "Highway Jct", "Station Road", "Guntakal PS", "Tempo Stand", 5.0],
    ["Dharmavaram", "Anantapur", "City Center", 14.4167, 77.7167, "Lakshmi Chennakesava Swamy Temple", "Ancient temple known for its Vijayanagara-style architecture and beautiful stone carvings.", "Dharmavaram Hotel", 4.8, "Railway Station", "Chenna Kitchen", 4.6, "Temple Jct", "Meals", "Nearby", "Saree Market", "Main Road", "Railway Station", "Dharmavaram PS", "Saree Market", 4.8],

    # Tadipatri
    ["Tadipatri", "Anantapur", "Pennar Banks", 14.9167, 78.0167, "Bugga Ramalingeswara Swamy Temple", "Stunning 16th-century Shiva temple famous for its exquisite stone carvings and natural spring.", "Tadipatri Lodge", 5.0, "Town center", "Hill Side", 4.8, "Temple Entrance", "Traditional", "Nearby", "Budget", "Main Bazar", "Main Road", "Tadipatri PS", "Market Area", 5.0],
    ["Tadipatri", "Anantapur", "Town area", 14.9189, 78.0189, "Chintala Venkataramana Swamy Temple", "Famous 16th-century Vaishnavite temple with architecture similar to Hampi.", "Nearby Hotel", 4.9, "Main Road", "Venkata Meals", 4.7, "Junction", "Pure Veg", "Nearby", "Budget", "Main Bazar", "Station Road", "Tadipatri PS", "Local Market", 4.9],

    # Bapatla & Narasaraopet
    ["Bapatla", "Bapatla", "City center", 15.9000, 80.4667, "Bapatla Bhavanarayana Swamy Temple", "Ancient 1,500-year-old temple said to be the source of the town's name.", "Hotel Geetha", 4.9, "Railway Station", "Bhavan Cafe", 4.7, "Junction", "Tiffins", "Nearby", "Budget", "Main Bazar", "Market Street", "Bapatla PS", "Market Area", 4.9],
    ["Narasaraopet", "Palnadu", "City center", 16.2333, 80.0500, "Narasaraopet Bhavanarayana Swamy", "Historic temple dedicated to Bhavanarayana Swamy, a significant regional shrine.", "Narasaraopet Hotel", 4.8, "Bus Stand", "Temple Kitchen", 4.6, "Entrance", "Meals", "Nearby", "Budget", "Guntur Road", "Main Road", "Narasaraopet PS", "Local Market", 4.8],

    # Gudur & Kavali
    ["Gudur", "Nellore", "GT Road", 14.1500, 79.8500, "Alaganatha Swamy Temple Gudur", "The largest temple in Gudur, built during the Chola Dynasty.", "Gudur Lodge", 4.8, "Railway Station", "Alagan Kitchen", 4.6, "Entrance", "Traditional", "Nearby", "Budget", "GT Road", "Main Market", "Gudur PS", "Main Bazar", 4.8],
    ["Kavali", "Nellore", "GT Road", 14.9167, 79.9833, "Pattabhi Ramaswamy Temple Kavali", "Highly revered temple dedicated to Lord Rama, central to the town's identity.", "Kavali Hotel", 4.9, "Bus Stand", "Rama Kitchen", 4.7, "Junction", "Pure Veg", "Nearby", "Budget", "GT Road", "Main Road", "Kavali PS", "Market Area", 4.9],

    # Rayachoti
    ["Rayachoti", "Annamayya", "GT Road", 14.0500, 78.7500, "Veerabhadra Swamy Temple Rayachoti", "A historic 1,000-year-old temple known as Dakshina Kasi with a massive Deepa Sthambham.", "Rayachoti Lodge", 5.0, "Town center", "Dakshina Cafe", 4.9, "Junction", "Traditional", "Nearby", "Budget", "GT Road", "Main Road", "Rayachoti PS", "Market", 5.0],

    # Tanuku & Tadepalligudem
    ["Tanuku", "West Godavari", "River Road", 16.7500, 81.7167, "Kapardeswara Swamy Temple", "A major religious site in Tanuku known for its peaceful atmosphere.", "Hotel Surya", 4.8, "Town center", "Siva Kitchen", 4.6, "Junction", "Traditional", "Nearby", "Budget", "Main Bazar", "Main Road", "Tanuku PS", "Market Area", 4.8],
    ["Tadepalligudem", "West Godavari", "City Center", 16.8333, 81.5000, "Bhramaramba Mallikharjuna Swamy", "Significant temple dedicated to Lord Shiva in Tadepalligudem town.", "Tadepalligudem Hotel", 4.8, "Hihway", "Mallikarjuna Cafe", 4.6, "Junction", "Meals", "Nearby", "Budget", "Railway Road", "Main Road", "Tadepalligudem PS", "Local Market", 4.8],

    # Amalapuram area
    ["Amalapuram", "Konaseema", "Ainavilli", 16.5833, 82.0000, "Ainavilli Siddhi Vinayaka Temple", "A globally famous temple for Lord Ganesha, located in the scenic Konaseema.", "Amalapuram Lodge", 5.0, "Amalapuram Road", "Vinayaka Tiffins", 4.9, "Entrance", "Pure Veg", "Nearby", "Budget", "Highway Jct", "Main Road", "Amalapuram PS", "Konaseema Market", 5.0],
    ["Amalapuram", "Konaseema", "Appanapalli", 16.5167, 81.8500, "Appanapalli Sri Balaji Temple", "A highly revered temple of Lord Venkateswara in the Konaseema region.", "Punnami Resorts", 4.9, "Appanapalli", "Balaji Kitchen", 4.7, "Junction", "Traditional", "Nearby", "Resort", "Amalapuram Road", "Konaseema", "Amalapuram PS", "Local Area", 4.9],

    # Chittoor extra
    ["Chittoor", "Chittoor", "Kanipakam", 13.2500, 79.1500, "Kanipakam Varasiddhi Vinayaka Temple", "Self-manifested Ganesha temple known for the legend of the growing idol in a well.", "Kanipakam Lodge", 5.0, "Temple Entrance", "Ganesha Meals", 5.0, "Junction", "Pure Veg", "Nearby", "Budget", "Chittoor Road", "Highway", "Kanipakam PS", "Temple Market", 5.0],
]

# Prepare to add
to_add = []
for spot in temple_data:
    key = get_clean_key(spot[5])
    if key not in existing_keys:
        row_dict = {}
        for i, col in enumerate(df.columns[:21]):
            row_dict[col] = spot[i]
        
        row_dict['Entry_Fee'] = "Free"
        row_dict['Rating'] = spot[20]
        row_dict['Final_Rating'] = spot[20]
        row_dict['Hotel'] = row_dict.get('Nearby_Hotel_Name', 'N/A')
        
        to_add.append(row_dict)

if not to_add:
    print("No new unique temples found to add.")
else:
    new_df = pd.DataFrame(to_add)
    final_df = pd.concat([df, new_df], ignore_index=True)
    final_df.to_csv(csv_path, index=False)
    print(f"Successfully added {len(to_add)} unique exhaustive temple locations across AP.")
