from camel_case import to_camel_case
import os
def generate_interface(name):
    # Define the file name and new entity name
    filename = 'templates/interface_template.txt'
    

    # Read the original file content
    with open(filename, 'r') as f:
        file_content = f.read()

    # Replace all occurrences of '{entity}' with the new entity name
    new_file_content = file_content.replace('{entity}', name)

    # Define the new file name
    new_filename = os.path.join('Interfaces',f"IService{to_camel_case(name)}.cs")

    # Write the updated file content to the new file
    with open(new_filename, 'w') as f:
        f.write(new_file_content)
