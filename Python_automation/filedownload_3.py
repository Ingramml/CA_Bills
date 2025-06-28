import datetime
from bs4 import BeautifulSoup
import os
import requests

def download_large_file(url, file_path, chunk_size=1024*1024):
    with requests.get(url, stream=True, timeout=300) as r:
        r.raise_for_status()
        with open(file_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=chunk_size):
                if chunk:
                    f.write(chunk)

def download_pubinfo_files(output_folder):
    output_folder = os.getcwd() if output_folder is None else output_folder
    url = "https://downloads.leginfo.legislature.ca.gov/"
    response = requests.get(url, stream=True, timeout=300)
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
            file_url = download_urls[fname]
            try:
                download_large_file(file_url, file_path)
                print(f"Download complete: {file_path}")
                results[fname] = file_path
            except Exception as e:
                print(f"Failed to download {fname}: {e}")
                results[fname] = None
        else:
            print(f"{fname} not found on the website.")
            results[fname] = None

    zip_files = [path for path in results.values() if path]
    return working_dir, zip_files

if __name__ == "__main__":
    output_folder = os.getcwd()
    working_dir, zipfile_paths = download_pubinfo_files(output_folder)
    print(f"Working directory: {working_dir}")
    print(f"Downloaded zip files: {zipfile_paths}")
