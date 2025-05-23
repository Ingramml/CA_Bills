import os
import shutil
import glob

def move_files(inputpath):
    
    output_path = os.path.dirname(inputpath)
    """
    print('Moving files from: ' + inputpath)
    print('Moving files to: ' + output_path)
    """
    # Find all .bat files in the input path
    files_to_be_moved = glob.glob(os.path.join(inputpath, '*.*'))
    
    print('Files to be moved: ' + str(files_to_be_moved))

    for file in files_to_be_moved:
        if file.endswith('.bat'):
            print(f'Skipping file: {file}')
            destination = os.path.join(output_path,"Bat_files", os.path.basename(file))

        elif file.endswith('.lob'):
            destination = os.path.join(output_path,"LObFiles" ,os.path.basename(file))
        print(f'Moving file: {file} to {destination}')
        
        # Move the file
        shutil.move(file, destination)

    print('Files moved successfully')

if __name__ == "__main__":
    """
    """

def unzip(zip_file_path):
    import zipfile
    import os
    unzip_dir = os.path.join(os.path.dirname(zip_file_path), "unzip")

    if os.path.exists(unzip_dir):
        print(f"Directory {unzip_dir} already exists.")
    else:    
        os.makedirs(unzip_dir, exist_ok=True)
    
    # Open the zip file and extract to the unzip_dir
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(unzip_dir)

    print('Unzipping complete')
    return unzip_dir
 

if __name__ == "__main__":
    zipfile_path = "/Users/michaelingram/Documents/GitHub/CA_bills/Python automation/2025-05-20/pubinfo_daily_Sun.zip"
    unzip(zipfile_path)

