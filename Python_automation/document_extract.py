from xml.etree import ElementTree as ET

#Extracted from Bill_Analysits_TBLe
#extreact text from a WordprocessingML document (document.xml) in a .docx file
# Load the uploaded document.xml file
doc_path = "/Users/michaelingram/Documents/GitHub/CA_Bills-1/2025-06-20/dunzipped_lob/word/document.xml"
#Extracted from Bill_Analysits_TBLe
def extract_bill_analysis_text(doc_path):
    """     
    Extracts text from a WordprocessingML document (document.xml) in a .docx file.
    Returns the text as a string.
    """
    # Parse the XML document
    tree = ET.parse(doc_path)
    root = tree.getroot()

    # Define the WordprocessingML namespace
    namespace = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}

    # Extract all text while retaining paragraph structure
    paragraphs = []

    for para in root.findall(".//w:p", namespace):
        runs = para.findall(".//w:t", namespace)
        texts = [run.text for run in runs if run.text]
        if texts:
            paragraphs.append("".join(texts))

    # Join paragraphs with double newlines for formatting
    text_output = "\n\n".join(paragraphs)

    # Preview the first 1500 characters
    print(text_output[:1500])
