import xml.etree.ElementTree as ET
import pandas as pd

# Function to extract key elements from XML and save as CSV
def extract_and_save_to_csv(file_path):
    try:
        # Load and parse the XML file
        tree = ET.parse(file_path)
        root = tree.getroot()

        # Extract namespace from the root tag
        namespace = root.tag.split('}')[0].strip('{') + '}'  # Ensure correct formatting

        # Extract key elements into a dictionary
        key_elements = {}
        for element in root.iter():
            tag_name = element.tag.replace(namespace, '')  # Remove namespace for readability
            key_elements[tag_name] = element.text.strip() if element.text else None

        # Use the "Id" element as the filename (sanitizing it for safety)
        fixed_keys_data = {key.strip('{'): value for key, value in key_elements.items()}
        bill_id = fixed_keys_data.get("Id", "Unknown")
        print(bill_id)
        file_id = key_elements.get("Id", "exported_data").replace("/", "_").replace("\\", "_")
        filename=key_elements.get("Id")
        #print(key_elements)
        output_csv_path = f"/Users/michaelingram/Documents/Coding_Projects/CA_Bills/{bill_id}.csv"

        # Convert the extracted key elements to a DataFrame and save to CSV
        df = pd.DataFrame([key_elements])
        df.to_csv(output_csv_path, index=False, encoding="utf-8")
        
        # Return the path to the saved CSV file
        return output_csv_path

    except ET.ParseError as e:
        return f"XML Parsing Error: {e}"

# Example Usage
file_path = "/Users/michaelingram/Downloads/pubinfo_daily_Wed/BILL_VERSION_TBL_650.lob"  # Replace with the path to your XML file
output_csv_path = extract_and_save_to_csv(file_path)

output_csv_path
