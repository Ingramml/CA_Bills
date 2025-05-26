import xml.etree.ElementTree as ET
import pandas as pd
import os

def flatten_dict(d, parent_key='', sep='_'):
    """Flattens a nested dictionary for better CSV formatting."""
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)

def extract_elements(element, namespace=''):
    """Recursively extract XML elements into a nested dictionary."""
    key_elements = {}
    tag_name = element.tag.replace(namespace, '')  # Remove namespace
    
    # If element has text, store it
    text = element.text.strip() if element.text else None
    key_elements[tag_name] = text if text else {}  # Store text or a nested dictionary
    
    # Process child elements recursively
    for child in element:
        child_data = extract_elements(child, namespace)
        
        if isinstance(key_elements[tag_name], dict):
            key_elements[tag_name].update(child_data)
        else:
            key_elements[tag_name] = child_data  # Handle cases where text and children exist
    
    return key_elements

def extract_and_save_to_csv(file_path):
    """Parses an XML file, extracts elements, and saves to a properly formatted CSV file."""
    try:
        # Load and parse the XML file
        tree = ET.parse(file_path)
        root = tree.getroot()

        # Extract namespace from the root tag if present
        namespace = ''
        if '}' in root.tag:
            namespace = root.tag.split('}')[0].strip('{') + '}'  # Extract namespace

        # Extract all elements from the XML
        key_elements = extract_elements(root, namespace)
        flattened_data = flatten_dict(key_elements)  # Flatten nested dictionary

        # Search for "Id" value using an iterative stack-based approach (DFS)
        search_key = "Id"
        bill_id = flattened_data.get(search_key, "Unknown")
        bill_id = bill_id.replace("/", "_").replace("\\", "_")

        # Ensure directory exists
        output_directory = "/Users/michaelingram/Documents/Coding_Projects/CA_Bills/"
        os.makedirs(output_directory, exist_ok=True)

        # Set the final output path
        output_csv_path = os.path.join(output_directory, f"{bill_id}.csv")

        # Convert the extracted key elements to a DataFrame and save to CSV
        df = pd.DataFrame([flattened_data])
        df.to_csv(output_csv_path, index=False, encoding="utf-8")

        print(f"CSV saved successfully: {output_csv_path}")
        return output_csv_path

    except ET.ParseError as e:
        return f"XML Parsing Error: {e}"
    except Exception as e:
        return f"Unexpected Error: {e}"

# Example usage
xml_file = "/Users/michaelingram/Downloads/pubinfo_daily_Wed/BILL_VERSION_TBL_675.lob"
csv_path = extract_and_save_to_csv(xml_file)
print(csv_path)  # Prints the saved CSV path

