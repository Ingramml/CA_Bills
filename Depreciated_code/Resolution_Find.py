import os
import xml.etree.ElementTree as ET
import pandas as pd
from datetime import date
import glob

today=str(date.today())
print(today)

input_path='/Users/michaelingram/Downloads/pubinfo_daily_Sat'

filename = os.path.basename(input_path)
    #print(filename)
    #print(file_path)
tree = ET.parse(input_path)
root = tree.getroot()

base=root[0]
namespace='{http://lc.ca.gov/legalservices/schemas/caml.1#}'

ID=base.find(namespace+'Id').text


Resolution=root.find('.//'+namespace+'Resolution') 


resolution_texts = []
for child in Resolution:
    for subchild in child:
        text = subchild.text
        if text:
            resolution_texts.append(text)

resolution_texts2=[]

#print([elem.text for elem in Resolution.iter()])
for elem in Resolution.iter():
    #print(elem.tag, elem.text)
    if elem.text != None:
        resolution_texts2.append(elem.text)
resolution="".join(resolution_texts2)

print(resolution)


"""
for child in Resolution:
    print(child.tag)
    for subchild in child:
        print(subchild.tag)
        print(subchild.text)
        print(subchild.attrib)"
"""