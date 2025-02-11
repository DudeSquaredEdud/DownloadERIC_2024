import bs4
import json
import os
import requests
import tqdm


# bs4.BeautifulSoup
#####################
# get the files
files = []

with os.scandir('./DownloadERIC_2024/ids') as entries:
    for entry in entries:
        files.append(entry.path)


#####################
# Pull the IDs out
ids = []
for file in files:
    filedata = json.loads(open(file, 'r').read())
    for identifier in filedata["response"]["docs"]:
        ids.append(identifier["id"])

#####################
# Append to make URLs
urls = []

for identifier in ids:
    urls.append(f"https://eric.ed.gov/?id={identifier}")

outputURLs = []



i = 0
    
f = open("ERIC_2024_2025_urls.txt", "a")
for url in tqdm.tqdm(urls):
    try:
        soup = bs4.BeautifulSoup(requests.get(url, timeout=200).content, 'html.parser').find("div", {"class":"r_f"})
        outputURLs.append(soup.find("a")["title"])
    except:
        outputURLs.append(soup.find("a")["href"])
    
    f.write(outputURLs[-1] + '\n')
    
#################################
# This is the PDF download code
# It doesn't work correctly just yet
# Download the URLs if you can!
#################################
    
for url in outputURLs:
    soup = bs4.BeautifulSoup(requests.get(url,timeout=200), 'html.parser')
    links = soup.find_all('a')
    for link in tqdm.tqdm(links):
        if ('.pdf' in link.get('href', [])):
            i += 1
            print("Downloading file: ", i)

            # Get response object for link
            response = requests.get(link.get('href'), timeout=200)

            # Write content in pdf file
            pdf = open("pdf"+str(i)+".pdf", 'a')
            pdf.write(response.content)
            pdf.close()
            print("File ", i, " downloaded")
f.close()
