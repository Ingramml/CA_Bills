import datetime
from bs4 import BeautifulSoup
import os
import requests

# This script downloads specific files from the California Legislative Information website.
# It looks for "pubinfo_daily_Sun.zip" and "pubinfo_2025.zip" files, downloads them if they are not already present,
# and saves them in a date-stamped directory within the specified output folder.

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

    return working_dir

# Example usage:
if __name__ == "__main__":
    """
    output_folder = "/Users/michaelingram/Documents/GitHub/CA_Bills-1/Python_automation"
    download_pubinfo_files(output_folder)
    """