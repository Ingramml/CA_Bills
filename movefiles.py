import os
import shutil
import glob

def move_files(inputpath):
    output_path = '/Users/michaelingram/Documents/GitHub/CA_bills/CA_Bills/Sqlfiles'
    
    print('Moving files from: ' + inputpath)
    print('Moving files to: ' + output_path)

    # Find all .bat files in the input path
    files_to_be_moved = glob.glob(os.path.join(inputpath, '*.dat'))
    
    print('Files to be moved: ' + str(files_to_be_moved))

    for file in files_to_be_moved:
        destination = os.path.join(output_path, os.path.basename(file))
        print(f'Moving file: {file} to {destination}')
        
        # Move the file
        shutil.move(file, destination)

    print('Files moved successfully')

move_files('/Users/michaelingram/Documents/pubinfo_2025')
