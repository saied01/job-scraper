import requests
from bs4 import BeautifulSoup
import json
import os
import csv

def scrape_site1():

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    DB_DIR = os.path.join(BASE_DIR, "data")
    
    os.makedirs(DB_DIR, exist_ok=True)
    
    
    csv_path = os.path.join(DB_DIR, "computrabajo.csv")
    
    
    jobs_data = []
    
    
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

                main = job_soup.find("main", class_="detail_fs")

                scope = main if main is not None else job_soup  # fallback al documento entero


                puesto_tag = scope.find("h1", class_=lambda c: c and "box_detail" in c)
                empresa_tag = scope.find("p", class_=lambda c: c and "fs16" in c)

                # EXCTRACT VALUE FROM TAGS OUTSIDE OF TAGS LIST
                puesto = puesto_tag.get_text(strip=True) if puesto_tag else "N/A"

                if empresa_tag:
                    empresa_text = empresa_tag.text.strip()
                    partes = [p.strip() for p in empresa_text.split(" - ")]

                    if len(partes) >= 2:
                        # La última es ubicación
                        ubicacion = partes[-1]
                        # Todo lo demás junto como empresa (puede incluir departamento)
                        empresa = ", ".join(partes[:-1])
                    else:
                        empresa = partes[0]
                        ubicacion = "N/A"
                else:
                    empresa, ubicacion = "N/A", "N/A"


                # CREATE DICT FOR TAG AMOUNT
                job_info = {
                    "url": job_url,
                    "puesto": puesto,
                    "ubicacion": ubicacion,
                    "empresa": empresa,
                    "salario": "N/A",
                    "contrato": "N/A",
                    "jornada": "N/A",
                    "modalidad": "N/A"
                }


                tags = job_soup.find_all("span", class_="tag base mb10")
                tag_texts = [t.text.strip() for t in tags]

                for t in tags:
                    text = t.get_text(strip=True)

                    if text.startswith("$") or text.lower().startswith("a convenir"):
                        job_info["salario"] = text
                    elif "contrato" in text.lower():
                        job_info["contrato"] = text
                    elif "jornada" in text.lower():
                        job_info["jornada"] = text
                    elif "remoto" in text.lower() or "presencial" in text.lower() or "híbrido" in text.lower():
                        job_info["modalidad"] = text

                jobs_data.append(job_info)


    if jobs_data:
        with open(csv_path, "w", newline="", encoding="utf8") as f:
            writer = csv.DictWriter(f, fieldnames=jobs_data[0].keys())
            writer.writeheader()
            writer.writerows(jobs_data)

        print(f"✅ datos guardados en {csv_path}")
    else:
        print("⚠️ No se encontraron trabajos.")