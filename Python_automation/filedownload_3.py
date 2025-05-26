import datetime
from bs4 import BeautifulSoup
import os
import requests



def download_pubinfo_files(output_folder):
    url = "https://downloads.leginfo.legislature.ca.gov/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    files_to_download = ["pubinfo_daily_Sun.zip", "pubinfo_2025.zip"]
    download_urls = {}

    for link in soup.find_all("a"):
        href = link.get("href")
        for fname in files_to_download:
            if href and fname in href:
                download_urls[fname] = url + href

    today = datetime.date.today()
    working_dir = os.path.join(output_folder, today.strftime("%Y-%m-%d"))
    os.makedirs(working_dir, exist_ok=True)

    results = {}
    for fname in files_to_download:
        file_path = os.path.join(working_dir, fname)
        if os.path.exists(file_path):
            print(f"File already exists: {file_path}")
            results[fname] = file_path
        elif fname in download_urls:
            print(f"Downloading: {download_urls[fname]}")
            r = requests.get(download_urls[fname])
            with open(file_path, "wb") as f:
                f.write(r.content)
            print(f"Download complete: {file_path}")
            results[fname] = file_path
        else:
            print(f"{fname} not found on the website.")
            results[fname] = None

    # Return working_dir and a list of non-None zip file paths
    zip_files = [path for path in results.values() if path]
    return working_dir, zip_files