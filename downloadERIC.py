import bs4
import json
import os
import requests
from tqdm import tqdm
from urllib.parse import urljoin


# Hello! Thank you so much for helping.


start_index = 0
end_index = -1

files = [
    entry.path
    for entry in os.scandir('./DownloadERIC_2024/ids/ERIC_hosted')
    if entry.is_file()
]
ids = [[], []]
for file in files:
    with open(file) as f:
        data = json.load(f)
        ids[0].extend(doc["id"] for doc in data["response"]["docs"])
        ids[1].extend(doc["title"] for doc in data["response"]["docs"])

base_url = "https://eric.ed.gov/?id={}"
urls = [base_url.format(id) for id in ids[0]]

print(len(urls))

with requests.Session() as session, open("ERIC_2024_2025_urls.txt", "a") as f:
    session.headers.update({'User-Agent': 'Mozilla/5.0'})
    
    for url in tqdm(urls[start_index:end_index], desc="Processing URLs"):
        try:
            response = session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = bs4.BeautifulSoup(response.content, 'html.parser')
            if (div_rf := soup.find("div", class_="r_f")) and (a_tag := div_rf.find("a")):
                link = a_tag.get("title") or a_tag.get("href")
                if link:
                    f.write(f"{link}\n")
                    
            # Check and download PDF
                if link.lower().endswith('.pdf'):
                    current_id = url.split('=')[-1]
                    
                    try:
                        pdf_response = session.get(link, timeout=15, stream=True)
                        pdf_response.raise_for_status()
                        
                        # Create complete file path
                        pdf_path = os.path.join('./pdfs', f'{current_id}.pdf')
                        
                        # Ensure directory structure exists
                        os.makedirs(os.path.dirname(pdf_path), exist_ok=True)
                        
                        with open(pdf_path, 'wb') as pdf_file:
                            for chunk in pdf_response.iter_content(chunk_size=8192):
                                pdf_file.write(chunk)
                    
                        
                    except Exception as pdf_error:
                        print(f"PDF Download Error ({current_id}): {str(pdf_error)[:100]}")
        
            
        except (requests.RequestException, AttributeError) as e:
            continue