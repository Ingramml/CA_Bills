import xml.etree.ElementTree as ET
import pandas as pd
import os

def extract_elements(element, namespace=''):
    """Recursively extract XML elements into a nested dictionary."""
    key_elements = {}
    tag_name = element.tag.replace(namespace, '')  # Remove namespace
    # If element has text, store it
    text = element.text.strip() if element.text else None
    key_elements[tag_name] = text if text else {}  # Store text or a nested dictionary
    # Process child elements
    for child in element:
        child_data = extract_elements(child, namespace)
        
        if isinstance(key_elements[tag_name], dict):
            key_elements[tag_name].update(child_data)
        else:
            key_elements[tag_name] = child_data  # Handle cases where text and children exist
    
    return key_elements


def extract_and_save_to_csv(file_path):
    """Parses an XML file, extracts elements, and saves to a CSV file."""
    try:
        # Load and parse the XML file
        tree = ET.parse(file_path)
        root = tree.getroot()

        # Extract namespace from the root tag if present
        namespace = ''
        if '}' in root.tag:
            namespace = root.tag.split('}')[0].strip('{') + '}'  # Extracts namespace

        # Extract all elements from the XML
        key_elements = extract_elements(root, namespace)

        # Fix namespace keys to remove unwanted characters
        fixed_keys_data = {key.replace(namespace, ''): value for key, value in key_elements.items()}

        """ # Determine a valid file name
        fixed_keys_data = {key.strip('{'): value for key, value in key_elements.items()}
        bill_id = fixed_keys_data.get("Id", "Unknown")
        """
       

        # Assume key_elements is already extracted from the XML
        search_key = "Id"
        found_value = None  # Default value if not found

        # Use a stack-based approach (Iterative DFS) to search for the key in a nested dictionary
        stack = [key_elements]  # Start with the main dictionary

        while stack:
            current_dict = stack.pop()
        
        if isinstance(current_dict, dict):
            for key, value in current_dict.items():
                if key.strip('{') == search_key:  # Remove braces from key and check match
                    found_value = value
                    break  # Stop searching once found
                elif isinstance(value, dict):  # If value is a dict, add it to stack
                    stack.append(value)
                elif isinstance(value, list):  # If value is a list, check each item
                    stack.extend(value)

        # Print the extracted ID
        print('Id":'+str(found_value))  # Outputs: '20250AB__024799INT' (or None if not found)
        

        # Ensure directory exists
        output_directory = "/Users/michaelingram/Documents/Coding_Projects/CA_Bills/"
        os.makedirs(output_directory, exist_ok=True)

        # Set the final output path
        output_csv_path = os.path.join(output_directory, f"{found_value}.csv")

        # Convert the extracted key elements to a DataFrame and save to CSV
        df = pd.DataFrame([fixed_keys_data])
        #df.to_csv(output_csv_path, index=False, encoding="utf-8")

        #print(f"CSV saved successfully: {output_csv_path}")
        
        return output_csv_path

    except ET.ParseError as e:
        return f"XML Parsing Error: {e}"
    except Exception as e:
        return f"Unexpected Error: {e}"
    

xml_file = "/Users/michaelingram/Downloads/pubinfo_daily_Wed/BILL_VERSION_TBL_675.lob"
csv_path = extract_and_save_to_csv(xml_file)
print(csv_path)  # Prints the saved CSV path

