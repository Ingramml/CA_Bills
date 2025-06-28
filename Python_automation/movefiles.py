import os
import shutil
import glob
import zipfile
import os
import datetime

def move_files(*inputpaths):
    #Moves files from the input paths to their respective directories based on file extensions.
   for inputpath in inputpaths:
        output_path = os.path.dirname(inputpath)
        print(f"output path {output_path}")
        files_to_be_moved = glob.glob(os.path.join(inputpath, '*.*'))
        for file in files_to_be_moved:
            if file.endswith('.dat'):
                destination = os.path.join(output_path,"Dat_files", os.path.basename(file))
                os.makedirs(os.path.join(output_path,"Dat_files"), exist_ok=True)  
                shutil.move(file, destination)
            elif file.endswith('.lob'):
                destination = os.path.join(output_path,"Lob_files" ,os.path.basename(file))
                os.makedirs(os.path.join(output_path,"Lob_files"), exist_ok=True) 
                shutil.move(file, destination)
print('Files moved successfully')

def unzip(*zip_file_paths):
    today = datetime.date.today().strftime("%Y-%m-%d")
    unzip_dirs = []
    for zip_file_path in zip_file_paths:
        unzip_dir = os.path.join(os.path.dirname(zip_file_path), "unzip")
        print(f'Unzipping {zip_file_path} to {unzip_dir}')
        if not os.path.exists(unzip_dir):
            os.makedirs(unzip_dir, exist_ok=True)
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(unzip_dir)
        print(f'Unzipping complete for {zip_file_path}')
        unzip_dirs.append(unzip_dir)
    return unzip_dirs
    
 

if __name__ == "__main__":
    
    
    zip_file_path = ["/Users/michaelingram/Documents/GitHub/CA_Bills-1/2025-06-27/pubinfo_2025.zip","/Users/michaelingram/Documents/GitHub/CA_Bills-1/2025-06-27/pubinfo_daily_Sun.zip"]
    unzip(*zip_file_path)
    
    inputpath = "/Users/michaelingram/Documents/GitHub/CA_Bills-1/2025-06-27/unzip"
    move_files(inputpath)
    