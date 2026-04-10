import pandas as pd
import os

csv_path = r'datasets\AP_DATASET.CSV'

if not os.path.exists(csv_path):
    print(f"Error: {csv_path} not found.")
    exit(1)

# Load existing dataset
df = pd.read_csv(csv_path)

# Ensure Entry_Fee column exists in the main dataset first
if 'Entry_Fee' not in df.columns:
    df['Entry_Fee'] = "N/A"

# Normalize names for duplicate checking
def get_clean_key(name):
    s = str(name).lower()
    mapping = {"simhachalam": "simhachalam_temple", "varaha lakshmi narasimha": "simhachalam_temple"}
    for k, v in mapping.items():
        if k in s: return v
    return "".join(s.split())

existing_keys = set(df[df['City_Name'].str.contains('Visakhapatnam|Vizag', case=False, na=False)]['Tourist_Place'].apply(get_clean_key))

# Vizag Tourism Extracted List (31 New Spots)
# Format: [City, District, Area, Lat, Lon, Name, Description, Hotel, Rating, NearbyHotel, NearbyRestaurant, RatingRest, RestLoc, RestType, HotelLoc, HotelType, RestLoc2, HotelLoc2, PS, Shop, FinalRating]
new_vizag_spots = [
    ["Visakhapatnam", "Visakhapatnam", "Beach Road", 17.6967, 83.295, "Sri Kanaka Mahalakshmi Temple", "Historical Temple", "Dolphin Hotel", 5.0, "Near Port", "Coastal", 4.7, "Beach Road", "Tiffins", "Beach Road", "Dolphin", "Port Road", "Dolphin", "One Town PS", "Market", 5.0],
    ["Visakhapatnam", "Visakhapatnam", "Araku Road", 17.6583, 82.3853, "Kothapally Waterfalls", "Scenic Waterfall", "Araku Resorts", 4.9, "Araku Valley", "Hill Resort", 4.8, "Cascade Road", "Tiffins", "Nearby", "Resort", "Araku Road", "Araku Valley", "Paderu PS", "Araku Road", 4.9],
    ["Visakhapatnam", "Visakhapatnam", "Bheemili", 17.8911, 83.4455, "Bheemunipatnam Beach", "Dutch Heritage Port", "Bheemili Beach Resort", 4.8, "Bheemili", "Marine Drive", 4.6, "Dutch Road", "Seafood", "Beach Road", "Resort", "Main Road", "Beach Road", "Bheemis PS", "Market", 4.8],
    ["Visakhapatnam", "Visakhapatnam", "Sivaji Palem", 17.7283, 83.3367, "Sivaji Park", "Urban Recreation Park", "Welcomhotel", 4.7, "MVP Colony", "Sivaji Road", 4.5, "MVP Colony", "Tiffins", "Nearby", "Luxury", "MVP Colony", "MVP Main Road", "MVP PS", "Main Road", 4.7],
    ["Visakhapatnam", "Visakhapatnam", "Nearby Vizag", 17.7667, 83.3333, "Kambalakonda Wildlife Sanctuary", "Eco-Tourism Park", "Local Guesthouse", 4.8, "Santuary Rd", "Eco Cafe", 4.6, "Gate Entrance", "Snacks", "Entrance Area", "Lodge", "Nearby", "Highway Road", "Highway PS", "Main Road", 4.8],
    ["Visakhapatnam", "Visakhapatnam", "Port Area", 17.6911, 83.2967, "Ross Hill Church", "Hilltop Church & View", "Port Residency", 4.9, "Port Area", "Port View", 4.7, "Hill Road", "Meals", "Nearby", "Hospitaility", "Hill Entrance", "Port Road", "Port PS", "Harbour Area", 4.9],
    ["Visakhapatnam", "Visakhapatnam", "Gajuwaka", 17.6167, 83.2450, "Gangavaram Beach", "Private Beach Area", "Steel Plant Hotel", 4.6, "Gajuwaka", "Steel Hub", 4.4, "Factory Road", "Meals", "Gajuwaka", "Lodge", "Near Port", "Gajuwaka Road", "Gajuwaka PS", "Gajuwaka", 4.6],
    ["Visakhapatnam", "Visakhapatnam", "Konda Area", 17.6833, 83.2917, "Sri Venkateswara Swamy Konda Temple", "Hill Temple & Viewpoint", "Hill View Hotel", 5.0, "Konda Area", "Hill Tiffins", 4.8, "Hill Top", "Snacks", "Hill Side", "Guest House", "Hill Road", "Hill Top", "Port PS", "Hill Market", 5.0],
    ["Visakhapatnam", "Visakhapatnam", "MVP Area", 17.7317, 83.3444, "Lawson's Bay Beach", "Quiet Beach Side", "The Park Vizag", 4.8, "Beach Road", "The Park Food", 4.9, "Beach Front", "Global", "The Park", "Luxury", "Beach Road", "Luxury Resort", "MVP PS", "Beach Area", 4.8],
    ["Visakhapatnam", "Visakhapatnam", "Naval Base", 17.7125, 83.3139, "Naval Museum", "Naval Heritage Site", "Novotel", 4.9, "Beach Road", "Naval Mess", 4.8, "Harbour Road", "History", "Nearby", "Hotel", "Main Road", "Beach Road", "Harbour PS", "Beach Side", 4.9],
    ["Visakhapatnam", "Visakhapatnam", "Yarada", 17.6767, 83.2917, "Dolphin's Nose Light House", "Panoramic Viewpoint", "Yarada Resort", 5.0, "Yarada", "Lighthouse Cafe", 4.7, "Hilltop", "Snacks", "Lighthouse Road", "Resort", "Resort Entrance", "Yarada Beach", "New Port PS", "Beach Road", 5.0],
    ["Visakhapatnam", "Visakhapatnam", "One Town", 17.7125, 83.3111, "Queen Victoria Pavilion", "Colonial Monument", "Town Hotel", 4.7, "Market Area", "Town Food", 4.5, "Main Road", "Tiffins", "Nearby", "Lodge", "Town Road", "One Town", "One Town PS", "Main Market", 4.7],
    ["Visakhapatnam", "Visakhapatnam", "Anakapalle", 17.6883, 82.9917, "Nookambika Temple", "Famous Shakti Temple", "Anakapalle Hotel", 4.9, "Anakapalle", "Temple Road", 4.6, "Temple Road", "Meals", "Nearby", "Lodge", "Temple Entrance", "Market Road", "Anakapalle PS", "Main Road", 4.9],
    ["Visakhapatnam", "Visakhapatnam", "Rushikonda", 17.7417, 83.3517, "Titanic Sea View Point", "Breathtaking Ocean View", "Haritha Resorts", 5.0, "Rushikonda", "Hilltop Cafe", 4.8, "Hill Road", "Snacks", "Hilltop Entrance", "Resort", "Rushikonda Rd", "Hill Side", "Rushikonda PS", "Hilltop", 5.0],
    ["Visakhapatnam", "Visakhapatnam", "Madhurawada", 17.7811, 83.325, "Shilparamam Jathara", "Arts & Crafts Village", "Fairfield Marriot", 4.8, "Highway", "Jathara Food", 4.6, "Highway Road", "Snacks", "Nearby", "Premium", "Cricket Stadium", "Main Road", "PM Palem PS", "Highway Road", 4.8],
    ["Visakhapatnam", "Visakhapatnam", "Beach Road", 17.7267, 83.3311, "Lumbini Park", "Sea View Garden", "Four Points", 4.7, "Siripuram", "Lumbini Food", 4.5, "Beach Road", "Snacks", "Siripuram", "Premium", "Main Road", "Beach Road", "Beach Road PS", "Park Area", 4.7],
    ["Visakhapatnam", "Visakhapatnam", "Atchutapuram", 17.5833, 83.1167, "Thanthadi Beach", "Offbeat Virgin Beach", "Pharma City Hotel", 4.6, "Atchutapuram", "Highway Food", 4.3, "Highway Road", "Meals", "Atchutapuram", "Lodge", "Steel Plant", "Atchutapuram", "Steel Plant PS", "Main Road", 4.6],
    ["Visakhapatnam", "Visakhapatnam", "Jodugullapalem", 17.8333, 83.3917, "Mangamaripeta Beach", "Adventure Beach", "Bheemili Resort", 4.8, "Mangamaripeta", "Island Cafe", 4.6, "Adventure Rd", "Seafood", "Beach Side", "Lodge", "Bheemili Rd", "Mangamaripeta", "Bheemili PS", "Market Area", 4.8],
    ["Visakhapatnam", "Visakhapatnam", "Parawada", 17.5333, 83.05, "Mutyalammapalem Beach", "Fishing Village Beach", "Steel Plant Hotel", 4.6, "Steel Plant Area", "Canteen", 4.3, "Highway Road", "Meals", "Steel Plant", "Lodge", "Steel Plant Road", "Steel Plant Area", "Steel Plant PS", "Main Road", 4.6],
    ["Visakhapatnam", "Visakhapatnam", "City Center", 17.7167, 83.3083, "VMRDA City Central Park", "Large Urban Park", "Daspalla", 4.8, "RTC Complex", "Daspalla Rest", 4.9, "Jagadamba", "Cuisine", "RTC Complex", "Luxury", "Main Road", "Seven Hills", "II Town PS", "Jagadamba", 4.8],
    ["Visakhapatnam", "Visakhapatnam", "Harbour", 17.6967, 83.30, "Fishing Harbour", "Busy Fishing Port", "Port Residency", 4.7, "Port Area", "Coastal", 4.6, "Harbour Road", "Seafood", "Nearby", "Lodge", "Main Road", "Port Area", "One Town PS", "Market", 4.7],
    ["Visakhapatnam", "Visakhapatnam", "Simhachalam Road", 17.7833, 83.22, "Meghadri Gedda Reservoir", "Drinking Water Supply", "Airport Hotel", 4.6, "Airport", "Reservoir Cafe", 4.3, "Reservoir Rd", "Snacks", "Airport Road", "Premium", "Highway", "Airport Road", "Gopalapatnam PS", "Main Road", 4.6],
    ["Visakhapatnam", "Visakhapatnam", "Kailasagiri", 17.7583, 83.35, "Telugu Samskruthika Niketanam", "Museum of Telugu Culture", "Welcomhotel", 4.9, "Kailasagiri", "Hill Food", 4.7, "Hill Top", "Snacks", "Nearby", "Premium", "Kailasagiri entrance", "Main Road", "Rushikonda PS", "Hilltop Area", 4.9],
    ["Visakhapatnam", "Visakhapatnam", "Mudasarlova", 17.7611, 83.275, "Mudasarlova Park", "Oldest Reservoir & Park", "Hanumanthawaka Hotel", 4.7, "BRTS Road", "Park Cafe", 4.5, "Mudasarlova Rd", "Tiffins", "Nearby", "Lodge", "BRTS Main Road", "BRTS Highway", "Adarsh Nagar PS", "Main Road", 4.7],
    ["Visakhapatnam", "Visakhapatnam", "Steel Plant", 17.5833, 83.1833, "Appikonda Beach", "Shiva Temple Beach", "Gajuwaka Hotel", 4.6, "Steel Plant Area", "Steel Food", 4.4, "Factory Gate", "Meals", "Nearby", "Lodge", "Steel Plant Gate", "Gajuwaka Rd", "Steel Plant PS", "Gajuwaka market", 4.6],
    ["Visakhapatnam", "Visakhapatnam", "Asilmetta", 17.7117, 83.305, "Sree Sampath Vinayagar Temple", "Miracle Ganapati Temple", "Green Park Hotel", 5.0, "RTC Complex", "Green Park Rest", 4.9, "Asilmetta", "Global", "Asilmetta", "Luxury", "Main Junction", "RTC Complex", "II Town PS", "Central Market", 5.0],
    ["Visakhapatnam", "Visakhapatnam", "Beach Road", 17.71, 83.315, "Durga Beach", "Small Gated Beach", "Coastal Residency", 4.6, "Old Town", "Beach Tiffins", 4.4, "Beachfront", "Seafood", "Nearby", "Lodge", "Beach Side", "Coastal Road", "Coastal PS", "Old Town", 4.6],
    ["Visakhapatnam", "Visakhapatnam", "Ross Hill", 17.6911, 83.295, "Baba Ishaq Madina Mosque", "Dargah with Sea View", "Harbour View", 4.8, "Harbour Area", "Dargah Food", 4.5, "Harbour Road", "Haleem", "Hilltop Entrance", "Lodge", "One Town", "Port Area", "Port PS", "Harbour market", 4.8],
    ["Visakhapatnam", "Visakhapatnam", "Beach Road", 17.7183, 83.3333, "TU 142 Aircraft Museum", "Real Aircraft Museum", "Palm Beach Hotel", 4.9, "Beach front", "Palm Cafe", 4.7, "Beach Road", "International", "Beach Road", "Premium", "Submarine Lane", "Beach Road", "Beach Road PS", "Beach Side", 4.9],
    ["Visakhapatnam", "Visakhapatnam", "Sabbavaram", 17.7833, 83.0833, "Devipuram", "Unique Meru Temple", "Highway Lodge", 5.0, "Anakapalle Road", "Lodge Cafe", 4.6, "Highway Jct", "Meals", "Anakapalle", "Lodge", "Highway Jct", "Anakapalle Rd", "Sabbavaram PS", "Anakapalle Market", 5.0],
    ["Visakhapatnam", "Visakhapatnam", "Sagar Nagar", 17.7317, 83.345, "ISKCON Temple Vizag", "Beautiful Spiritual Center", "Sagar Nagar Lodge", 5.0, "Sagar Nagar", "Iskcon Govinda", 4.9, "Iskcon Campus", "Pure Veg", "Iskcon Guest House", "Lodge", "Sagar Nagar entrance", "Highway Road", "Arilova PS", "Sagar Nagar", 5.0],
]

# De-duplicate check
to_add = []
for spot in new_vizag_spots:
    if get_clean_key(spot[5]) not in existing_keys:
        to_add.append(spot)

if not to_add:
    print("No new unique places found to add.")
else:
    # Create DataFrame for new rows
    new_df = pd.DataFrame(to_add, columns=df.columns[:21]) # Use first 21 columns
    
    # Set Entry_Fee
    temple_keywords = ["Temple", "Mosque", "Church", "Dargah", "Devipuram", "Simhachalam"]
    def apply_free(row):
        name = str(row['Tourist_Place'])
        if any(k in name for k in temple_keywords):
            return "Free"
        return "N/A"
    
    new_df['Entry_Fee'] = new_df.apply(apply_free, axis=1)
    
    # Append
    final_df = pd.concat([df, new_df], ignore_index=True)
    final_df.to_csv(csv_path, index=False)
    print(f"Successfully added {len(to_add)} unique Vizag locations.")
