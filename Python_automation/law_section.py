import os
import glob
import xml.etree.ElementTree as ET
import json
import pandas as pd

def extract_law_section_content(input_path):
    """
    Extracts content from LAW_SECTION_TBL_*.lob files.
    Handles a single file or a directory.
    Returns a dict: {filename: content or error}
    """
    def parse_file(file_path):
        try:
            tree = ET.parse(file_path)
            root = tree.getroot()
            content_text = ''.join(root.itertext()).strip()
            return content_text
        except Exception as e:
            return f"Error: {str(e)}"

    result_dict = {}

    if os.path.isfile(input_path):
        filename = os.path.basename(input_path)[:-4]
        result_dict[filename] = parse_file(input_path)
        return result_dict
    elif os.path.isdir(input_path):
        files = glob.glob(os.path.join(input_path, "LAW_SECTION_TBL_*.lob"))
        for f in files:
            filename = os.path.basename(f)[:-4]
            result_dict[filename] = parse_file(f)
        csv_path = os.path.join(os.path.dirname(input_path), 'law_section_content.csv')
        pd.DataFrame.from_dict(result_dict, orient='index', columns=['Content']).to_csv(csv_path)
        return result_dict
    else:
        raise ValueError("Input path must be a file or directory.")

# Example usage:
if __name__ == "__main__":
    # For a single file:
    #single_file = "/Users/michaelingram/Documents/GitHub/CA_Bills-1/pubinfo_2025/LAW_SECTION_TBL_160834.lob"
    #result = extract_law_section_content(single_file)
    #print(json.dumps(result, indent=2))

    # For a directory:
    dir_path = "/Users/michaelingram/Documents/GitHub/CA_Bills-1/2025-06-27/Lob_files"
    results = extract_law_section_content(dir_path)
    json.dumps(results, indent=2)