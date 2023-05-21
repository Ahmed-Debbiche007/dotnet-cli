import sys
import os
import re

from entity import generate_entity, get_primary_key
from enumeration import generate_enum 
from service import generate_service
from interface import generate_interface
from controller import generate_controller

def generate(entity_name, is_enum, is_entity):
    """Generate code"""
    if is_enum:
        generate_enum(entity_name)
    if is_entity:
        generate_entity(entity_name)
        generate_service(entity_name)
        generate_interface(entity_name)
        

def get_attribute_data_types(cs_file_path):
    # Define a regular expression to match attribute declarations
    attribute_regex = r'\[.*\]\s*(public|private|protected)?\s*(static)?\s*(\w+)\s+(\w+)'

    # Read the file and search for attribute declarations
    with open(cs_file_path) as f:
        file_contents = f.read()
        matches = re.findall(attribute_regex, file_contents)

    # Extract the data types from the attribute declarations
    data_types = {}
    for match in matches:
        access_modifier, is_static, data_type, attribute_name = match
        if data_type not in data_types:
            data_types[data_type] = set()
        data_types[data_type].add(attribute_name)

    return data_types

if __name__ == '__main__':
    # print(get_attribute_data_types('./Domain/Patient.cs'))
    if (sys.argv[1]=="generate"):
        name = sys.argv[2]
        is_enum = False
        is_entity = False
        if len(sys.argv) > 3 and sys.argv[3] == "--enum":
            is_enum = True
        if len(sys.argv) > 3 and sys.argv[3] == "--entity":
            is_entity = True
        generate(name, is_enum, is_entity)
    if (sys.argv[1]=="mvc"):
        generate_controller()
    
    

