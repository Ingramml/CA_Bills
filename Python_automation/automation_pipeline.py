from filedownload import download_pubinfo_daily_sun
from movefiles import unzip,move_files



output_folder = "/Users/michaelingram/Documents/GitHub/CA_bills/Python automation"
zipfile_path,working_dir=download_pubinfo_daily_sun(output_folder)
move_files(working_dir)
unzip(zipfile_path)
