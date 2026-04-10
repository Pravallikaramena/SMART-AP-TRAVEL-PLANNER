import pandas as pd
import os

csv_path = r'datasets\AP_DATASET.CSV'

if not os.path.exists(csv_path):
    print(f"Error: {csv_path} not found.")
    exit(1)

# Load existing dataset
df = pd.read_csv(csv_path)

# Ensure Entry_Fee column exists
if 'Entry_Fee' not in df.columns:
    df['Entry_Fee'] = "N/A"

# Normalize names for duplicate checking
def get_clean_key(name):
    s = str(name).lower()
    mapping = {
        "simhachalam": "simhachalam_temple", 
        "varaha lakshmi narasimha": "simhachalam_temple",
        "kanaka durga": "kanaka_durga_temple",
        "venkateswaraswamy": "tirumala_temple",
        "tirumala": "tirumala_temple"
    }
    for k, v in mapping.items():
        if k in s: return v
    return "".join(s.split())

# Get existing keys for all cities to prevent duplicates
existing_keys = set(df['Tourist_Place'].apply(get_clean_key))

# Curated Famous Places across Andhra Pradesh
# Format: [City, District, Area, Lat, Lon, Name, Description, Hotel, Rating, NearbyHotel, NearbyRestaurant, RatingRest, RestLoc, RestType, HotelLoc, HotelType, RestLoc2, HotelLoc2, PS, Shop, FinalRating]
famous_spots = [
    # Vijayawada
    ["Vijayawada", "NTR", "Indrakeeladri", 16.5189, 80.6214, "Kanaka Durga Temple", "One of the most famous Shakti Peethas in India, located on a hill overlooking the Krishna River.", "Hotel Fortune Murali Park", 5.0, "Indrakeeladri Road", "RR Durbar", 4.8, "Besant Road", "Multi-Cuisine", "MG Road", "Premium", "Governorpet", "MG Road", "Two Town PS", "Besant Road Market", 5.0],
    ["Vijayawada", "NTR", "Krishna River", 16.5264, 80.5697, "Bhavani Island", "One of the largest river islands in India, offering water sports and scenic views.", "Bhavani Island Resort", 4.8, "Prakasam Barrage", "Riverside Cafe", 4.5, "Island Entrance", "Snacks", "Riverside", "Resort", "MG Road", "MG Road", "One Town PS", "Prakasam Barrage", 4.8],
    ["Vijayawada", "Guntur (Nearby)", "Undavalli", 16.4958, 80.5842, "Undavalli Caves", "Monolithic rock-cut caves that are a fine example of Indian rock-cut architecture.", "Hotel Manorama", 4.7, "Undavalli Road", "Caves Food Court", 4.4, "Caves Junction", "Meals", "Nearby", "Budget", "Vijayawada Road", "Vijayawada Road", "Tadepalli PS", "Temple Street", 4.7],
    ["Vijayawada", "NTR", "Seetharampuram", 16.5217, 80.6211, "Rajiv Gandhi Park", "A well-maintained urban park with musical fountains and children attractions.", "The Gateway Hotel", 4.6, "MG Road", "Park View Restaurant", 4.3, "Entrance", "Snacks", "Nearby", "Premium", "Governorpet", "MG Road", "Three Town PS", "Besant Road", 4.6],
    
    # Tirupati
    ["Tirupati", "Tirupati", "Tirumala Hills", 13.6831, 79.3472, "Venkateswara Swamy Temple", "The richest temple in the world, dedicated to Lord Venkateswara (Lord Vishnu).", "Fortune Select Grand Ridge", 5.0, "Tirumala Hill", "Annaprasadam Hall", 5.0, "Tirumala", "Pure Veg", "Tirumala Hills", "Pilgrim", "Tirupati Road", "Tirupati Town", "Tirumala PS", "TTD Market", 5.0],
    ["Tirupati", "Tirupati", "Zoo Road", 13.6267, 79.3517, "Venkateswara Zoological Park", "One of the largest zoological parks in Asia, famous for its lion safaris.", "Hotel Bliss", 4.8, "KT Road", "Zoo Canteen", 4.5, "Zoo Entrance", "Snacks", "Zoo Road", "Budget", "Alipiri Road", "Kapila Theertham", "Alipiri PS", "Alipiri Market", 4.8],
    ["Tirupati", "Tirupati", "Alipiri", 13.6494, 79.4089, "ISKCON Temple Tirupati", "A beautiful Radha Krishna temple known for its peaceful atmosphere.", "Hotel Marasa Sarovar Premiere", 4.9, "Alipiri Road", "Govinda Restaurant", 4.8, "Iskcon Campus", "Pure Veg", "Nearby", "Premium", "KT Road", "Kapila Theertham", "Alipiri PS", "Alipiri Market", 4.9],
    ["Tirupati", "Tirupati", "Eswar Nagar", 13.6467, 79.4180, "Kapila Theertham Waterfalls", "A sacred waterfall and temple dedicated to Lord Shiva in the foothills of Tirumala.", "Hotel Minerva Grand", 4.7, "Kapila Theertham", "Temple Meals", 4.5, "Hill Entrance", "Tiffins", "Hill Side", "Premium", "Alipiri Road", "KT Road", "Alipiri PS", "Temple Market", 4.7],
    
    # Rajahmundry
    ["Rajahmundry", "East Godavari", "Godavari Banks", 17.0067, 81.7700, "ISKCON Rajahmundry", "Largest ISKCON temple in Andhra Pradesh, located on the banks of Godavari river.", "Hotel River Bay", 4.9, "Riverside Road", "Govindas", 4.8, "Iskcon Campus", "Pure Veg", "Riverside", "Resort", "Main Road", "Pushkar Ghat", "Three Town PS", "Main Market", 4.9],
    ["Rajahmundry", "East Godavari", "River Road", 17.0067, 81.7700, "Pushkar Ghat", "A sacred place on the banks of Godavari river where Godavari Pushkaralu are held.", "Akash Ganga Hotel", 4.8, "Pushkar Ghat", "Ghat Food", 4.6, "Ghat Entrance", "Snacks", "River Road", "Budget", "Main Market", "Godavari Banks", "One Town PS", "Main Market", 4.8],
    ["Rajahmundry", "East Godavari", "Godavari River", 16.9200, 81.7800, "Papi Hills Boat Point", "Scenic boat ride through the lush Papi Hills on the Godavari river.", "Papi Hills Resort", 5.0, "Godavari Front", "Cruise Meals", 4.7, "On Board", "Traditional", "River Port", "Resort", "Bhadrachalam Road", "Godavari Banks", "Rajahmundry PS", "River Market", 5.0],
    ["Rajahmundry", "East Godavari", "Airport Road", 17.0125, 81.7850, "Happy Street Glow Garden", "A vibrant park with illuminations and family recreation areas.", "Grand Kakinada Reliance", 4.7, "Airport Road", "Happy Cafe", 4.5, "Park Entrance", "Snacks", "Nearby", "Budget", "Main Road", "Airport Road", "Airport PS", "Airport Area", 4.7],

    # Guntur
    ["Guntur", "Guntur", "Sannidhanam", 16.2736, 80.0531, "Kotappakonda Hill Temple", "A major pilgrim center dedicated to Lord Shiva, famous for its hill climb and annual fair.", "Hotel Sree Lakshmi", 4.8, "Kotappakonda Road", "Hillside Meals", 4.5, "Hill Entrance", "Tiffins", "Hill Side", "Budget", "Narasaraopet Road", "Narasaraopet", "Narasaraopet PS", "Temple Market", 4.8],
    ["Guntur", "Guntur", "Amaravati", 16.5753, 80.3581, "Amaravati Buddhist Stupa", "The Great Stupa, one of the most important Buddhist monuments in the world.", "Amaravati Hotel", 4.7, "Stupa Road", "Stupa Cafe", 4.4, "Museum Jct", "Snacks", "Nearby", "Lodge", "River Road", "Amaravati Entrance", "Amaravati PS", "Local Market", 4.7],
    ["Guntur", "Guntur", "Mangalagiri", 16.4386, 80.5606, "Mangalagiri Lakshmi Narasimha Temple", "Famous temple for God Panakala Narasimha Swamy, where jaggery water is offered.", "Mangalagiri Lodge", 4.9, "Temple Hill", "Giri Tiffins", 4.7, "Hilltop Entrance", "Traditonal", "Hill Base", "Budget", "Highway Jct", "Guntur Road", "Mangalagiri PS", "Handloom Market", 4.9],
    ["Guntur", "Guntur", "Uppalapadu", 16.2625, 80.4417, "Uppalapadu Bird Sanctuary", "Home to many rare bird species, especially painting storks and pelicans.", "Hotel Swagath", 4.7, "Uppalapadu", "Eco Picnic", 4.5, "Lake Area", "Snacks", "Nearby", "Budget", "Guntur Road", "Main Road", "Pedda Kakani PS", "Local Market", 4.7],

    # Kurnool
    ["Kurnool", "Kurnool", "City Center", 15.8283, 78.0333, "Konda Reddy Fort", "A massive historical fortification in the heart of Kurnool city.", "Mourya Inn", 4.8, "Fort Road", "Fort Dhaba", 4.4, "Fort Entrance", "Meals", "Nearby", "Premium", "Old Town", "Park Road", "Two Town PS", "Main Bazar", 4.8],
    ["Kurnool", "Nandyal", "Belum", 15.1022, 78.1114, "Belum Caves", "Longest cave system in the plains of India, known for stalactite and stalagmite formations.", "Belum Resort (Haritha)", 5.0, "Caves Entrance", "Belum Cafe", 4.5, "Cave Entrance", "Snacks", "Cave Entrance", "AP Tourism", "Banaganapalle Road", "Banaganapalle", "Banaganapalle PS", "Local Market", 5.0],
    ["Kurnool", "Nandyal", "Yaganti", 15.3500, 78.1400, "Yaganti Temple", "A beautiful Shiva temple famous for the growing Nandi statue and natural stone caves.", "Yaganti Lodge", 4.9, "Temple Entrance", "Giri Tiffins", 4.6, "Temple Jct", "Traditional", "Nearby", "Budget", "Banaganapalle Rd", "Nandyal Highway", "Banaganapalle PS", "Temple Market", 4.9],
    ["Kurnool", "Nandyal", "Mahanandi", 15.4744, 78.6253, "Mahanandi Temple", "An ancient Shiva temple with nine sacred Nandi shrines and natural water tanks.", "Mahanandi Hotel", 4.9, "Temple Road", "Nandi Meals", 4.7, "Entrance", "Pure Veg", "Nearby", "Budget", "Nandyal Road", "Nandyal Highway", "Mahanandi PS", "Temple Market", 4.9],

    # Kadapa
    ["Kadapa", "Kadapa", "Gandikota", 14.8147, 78.2867, "Gandikota Grand Canyon", "Stunning gorge and canyon formed by the Penna River, alongside a historic fort.", "Haritha Gandikota", 5.0, "Fort Entrance", "Canyon Cafe", 4.6, "Entrance", "Snacks", "Fort Area", "AP Tourism", "Jammalamadugu Road", "Jammalamadugu", "Jammalamadugu PS", "Local Market", 5.0],
    ["Kadapa", "Kadapa", "Vontimitta", 14.3917, 78.9667, "Vontimitta Kodandarama Temple", "A massive 16th-century temple known for spectacular architecture and Ramalingeswara Swamy.", "Vontimitta Lodge", 4.8, "Temple Entrance", "Rama Tiffins", 4.5, "Temple Jct", "Traditional", "Nearby", "Budget", "Kadapa Road", "Kadapa Highway", "Vontimitta PS", "Market Area", 4.8],
    ["Kadapa", "Kadapa", "Rayachoti Road", 14.4758, 78.8258, "Gandi Veeranjaneya Temple", "Sacred temple of Hanuman on the banks of Papaghni river.", "Kadapa Lodge", 4.7, "Rayachoti Road", "Gandi Kitchen", 4.4, "Junction", "Meals", "Nearby", "Budget", "Kadapa Road", "Highway Side", "Gandi PS", "Local Market", 4.7],

    # Nellore
    ["Nellore", "Nellore", "Penna River", 14.4500, 79.9833, "Talpagiri Ranganathaswamy Temple", "One of the oldest temples in Nellore, dedicated to Lord Vishnu on the banks of Penna River.", "Hotel Minerva Grand", 4.8, "Bara Shaheed Dargah", "Penna Spice", 4.6, "Main Road", "Multi-Cuisine", "Nearby", "Premium", "GT Road", "Pogathota", "One Town PS", "Pogathota Market", 4.8],
    ["Nellore", "Nellore", "Mypadu", 14.5000, 80.1833, "Mypadu Beach", "A serene beach with golden sands and a calm sea, perfect for evening relaxations.", "Haritha Mypadu", 4.7, "Beach Road", "Shoreline Cafe", 4.4, "Beachfront", "Seafood", "Beach Area", "AP Tourism", "Nellore Road", "Nellore Town", "Indukurpet PS", "Beach Shacks", 4.7],
    ["Nellore", "Nellore", "Pulicat Lake", 13.8833, 80.1833, "Pulicat Lake Bird Sanctuary", "A paradise for birdwatchers, especially famous for flamingos.", "Sullurupeta Lodge", 4.8, "Flamingo Road", "Bird Point Cafe", 4.6, "Sullurupeta", "Snacks", "Nearby", "Budget", "SHAR Road", "Highway Jct", "Sullurupeta PS", "Highway Market", 4.8],

    # Srisailam
    ["Srisailam", "Nandyal", "Nallamala Hills", 16.0742, 78.8681, "Mallikarjuna Swamy Temple", "A Jyotirlinga temple of Lord Shiva and one of the 18 Shakti Peethas.", "Punnami Srisailam", 5.0, "Temple Road", "Bhramaramba Food", 4.9, "Entrance", "Pure Veg", "Temple Area", "AP Tourism", "Dornala Road", "Dornala", "Srisailam PS", "Temple Market", 5.0],
    ["Srisailam", "Nandyal", "Srisailam Dam", 16.0886, 78.9025, "Srisailam Dam ViewPoint", "Breath-taking views of the second largest hydroelectric project in India.", "Haritha Resort", 4.9, "Dam Road", "Dam View Cafe", 4.7, "Dam Entrance", "Snacks", "Nearby", "AP Tourism", "Main Road", "Temple Area", "Srisailam PS", "Dam Area", 4.9],
    ["Srisailam", "Nandyal", "Nallamala hills", 16.1264, 78.8083, "Nagarjuna Sagar Srisailam Tiger Reserve", "The largest Tiger Reserve in India, spread across five districts.", "Tribal Lodge", 4.8, "Entrance Gate", "Forest Kitchen", 4.6, "Gate Jct", "Traditional", "Nearby", "Wildlife Lounge", "Main Highway", "Dornala Road", "Atmakur PS", "Forest Area", 4.8],

    # Anantapur
    ["Anantapur", "Sri Sathya Sai", "Lepakshi", 13.8033, 77.8089, "Veerabhadra Temple Lepakshi", "Marvelous 16th century architecture with a huge Nandi statue and hanging pillar.", "Lepakshi Lodge", 5.0, "Temple Entrance", "Giri Tiffins", 4.7, "Junction", "Traditional", "Nearby", "Budget", "Hindupur Road", "Hindupur", "Lepakshi PS", "Temple Market", 5.0],
    ["Anantapur", "Sri Sathya Sai", "Puttaparthi", 14.1667, 77.8167, "Prasanthi Nilayam (Puttaparthi)", "The spiritual hub and main ashram of Sri Sathya Sai Baba.", "Sai Towers", 4.9, "Main Road", "Sai Annapurna", 4.8, "Ashram Campus", "Pure Veg", "Nearby", "Premium", "Prasanthi Jct", "Main Road", "Puttaparthi PS", "Sai Market", 4.9],
    ["Anantapur", "Anantapur", "Gooty", 15.1189, 77.6347, "Gooty Fort", "Ancient shell-shaped fortification set atop a majestic hill, overlooking the town.", "Gooty Lodge", 4.7, "Fort Road", "Highway Dhaba", 4.5, "Fort Entrance", "Meals", "Nearby", "Budget", "Highway Jct", "Gooty Town", "Gooty PS", "Main Bazar", 4.7],

    # Srikakulam
    ["Srikakulam", "Srikakulam", "Arasavalli", 18.2881, 83.9136, "Arasavalli Sun Temple", "A major ancient sun temple of Andhra Pradesh, built by Kalinga kings.", "Hotel Sree Sreenivasa", 4.9, "Arasavalli Road", "Surya Tiffins", 4.7, "Temple Entrance", "Pure Veg", "Nearby", "Premium", "Srikakulam Town", "GT Road", "Srikakulam PS", "Main Bazar", 4.9],
    ["Srikakulam", "Srikakulam", "Sri Kurmam", 18.2831, 84.0136, "Sri Kurmanatha Swamy Temple", "The only temple in the world dedicated to Kurma (tortoise) avatar of Vishnu.", "Lodge Srinivas", 4.8, "Temple Entrace", "Kurma Meals", 4.6, "Nearby", "Pure Veg", "Temple Jct", "Budget", "Srikakulam Road", "Srikakulam", "Srikakulam PS", "Local Market", 4.8],
    ["Srikakulam", "Srikakulam", "Kalingapatnam", 18.3125, 84.1167, "Kalingapatnam Beach", "A lovely beach and lighthouse at the confluence of Vamsadhara river and Bay of Bengal.", "Haritha Kalingapatnam", 4.7, "Beach Road", "Harbour View", 4.5, "Beachfront", "Seafood", "Nearby", "AP Tourism", "Srikakulam Road", "Srikakulam", "Srikakulam PS", "Beach Shacks", 4.7],

    # Kakinada
    ["Kakinada", "Kakinada", "Coringa", 16.8314, 82.3367, "Coringa Wildlife Sanctuary", "Second largest mangrove forest in India with a unique eco-system.", "Kakinada Hotel Royal Park", 4.8, "Beach Road", "Coringa Kitchen", 4.6, "Sanctuary Entrance", "Snacks", "Nearby", "Premium", "Town Road", "Harbour Area", "Kakinada PS", "Kakinada Market", 4.8],
    ["Kakinada", "Kakinada", "Uppada", 17.1000, 82.3333, "Uppada Beach", "Known for its beautiful coastline and traditional Uppada Jamdani sarees.", "Sea Shore Resort", 4.7, "Beach Road", "Shell Shack", 4.5, "Beachfront", "Seafood", "Beach Area", "Resort", "Kakinada Road", "Main Road", "Kakinada PS", "Saree Market", 4.7],
    ["Kakinada", "Kakinada", "Draksharamam", 16.7831, 82.0667, "Draksharamam Temple", "One of the Pancharama Kshetras, housing an 8ft tall crystal Shiva Lingam.", "Temple Lodge", 4.9, "Temple Entrance", "Lodge Meals", 4.7, "Nearby", "Traditional", "Nearby", "Budget", "Kakinada Road", "Ramachandrapuram", "Ramachandrapuram PS", "Temple Market", 4.9],

    # Vizianagaram
    ["Vizianagaram", "Vizianagaram", "City Center", 18.1125, 83.4111, "Ramanarayanam Temple", "A world-class spiritual center depicting the entire Ramayana in sculptural detail.", "Hotel Sunray", 5.0, "Highway Road", "Rama Cafe", 4.9, "Temple Campus", "Pure Veg", "Nearby", "Premium", "Railway Road", "RTC Complex", "Vizianagaram PS", "Main Bazar", 5.0],
    ["Vizianagaram", "Vizianagaram", "Fort area", 18.1189, 83.4022, "Vizianagaram Fort", "Historic fort with majestic entrance gates and rich cultural structures.", "Hotel Mayura", 4.7, "Fort Road", "Fort Dhaba", 4.4, "Fort Jct", "Meals", "Nearby", "Budget", "Main Market", "RTC Complex", "Vizianagaram PS", "Main Bazar", 4.7],
    ["Vizianagaram", "Vizianagaram", "Pydithalli", 18.1067, 83.3967, "Pydithalli Ammavari Temple", "Highly revered temple of Goddess Pydithalli, especially during Sirimanu Utsav.", "Temple Lodge", 4.8, "Temple Entrace", "Annapurna", 4.6, "Main Road", "Tiffins", "Nearby", "Budget", "Market Road", "Railway Station", "Vizianagaram PS", "Market Area", 4.8],

    # Amaravati
    ["Amaravati", "Guntur", "Buddha Statue", 16.5753, 80.3581, "Dhyana Buddha Statue", "A massive 125ft tall statue of Lord Buddha in Amaravati overlooking the Krishna River.", "Hotel Riverview", 5.0, "Statue Road", "Buddha Cafe", 4.7, "Garden Entrance", "Snacks", "Riverfront", "Lodge", "Amaravati Jct", "Guntur Road", "Amaravati PS", "Local Market", 5.0],

    # Annavaram
    ["Annavaram", "Kakinada", "Ratnagiri Hill", 17.2833, 82.4000, "Satyanarayana Swamy Temple", "Major holy hill pilgrim center where Sri Satyanarayana Swamy Vratams are famous.", "Haritha Annavaram", 5.0, "Hillside Road", "Temple Prasadam", 5.0, "Hilltop", "Traditional", "Hill Base", "AP Tourism", "Highway Jct", "Main Road", "Annavaram PS", "Hill Market", 5.0],

    # Antarvedi
    ["Antarvedi", "Konaseema", "Beach road", 16.3267, 81.7267, "Antarvedi Lakshmi Narasimha Temple", "Located at the confluence of Vashista Godavari and the Bay of Bengal.", "Antarvedi Lodge", 4.9, "Temple Road", "Confluence Kitchen", 4.7, "Temple Entrance", "Tiffins", "Nearby", "Lodge", "Beach Road", "Godavari Banks", "Antarvedi PS", "Temple Market", 4.9],

    # Dwaraka Tirumala
    # Dwaraka Tirumala
    ["Dwaraka Tirumala", "Eluru", "Hill area", 16.9458, 81.2583, "Venkateswara Swamy Temple (Chinna Tirupati)", "Highly popular sacred hill temple of Lord Venkateswara in Eluru district.", "Dwaraka Lodge", 4.9, "Hill Base", "Giri Tiffins", 4.7, "Hill Entrance", "Pure Veg", "Nearby", "Budget", "Eluru Road", "Main Road", "Dwaraka Tirumala PS", "Temple Market", 4.9],

    # Machilipatnam
    ["Machilipatnam", "Krishna", "Beach area", 16.1417, 81.2167, "Manginapudi Beach", "Known for its unique black soil and historic port, ideal for swimming and evening relaxation.", "Riva Resorts", 4.7, "Beach Road", "Shoreline Cafe", 4.5, "Beachfront", "Seafood", "Nearby", "Budget", "Koneru Centre", "Main Road", "Inuguduru PS", "Beach Shacks", 4.7],
    ["Machilipatnam", "Krishna", "Koneru Centre", 16.1833, 81.1333, "Panduranga Swamy Temple", "A major pilgrim center with a beautiful temple dedicated to Lord Krishna.", "Hotel Jaya", 4.9, "Koneru Centre", "Gopala Tiffins", 4.7, "Entrance", "Pure Veg", "Nearby", "Budget", "Main Bazar", "Main Road", "Chilakalapudi PS", "Market Road", 4.9],

    # Ongole
    ["Ongole", "Prakasam", "Kothapatnam Beach", 15.4333, 80.1500, "Kothapatnam Beach", "A popular beach famous for its scenic beauty and clean sands.", "Hotel Sree Surya", 4.6, "Highway", "Beach Spices", 4.4, "Beachfront", "Meals", "Nearby", "Lodge", "Ongole Town", "GT Road", "Ongole PS", "Local Market", 4.6],
    ["Ongole", "Prakasam", "GT Road", 15.5000, 80.0500, "Chennakesava Swamy Temple", "An ancient temple dedicated to Lord Vishnu, built during the Vijayanagara empire.", "Hotel Mourya", 4.8, "GT Road", "Chenna Meals", 4.6, "Entrance", "Pure Veg", "Nearby", "Budget", "Main Bazar", "Main Road", "Ongole II PS", "Main Market", 4.8],

    # Eluru
    ["Eluru", "Eluru", "Kolleru", 16.6333, 81.2000, "Kolleru Lake Bird Sanctuary", "One of the largest freshwater lakes in India, home to migrating birds.", "Hotel Sreshti", 4.7, "Highway", "Bird Point Cafe", 4.5, "Lake Entrance", "Snacks", "Nearby", "Budget", "Eluru Town", "Highway Jct", "Eluru PS", "Local Market", 4.7],
    ["Eluru", "Eluru", "City Center", 16.7111, 81.1028, "Eluru Buddha Park", "Centered around a large Buddha statue, this park is a major local attraction.", "Hotel Adithya", 4.8, "GNT Road", "Park Cafe", 4.6, "Entrance", "Tiffins", "Nearby", "Budget", "Main Bazar", "Station Road", "Eluru I PS", "Main Market", 4.8],

    # Chittoor
    ["Chittoor", "Chittoor", "Horsley Hills", 13.6500, 78.4000, "Horsley Hills Station", "The scenic hll station of Andhra Pradesh, famous for its cool climate.", "Haritha Hill Resort", 4.9, "Hilltop", "Hill View Restaurant", 4.8, "Entrance", "Multi-Cuisine", "Nearby", "AP Tourism", "Hill Base", "Madanapalle Road", "Madanapalle PS", "Hill Market", 4.9],
    ["Chittoor", "Chittoor", "Kanipakam", 13.2500, 79.0167, "Kanipakam Vinayaka Temple", "Self-manifested Ganesha temple known for the legend of the growing idol.", "Kanipakam Lodge", 5.0, "Temple Entrance", "Ganesha Meals", 4.8, "Junction", "Pure Veg", "Nearby", "Budget", "Chittoor Road", "Chittoor Highway", "Kanipakam PS", "Temple Market", 5.0],
    ["Chittoor", "Chittoor", "Talakona", 13.7833, 79.2167, "Talakona Waterfalls", "Highest waterfall in Andhra Pradesh, located within the national park.", "Forest Log Hut", 4.9, "Entrance Gate", "Forest Cafe", 4.7, "Junction", "Traditional", "Nearby", "Log Huts", "Bakrapet Road", "Tirupati Highway", "Bakrapet PS", "Local Market", 4.9],

    # Nandyal
    ["Nandyal", "Nandyal", "Rollapadu", 15.7333, 78.3667, "Rollapadu Wildlife Sanctuary", "A sanctuary known for the protection of the Great Indian Bustard.", "Rollapadu Lodge", 4.8, "Sanctuary Road", "Grasslands Cafe", 4.6, "Sanctuary", "Snacks", "Nearby", "Budget", "Nandyal Road", "Highway Side", "Nandyal PS", "Local Market", 4.8],

    # Adoni
    ["Adoni", "Kurnool", "Fort Area", 15.6333, 77.2833, "Adoni Fort", "An ancient impregnable fortification with huge stone walls.", "Adoni Hotel", 4.7, "Fort Road", "Fort Dhaba", 4.5, "Fort Jct", "Meals", "Nearby", "Lodge", "Main Bazar", "Town Road", "Adoni PS", "Market Area", 4.7],
]

# Add more generic famous places that can apply as big parks or landmarks in many cities
common_types = ["Central Park", "Urban Garden", "Historical Fort Ruins", "Museum"]

# Prepare to add
to_add = []
for spot in famous_spots:
    key = get_clean_key(spot[5])
    if key not in existing_keys:
        # Check if the row has at least 21 columns (initial df was 21)
        # Our famous_spots rows have 21 elements
        row_dict = {}
        for i, col in enumerate(df.columns[:21]):
            row_dict[col] = spot[i]
        
        # Add Entry_Fee and other columns
        name = str(spot[5])
        temple_keywords = ["Temple", "Mosque", "Church", "Dargah", "ISKCON", "Saranam", "Satyanarayana", "Venkateswara", "Narasimha", "Lord"]
        if any(k in name for k in temple_keywords):
            row_dict['Entry_Fee'] = "Free"
        elif "Park" in name or "Garden" in name or "Zoo" in name:
            row_dict['Entry_Fee'] = "₹50 - ₹100"
        elif "Cave" in name or "Fort" in name or "Museum" in name:
            row_dict['Entry_Fee'] = "₹20 - ₹50"
        else:
            row_dict['Entry_Fee'] = "Free"
            
        row_dict['Rating'] = spot[20] # The 21st element
        row_dict['Final_Rating'] = spot[20]
        row_dict['Hotel'] = row_dict.get('Nearby_Hotel_Name', 'N/A')
        
        to_add.append(row_dict)

if not to_add:
    print("No new unique famous places found to add.")
else:
    new_df = pd.DataFrame(to_add)
    final_df = pd.concat([df, new_df], ignore_index=True)
    final_df.to_csv(csv_path, index=False)
    print(f"Successfully added {len(to_add)} unique famous locations across AP.")
