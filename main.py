import sys
import os

from entity import generate_entity
from enumeration import generate_enum 
from service import generate_service
from interface import generate_interface

def generate(entity_name, is_enum, is_entity):
    """Generate code"""
    if is_enum:
        generate_enum(entity_name)
    if is_entity:
        generate_entity(entity_name)
        generate_service(entity_name)
        generate_interface(entity_name)
        


if __name__ == '__main__':
    if (sys.argv[1]=="generate"):
        name = sys.argv[2]
        is_enum = False
        is_entity = False
        if len(sys.argv) > 3 and sys.argv[3] == "--enum":
            is_enum = True
        if len(sys.argv) > 3 and sys.argv[3] == "--entity":
            is_entity = True
        generate(name, is_enum, is_entity)
