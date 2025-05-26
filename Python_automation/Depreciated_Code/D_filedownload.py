import os
import requests
from bs4 import BeautifulSoup
import datetime


def download_pubinfo_daily_sun(output_folder):
    url = "https://downloads.leginfo.legislature.ca.gov/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    download_url = None
    for link in soup.find_all("a"):
        href = link.get("href")
        if href and "pubinfo_daily_Sun.zip" in href:
            download_url = url + href
            break

    if download_url:

        today= datetime.date.today()
        working_dir = os.path.join(output_folder, today.strftime("%Y-%m-%d"))
        os.makedirs(working_dir, exist_ok=True)
        
        file_path = os.path.join(working_dir, "pubinfo_daily_Sun.zip")
        if os.path.exists(file_path):
            print(f"File already exists: {file_path}")
            return file_path,working_dir
        else:
            print(f"Downloading: {download_url}")
            r = requests.get(download_url)
            with open(file_path, "wb") as f:
                f.write(r.content)
            print(f"Download complete: {file_path}")
            return file_path,working_dir
    else:
        print("pubinfo_daily_Sun.zip not found.")
        return None,None
    

if __name__ == "__main__":
    """
    output_folder  =  "/Users/michaelingram/Documents/GitHub/CA_Bills-2/Python_automation"
    download_pubinfo_daily_sun(output_folder)
    """