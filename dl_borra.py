import urllib.request
import json
import ssl

places = {
    'borra.jpg': 'Borra_Caves'
}

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

req_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

for filename, title in places.items():
    try:
        print(f"Downloading {filename} from {title}...")
        api_url = f"https://en.wikipedia.org/w/api.php?action=query&titles={title}&prop=pageimages&format=json&pithumbsize=2000"
        
        req = urllib.request.Request(api_url, headers=req_headers)
        with urllib.request.urlopen(req, context=ctx) as response:
            data = json.loads(response.read().decode('utf-8'))
            pages = data['query']['pages']
            page_id = list(pages.keys())[0]
            if 'thumbnail' in pages[page_id]:
                img_url = pages[page_id]['thumbnail']['source']
                
                img_req = urllib.request.Request(img_url, headers=req_headers)
                with urllib.request.urlopen(img_req, context=ctx) as img_resp, open(f'static/{filename}', 'wb') as out_file:
                    out_data = img_resp.read()
                    out_file.write(out_data)
                print(f"Success for {filename}. Size: {len(out_data)} bytes")
            else:
                print(f"No thumbnail found for {title}")
    except Exception as e:
        print(f"Failed {filename}: {e}")
