import os
import zipfile
import glob

def extract_and_keep_document_xml(input_path):
    """
    Unzips all BILL_ANALYSIS_TBL_*.lob files in a directory (or a single file),
    keeps only the word/document.xml file for each, and deletes all other extracted files.
    Returns a list of paths to the kept document.xml files.
    """
    def process_lob_file(lob_file, extract_dir):
        with zipfile.ZipFile(lob_file, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)
        # Find the document.xml file
        doc_xml_path = os.path.join(extract_dir, "word", "document.xml")
        if os.path.exists(doc_xml_path):
            # Move document.xml to a unique name in extract_dir
            new_name = os.path.basename(lob_file).replace('.lob', '') + "_document.xml"
            new_path = os.path.join(extract_dir, new_name)
            os.rename(doc_xml_path, new_path)
        else:
            new_path = None
        # Remove all other files and folders in extract_dir except the new_path
        for root, dirs, files in os.walk(extract_dir, topdown=False):
            for file in files:
                file_path = os.path.join(root, file)
                if file_path != new_path:
                    os.remove(file_path)
            for dir in dirs:
                dir_path = os.path.join(root, dir)
                if os.path.exists(dir_path):
                    try:
                        os.rmdir(dir_path)
                    except OSError:
                        pass
        return new_path

    kept_files = []
    if os.path.isfile(input_path) and input_path.endswith('.lob'):
        extract_dir = os.path.join(os.path.dirname(input_path), "unzipped_lob")
        os.makedirs(extract_dir, exist_ok=True)
        kept = process_lob_file(input_path, extract_dir)
        if kept:
            kept_files.append(kept)
    elif os.path.isdir(input_path):
        lob_files = glob.glob(os.path.join(input_path, "BILL_ANALYSIS_TBL_*.lob"))
        extract_dir = os.path.join(input_path, "unzipped_lob")
        os.makedirs(extract_dir, exist_ok=True)
        for lob_file in lob_files:
            kept = process_lob_file(lob_file, extract_dir)
            if kept:
                kept_files.append(kept)
    else:
        raise ValueError("Input must be a .lob file or a directory containing .lob files.")
    return kept_files

# Example usage:
if __name__ == "__main__":
    # For a directory:
    dir_path = "/Users/michaelingram/Documents/GitHub/CA_Bills-1/2025-06-27/Lob_files"
    kept = extract_and_keep_document_xml(dir_path)
    print("Kept files:", kept)

    # For a single file:
    # file_path = "/Users/michaelingram/Documents/GitHub/CA_Bills-1/2025-06-20/Lob_files/BILL_ANALYSIS_TBL_1.lob"
    # kept = extract_and_keep_document_xml(file_path)
    # print("Kept file:", kept)
