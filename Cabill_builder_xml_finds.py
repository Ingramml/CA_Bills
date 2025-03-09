import os
import xml.etree.ElementTree as ET
import pandas as pd
from datetime import date
import glob
import shutil

today=str(date.today())
print(today)

input_path='/Users/michaelingram/Downloads/pubinfo_daily_Sat'
ns = {  'caml':'http://lc.ca.gov/legalservices/schemas/caml.1#',
        'xlink':'http://www.w3.org/1999/xlink',
       ' xhtml':'http://www.w3.org/1999/xhtml',
        'xsi':'http://www.w3.org/2001/XMLSchema-instance'}
bill_data = {}

    # Determine if input is a folder or a single file
files_to_process = []
if os.path.isdir(input_path):
        files_to_process = [
            os.path.join(input_path, f) for f in os.listdir(input_path) 
            if f.endswith(".xml") or f.endswith(".lob") and f.startswith("BILL_VERSION_TBL_")
        ]
elif os.path.isfile(input_path) and (input_path.endswith(".xml") or input_path.endswith(".lob")):
        files_to_process = [input_path]
else:
    print("Invalid input. Please provide a valid XML file or folder containing XML files.")

bill_data=[]
    # Process each file
for file_path in files_to_process:
    filename = os.path.basename(file_path)
    #print(filename)
    #print(file_path)
    tree = ET.parse(file_path)
    root = tree.getroot()
    
    base=root[0]
    namespace='{http://lc.ca.gov/legalservices/schemas/caml.1#}'
    Id=base.find(namespace+'Id').text.replace("__", "")
    #print('ID:'+Id)
    History=base.find(namespace+'History')
    #print(History)
    Actiontext =base.find('.//'+namespace+'ActionText')
    #print('Action Text:'+Actiontext.text)
    Actiondate=base.find('.//'+namespace+'ActionDate')
    #print('Action Date:'+Actiondate.text)

    title = base.find("caml:Title", ns).text if base.find("caml:Title", ns) is not None else None
    #print('Title:'+title)

    session_year = base.find('.//'+namespace+'SessionYear', ns).text if root[0].find('.//'+namespace+'SessionYear', ns) is not None else None
    #print("Session Year "+ str(session_year))

    session_number =  base.find('.//'+namespace+'SessionNum', ns).text if root[0].find('.//'+namespace+'SessionNum', ns) is not None else None
    #print('Session Number:'+session_number)

    digesttext =  base.find('./'+namespace+'DigestText/*').text if base.find('./'+namespace+'DigestText/*') is not None else None
    #print('Digest Text :'+ str(digesttext))
    
    #Replaces digtest text with resolution text if digest text is None)
    if digesttext is None:
         Resolution=root.find('.//'+namespace+'Resolution')
         resolution_texts = []
         for elem in Resolution.iter():
            #print(elem.tag, elem.text)
            if elem.text != None:
                resolution_texts.append(elem.text)
            resolution="".join(resolution_texts)
            digesttext=resolution
    
    bill_data.append({
            "Bill ID": Id,
            "Title": title,
            "Session Year": session_year,
            "Source File": filename,
            "Digesgt Text": digesttext
        })

df=pd.DataFrame.from_dict(bill_data)



output_path=(today+'CSV')
print(output_path)
if os.path.isdir(output_path) is True:
   shutil.rmtree(output_path)
else:
    os.makedirs(today+'CSV',exist_ok=False)
#print('Output:'+ output)
csv_name=output_path+'/bill_data.csv'
print(csv_name)
df.to_csv(csv_name,index=False)