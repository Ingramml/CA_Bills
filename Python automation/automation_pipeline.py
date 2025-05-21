from filedownload import download_pubinfo_daily_sun
from movefiles import unzip



output_folder = "/Users/michaelingram/Documents/GitHub/CA_bills/Python automation"
zipfile_path=download_pubinfo_daily_sun(output_folder)
unzip(zipfile_path)
