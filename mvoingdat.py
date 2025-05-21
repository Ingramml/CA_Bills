import os
import shutil
import glob


#moves moves files from download directory to sql files

def move_files(input_path):
    # get all files in the input path
    
    files = glob.glob(input_path + '/*.dat')
    # move all files to the sql directory
    for file in files:
        print("moving file: ", file)
        filename=os.path.basename(file)
        os.rename(file, '/Users/michaelingram/Documents/Coding_Projects/CA_Bills/sqlfiles/'+filename)
        #shutil.move(file,'/Users/michaelingram/Documents/Coding_Projects/CA_Bills/sqlfiles' )
    print('Files moved to sql_files directory')
    print("moving files from:" +   input_path)

if __name__ == '__main__':
    move_files('download')





move_files('/Users/michaelingram/Downloads/pubinfo_daily_Wed')