import os
import xml.etree.ElementTree as ET
import pandas as pd

input_path='/Users/michaelingram/Downloads/pubinfo_daily_Wed/BILL_VERSION_TBL_61.lob'
files_to_process = []
if os.path.isdir(input_path):
    files_to_process = [
        os.path.join(input_path, f) for f in os.listdir(input_path) 
        if f.endswith(".xml") or f.endswith(".lob")
    ]
elif os.path.isfile(input_path) and (input_path.endswith(".xml") or input_path.endswith(".lob")):
    files_to_process = [input_path]
else:
    print("Invalid input. Please provide a valid XML file or folder containing XML files.")


# Process each file
for file_path in files_to_process:
    filename = os.path.basename(file_path)
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        #print(root)
    except ET.ParseError as e:
            print(f"Error parsing {filename}: {e}")


#Establish variable
Bill_dict=[]
base=root
ns = {  'caml':'http://lc.ca.gov/legalservices/schemas/caml.1#',
        'xlink':'http://www.w3.org/1999/xlink',
       ' xhtml':'http://www.w3.org/1999/xhtml',
        'xsi':'http://www.w3.org/2001/XMLSchema-instance'}




ID=base.find("./caml:Id",ns).text if base.find("./caml:Id",ns) is not None else None
Action_text=base.find('.//'+name_space+'ActionText').text if base.find('.//'+name_space+'ActionText') is not None else None
Action_Date= base.find('.//'+name_space+'ActionDate').text if base.find('.//'+name_space+'ActionDate') is not None else None
title = base.find("caml:Title", ns).text if base.find("caml:Title", ns) is not None else None
session_year = base.find(".//caml:SessionYear", ns).text if base.find(".//caml:SessionYear", ns) is not None else None
measure_type = base.find(".//caml:MeasureType", ns).text if base.find(".//caml:MeasureType", ns) is not None else None
measurenum = base.find(".//caml:MeasureNum",ns).text if base.find(".//caml:MeasureNum",ns) is not None else None
subject = base.find("caml:Subject", ns).text if base.find("caml:Subject", ns) is not None else None

relatingclause=base.find("./caml:RelatingClause:",ns) if base .find("./caml:RelatingClause",ns) is not None else None
# Author Section
legislator_contribution = base.find(".//caml:Contribution",ns).text if base.find(".//caml:Contribution",ns) is not None else None
house =base.find(".//caml:House",ns).text if base.find(".//caml:House",ns) is not None else None
name = base.find(".//caml:Name",ns).text if base.find(".//caml:Name",ns) is not None else None

digesttext = base.find(".//caml:DigestText",ns).text if base.find(".//caml:DigestTest",ns) is not None else None

Bill_dict.append({
            "Doc_ID": ID,
            "Action_text":Action_text,
            "Action_Date":Action_Date,
            "Title": title,
            "Session Year": session_year,
            "Measure Type": measure_type,
            "Measure Number": measurenum,
            "Subject": subject,
            "Source File": filename,
            "Relating Clause" : relatingclause,
            "Legislator_Contribution": legislator_contribution,
            "House": house,
            "Name": name,
            "Digesgest_Text":digesttext
        })
print(Bill_dict)
            
