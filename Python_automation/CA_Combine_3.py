import os
import xml.etree.ElementTree as ET
import pandas as pd
import glob
import time

def process_lob_files(input_path, max_files=None):
    """
    Processes .lob or .xml files from a glob pattern, directory, file, or list.
    Writes Bill_Version.csv to the parent of the first file processed.
    Args:
        input_path: glob pattern, directory, file, or list of files
        max_files: int or None, number of files to process (default: all)
    Returns:
        Path to Bill_Version.csv
    """
    # Accept a glob pattern, directory, or single file
    if isinstance(input_path, list):
        files_to_process = input_path
    elif isinstance(input_path, str) and ('*' in input_path or '?' in input_path or '[' in input_path):
        files_to_process = glob.glob(input_path)
    elif isinstance(input_path, str) and os.path.isdir(input_path):
        files_to_process = [
            os.path.join(input_path, f) for f in os.listdir(input_path)
            if f.endswith(".xml") or f.endswith(".lob")
        ]
    elif isinstance(input_path, str) and os.path.isfile(input_path) and (input_path.endswith(".xml") or input_path.endswith(".lob")):
        files_to_process = [input_path]
    else:
        print("Invalid input. Please provide a valid XML file, folder, glob pattern, or list of files.")
        return None

    # Limit the number of files for testing if max_files is set
    if max_files is not None:
        files_to_process = files_to_process[:max_files]

    Bill_dict = []

    # Namespace dictionary
    ns = {
        'caml': 'http://lc.ca.gov/legalservices/schemas/caml.1#',
        'xlink': 'http://www.w3.org/1999/xlink',
        'xhtml': 'http://www.w3.org/1999/xhtml',
        'xsi': 'http://www.w3.org/2001/XMLSchema-instance'
    }
    start_time = time.time()
    for file_path in files_to_process:
        filename = os.path.basename(file_path)
        try:
            tree = ET.parse(file_path)
            root = tree.getroot()
        except ET.ParseError as e:
            print(f"Error parsing {filename}: {e}")
            continue

        # Extract fields using namespace prefix and ns dictionary
        base = root

        ID = base.find(".//caml:Id", ns)
        ID = ID.text if ID is not None else None

        Action_text = base.find('.//caml:ActionText', ns)
        Action_text = Action_text.text if Action_text is not None else None

        Action_Date = base.find('.//caml:ActionDate', ns)
        Action_Date = Action_Date.text if Action_Date is not None else None

        title = base.find(".//caml:Title", ns)
        title = title.text if title is not None else None

        session_year = base.find(".//caml:SessionYear", ns)
        session_year = session_year.text if session_year is not None else None

        measure_type = base.find(".//caml:MeasureType", ns)
        measure_type = measure_type.text if measure_type is not None else None

        measurenum = base.find(".//caml:MeasureNum", ns)
        measurenum = measurenum.text if measurenum is not None else None

        subject = base.find(".//caml:Subject", ns)
        subject = subject.text if subject is not None else None

        relatingclause = base.find(".//caml:RelatingClause", ns)
        relatingclause = relatingclause.text if relatingclause is not None else None

        # Author Section
        legislator_contribution = base.find(".//caml:Contribution", ns)
        legislator_contribution = legislator_contribution.text if legislator_contribution is not None else None

        house = base.find(".//caml:House", ns)
        house = house.text if house is not None else None

        name = base.find(".//caml:Name", ns)
        name = name.text if name is not None else None

        # Digest Text (may contain HTML, so get inner XML/text)
        digesttext_elem = base.find(".//caml:DigestText", ns)
        if digesttext_elem is not None:
            # Join all text, including from child elements
            digesttext = ''.join(digesttext_elem.itertext()).strip()
        else:
            digesttext = None

        Bill_dict.append({
            "Doc_ID": ID,
            "Action_text": Action_text,
            "Action_Date": Action_Date,
            "Title": title,
            "Session Year": session_year,
            "Measure Type": measure_type,
            "Measure Number": measurenum,
            "Subject": subject,
            "Source File": filename,
            "Relating Clause": relatingclause,
            "Legislator_Contribution": legislator_contribution,
            "House": house,
            "Name": name,
            "Digest_Text": digesttext
        })
    if files_to_process:
        working_dir = os.path.dirname(os.path.dirname(files_to_process[0]))
    else:
        working_dir = os.getcwd()
    end_time = time.time()
    elapsed = end_time - start_time   
    output_filename = os.path.join(working_dir, 'Bill_Version.csv')
    pd.DataFrame(Bill_dict).to_csv(output_filename, index=False)
    print(f"Bill_Version.csv written to: {output_filename} in {elapsed:.2f} seconds")
    return output_filename

# Example usage:
if __name__ == "__main__":
    # You can pass a glob pattern, directory, file, or list of files
    lob_files = glob.glob('/Users/michaelingram/Documents/GitHub/CA_Bills-1/Python_automation/2025-05-25/Lob_files/BILL_VERSION_TBL*.lob')
    process_lob_files(lob_files, max_files=None)