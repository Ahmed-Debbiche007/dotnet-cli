from camel_case import to_camel_case
import os
from utils import find_dotnet_classes_and_enums
from entity import get_primary_key

def generate_controller():

    folder_path = "Domain"
    classes, enums = find_dotnet_classes_and_enums(folder_path)

    # Define the file name and new entity name
    filename = 'templates/controller_template.txt'
    

    for entity in classes:
        # Read the original file content
        with open(filename, 'r') as f:
            file_content = f.read()

        # Replace all occurrences of '{entity}' with the new entity name

        new_file_content = file_content.replace('{entity}', entity)
        new_file_content = new_file_content.replace('{data_type}', get_primary_key(entity))

        # Define the new file name
        new_filename = os.path.join("Controllers",f"{to_camel_case(entity)}Controller.cs")

        # Write the updated file content to the new file
        with open(new_filename, 'w') as f:
            f.write(new_file_content)
