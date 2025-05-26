import os
import xml.etree.ElementTree as ET
import pandas as pd

def extract_bill_data(input_path, output_csv):
    """
    Extracts bill data from a single XML file or all XML files in a folder and saves to CSV.

    Parameters:
        input_path (str): Path to a folder or a single XML file.
        output_csv (str): Path to save the extracted data as a CSV file.

    Returns:
        None
    """
    ns = {'caml': 'http://lc.ca.gov/legalservices/schemas/caml.1#'}
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
        return

    # Process each file
    for file_path in files_to_process:
        filename = os.path.basename(file_path)
        try:
            tree = ET.parse(file_path)
            root = tree.getroot()
            print(root)

            # Extract relevant fields
            for bill in root.findall("caml:Bill", ns):
                bill_id = bill.get("id")
                print(bill_id)
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

        except ET.ParseError as e:
            print(f"Error parsing {filename}: {e}")

    # Convert data to DataFrame and save to CSV
    df = pd.DataFrame(bill_data)
    
    df.to_csv(output_csv, index=False)
#print(f"Data successfully saved to {output_csv}")
#print(df)

# Example Usage
input_path = "/Users/michaelingram/Downloads/pubinfo_daily_Wed/BILL_VERSION_TBL_628.lob"  # Replace with the actual file or folder path
output_csv = "/Users/michaelingram/Documents/Coding_Projects/CA_Bills/output.csv"  # Replace with the desired output CSV path

#extract_bill_data(input_path, output_csv)
