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
        # Create a unique temp directory for each lob file
        base_name = os.path.basename(lob_file).replace('.lob', '')
        temp_dir = os.path.join(extract_dir, f"tmp_{base_name}")
        os.makedirs(temp_dir, exist_ok=True)
        with zipfile.ZipFile(lob_file, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)
        # Find the document.xml file
        doc_xml_path = os.path.join(temp_dir, "word", "document.xml")
        if os.path.exists(doc_xml_path):
            # Move document.xml to a unique name in extract_dir
            new_name = base_name + "_document.xml"
            new_path = os.path.join(extract_dir, new_name)
            os.rename(doc_xml_path, new_path)
        else:
            new_path = None
        # Clean up the temp directory
        import shutil
        shutil.rmtree(temp_dir)
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
        extract_dir = os.path.join(os.path.dirname(input_path), "unzipped_lob")
        os.makedirs(extract_dir, exist_ok=True)
        for lob_file in lob_files:
            kept = process_lob_file(lob_file, extract_dir)
            if kept:
                kept_files.append(kept)
    else:
        raise ValueError("Input must be a .lob file or a directory containing .lob files.")
    return kept_files

import os
import glob
from xml.etree import ElementTree as ET

def extract_bill_analysis_text(input_path):
    """
    Extracts text from one or more WordprocessingML document.xml files.
    Accepts a directory or a single file.
    Returns a dict: {filename: extracted_text}
    """
    def extract_text_from_docxml(doc_path):
        try:
            tree = ET.parse(doc_path)
            root = tree.getroot()
            namespace = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
            paragraphs = []
            for para in root.findall(".//w:p", namespace):
                runs = para.findall(".//w:t", namespace)
                texts = [run.text for run in runs if run.text]
                if texts:
                    paragraphs.append("".join(texts))
            return "\n\n".join(paragraphs)
        except Exception as e:
            return f"Error: {str(e)}"

    results = {}

    if os.path.isfile(input_path):
        # If it's a document.xml file
        if input_path.endswith("document.xml"):
            filename = os.path.basename(input_path)
            results[filename] = extract_text_from_docxml(input_path)
        # If it's a .lob file, try to extract document.xml first
        elif input_path.endswith('.lob'):
            # You can call your extract_and_keep_document_xml here if needed
            pass
    elif os.path.isdir(input_path):
        # Find all *_document.xml files in the directory (recursively)
        docxml_files = glob.glob(os.path.join(input_path, "*_document.xml"))
        if not docxml_files:
            # Also check for document.xml in subfolders
            docxml_files = [y for x in os.walk(input_path) for y in glob.glob(os.path.join(x[0], 'document.xml'))]
        for doc_path in docxml_files:
            filename = os.path.basename(doc_path)
            results[filename] = extract_text_from_docxml(doc_path)
    else:
        raise ValueError("Input path must be a file or directory.")

    return results

# Example usage:
if __name__ == "__main__":
    # For a directory containing *_document.xml files:
    dir_path = "/Users/michaelingram/Documents/GitHub/CA_Bills-1/2025-06-20/dunzipped_lob"
    result = extract_bill_analysis_text(dir_path)
    print(result)

    # For a single file:
    # file_path = "/Users/michaelingram/Documents/GitHub/CA_Bills-1/2025-06-20/dunzipped_lob/BILL_ANALYSIS_TBL_1_document.xml"
    # result = extract_bill_analysis_text(file_path)
    # print(result)

























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
