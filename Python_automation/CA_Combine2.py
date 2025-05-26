import os
import xml.etree.ElementTree as ET
import pandas as pd
import glob

lob=glob.glob('/Users/michaelingram/Documents/GitHub/CA_Bills-1/Python_automation/2025-05-25/Lob_files/BILL_VERSION_TBL_2*.lob')
input_path = lob
files_to_process = []
MAX_FILES = None   # Limit the number of files to process for testing
# Accept a glob pattern, directory, or single file
if isinstance(input_path, list):
    files_to_process = input_path
elif '*' in input_path or '?' in input_path or '[' in input_path:
    files_to_process = glob.glob(input_path)
elif os.path.isdir(input_path):
    files_to_process = [
        os.path.join(input_path, f) for f in os.listdir(input_path)
        if f.endswith(".xml") or f.endswith(".lob")
    ]
elif os.path.isfile(input_path) and (input_path.endswith(".xml") or input_path.endswith(".lob")):
    files_to_process = [input_path]
else:
    print("Invalid input. Please provide a valid XML file, folder, or glob pattern.")

# Limit the number of files for testing
files_to_process = files_to_process[:MAX_FILES]

Bill_dict = []

# Namespace dictionary (no leading space in 'xhtml')
ns = {
    'caml': 'http://lc.ca.gov/legalservices/schemas/caml.1#',
    'xlink': 'http://www.w3.org/1999/xlink',
    'xhtml': 'http://www.w3.org/1999/xhtml',
    'xsi': 'http://www.w3.org/2001/XMLSchema-instance'
}

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
working_dir=os.path.dirname(os.path.dirname(file_path))
print(f"Working directory: {working_dir}")
filename=os.path.join(working_dir, 'Bill_Version.csv')
df=pd.DataFrame(Bill_dict).to_csv(filename, index=False)
# Print the Bill_dict to verify the output  

#print(Bill_dict)