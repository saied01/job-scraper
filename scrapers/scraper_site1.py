import requests
from bs4 import BeautifulSoup
import json

# URL TO SCRAPE
url = "https://ar.computrabajo.com/trabajo-de-desarrollador"

# HEADERS TO AVOID CAPTCHA
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
}


# REQUEST SERVER FOR DATA
response = requests.get(url, headers=headers)


if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")

    # FIND SCRIPT WITH JSON-LD
    script_tag = soup.find("script", type="application/ld+json")

    if script_tag:
        data = json.loads(script_tag.string)    # LOAD JSON

        #print(json.dumps(data, indent=2, ensure_ascii=False))

        # SPECIFIC 'COMPUTRABAJO'
        job_list = data["@graph"][2]["itemListElement"]
 
        for job in job_list:
            job_url = job.get("url", "N/A")
            position = job.get("position", "N/A")
            
            job_url_response = requests.get(job_url, headers=headers)
            job_soup = BeautifulSoup(job_url_response.text, "html.parser")

            tags = job_soup.find_all("span", class_="tag base mb10")

            # Imprimir todos
            for tag in tags:
                print(tag.text)
 
 
    #print(soup.prettify())
else:
    print("ERROR:", response.status_code)