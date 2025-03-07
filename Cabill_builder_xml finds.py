import os
import xml.etree.ElementTree as ET
import pandas as pd



input_path='/Users/michaelingram/Downloads/pubinfo_daily_Wed/BILL_VERSION_TBL_628.lob'
ns = {  'caml':'http://lc.ca.gov/legalservices/schemas/caml.1#',
        'xlink':'http://www.w3.org/1999/xlink',
       ' xhtml':'http://www.w3.org/1999/xhtml',
        'xsi':'http://www.w3.org/2001/XMLSchema-instance'}
bill_data = []

    # Determine if input is a folder or a single file
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
    tree = ET.parse(file_path)
    root = tree.getroot()
    #print(root[0][0].text)
"""
for child in root:
    print(child.tag, child.attrib)
    with open('output.txt', 'w') as f:
        print(root.attrib, file=f)
"""    
#print(root[0][2].tag)

base=root[0]
namespace='{http://lc.ca.gov/legalservices/schemas/caml.1#}'
Id=base.find(namespace+'Id')
print('ID:'+Id.text)
History=base.find(namespace+'History')
print(History.text)
Actiontext =base.find('.//'+namespace+'ActionText')
print('Action Text:'+Actiontext.text)
Actiondate=base.find('.//'+namespace+'ActionDate')
print('Action Date:'+Actiondate.text)

title = base.find("caml:Title", ns).text if base.find("caml:Title", ns) is not None else None
print('Title:'+title)

session_year = base.find(".//caml:SessionYear", ns).text if root[0].find("caml:SessionYear", ns) is not None else None
print(session_year)

session_number =  base.find(".//caml:SessionNum", ns).text if root[0].find("caml:SessionNum", ns) is not None else None
print('Session Number:'+session_number)


#Description=root.find('http://lc.ca.gov/legalservices/schemas/caml.1#}Description')
#print(Description)

"""
    # Extract relevant fields
    for bill in root.findall("caml:Bill", ns):
        bill_id = bill.get("id")  # Attribute extraction
        title = bill.find("caml:Title", ns).text if bill.find("caml:Title", ns) is not None else None
        session_year = root.find("caml:SessionYear", ns).text if root.find("caml:SessionYear", ns) is not None else None
        measure_type = root.find("caml:MeasureType", ns).text if root.find("caml:MeasureType", ns) is not None else None
        subject = root.find("caml:Subject", ns).text if root.find("caml:Subject", ns) is not None else None

        bill_data.append({
            "Bill ID": bill_id,
            "Title": title,
            "Session Year": session_year,
            "Measure Type": measure_type,
            "Subject": subject,
            "Source File": filename
        })
        """
#df = pd.DataFrame(bill_data)
#print(df)