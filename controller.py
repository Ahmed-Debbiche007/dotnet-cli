from camel_case import to_camel_case
import os
import re
from utils import find_dotnet_classes_and_enums
from entity import get_primary_key, get_primary_key_name
from find_folder import create_folder

def generate_controller():

    folder_path = "Domain"
    classes, enums = find_dotnet_classes_and_enums(folder_path)

    # Define the file name and new entity name
    filename = 'templates/controller_template.txt'
    attr = get_class_attributes()

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

    generate_create_view(attr)
    generate_edit_view(attr)
    generate_index_view(attr)
    generate_details_view(attr)


def get_class_attributes():
    folder_path = "Domain"
    classes, enums = find_dotnet_classes_and_enums(folder_path)
    class_attributes = {}

    # Regular expression pattern to match attribute usage
    attribute_pattern = r"public\s+(\w+)\s+(\w+)"
    for entity in classes:

        with open("Domain/"+entity+".cs", "r") as file:
            content = file.read()

            # Search for class and attribute matches
            class_matches = re.findall(r"class\s+(\w+)", content)
            attribute_matches = re.findall(attribute_pattern, content)

            for class_name in class_matches:
                # Get attribute list for each class
                attribute_matches = re.findall(attribute_pattern, content)
                attributes = [attribute for attribute in attribute_matches if attribute[0] != 'class' and attribute[0] != 'virtual']
                class_attributes[class_name] = attributes

    return class_attributes


def generate_edit_view(attributes):
    filename = 'templates/views/update.txt'

    for entity in attributes.keys():
        with open(filename, "r") as file:
            content = file.readlines()
        
        create_folder("Views/" + entity)
        modified_content = []
        lines_to_add = ""
        attributs = attributes[entity]

        for data_type, name in attributs:
            lines_to_add += "\t\t\t<div class=\"form-group\">\n"
            lines_to_add += f"\t\t\t\t<label asp-for=\"{name}\" class=\"control-label\"></label>\n"
            lines_to_add += f"\t\t\t\t<input asp-for=\"{name}\" class=\"form-control\" />\n"
            lines_to_add += f"\t\t\t\t<span asp-validation-for=\"{name}\" class=\"text-danger\"></span>\n"
            lines_to_add += "\t\t\t</div>\n"

        for line in content:
            if "{entity}" in line:
                line = line.replace("{entity}",entity)
            if "//form" in line:
                line = lines_to_add + "\n"
            modified_content.append(line)

        with open("Views/" + entity + "/Edit.cshtml", "w") as file:
            file.writelines(modified_content)

def generate_create_view(attributes):
    filename = 'templates/views/create.txt'

    for entity in attributes.keys():
        with open(filename, "r") as file:
            content = file.readlines()
        
        create_folder("Views/" + entity)
        modified_content = []
        lines_to_add = ""
        attributs = attributes[entity]

        for data_type, name in attributs:
            lines_to_add += "\t\t\t<div class=\"form-group\">\n"
            lines_to_add += f"\t\t\t\t<label asp-for=\"{name}\" class=\"control-label\"></label>\n"
            lines_to_add += f"\t\t\t\t<input asp-for=\"{name}\" class=\"form-control\" />\n"
            lines_to_add += f"\t\t\t\t<span asp-validation-for=\"{name}\" class=\"text-danger\"></span>\n"
            lines_to_add += "\t\t\t</div>\n"

        for line in content:
            if "{entity}" in line:
                line = line.replace("{entity}",entity)
            if "//form" in line:
                line = lines_to_add + "\n"
            modified_content.append(line)

        with open("Views/" + entity + "/Create.cshtml", "w") as file:
            file.writelines(modified_content)

def generate_index_view(attributes):
    filename = 'templates/views/index.txt'

    for entity in attributes.keys():
        with open(filename, "r") as file:
            content = file.readlines()
        
        create_folder("Views/" + entity)
        modified_content = []
        head_to_add = ""
        body_to_add = ""
        attributs = attributes[entity]

        for data_type, name in attributs:
            head_to_add += "\t\t\t<th>\n"
            head_to_add += f"\t\t\t\t@Html.DisplayNameFor(model => model.{name})\n"
            head_to_add += "\t\t\t</th>\n"
            body_to_add += "\t\t\t<th>\n"
            body_to_add += f"\t\t\t\t@Html.DisplayNameFor(model => item.{name})\n"
            body_to_add += "\t\t\t</th>\n"

        for line in content:
            if "{entity}" in line:
                line = line.replace("{entity}",entity)
            if "//table_head" in line:
                line = head_to_add + "\n"
            if "//table_body" in line:
                line = body_to_add + "\n"
            if "{PrimaryKey}" in line:
                line = line.replace("{PrimaryKey}",get_primary_key_name(entity))
            modified_content.append(line)

        with open("Views/" + entity + "/Index.cshtml", "w") as file:
            file.writelines(modified_content)

def generate_details_view(attributes):
    filename = 'templates/views/detail.txt'

    for entity in attributes.keys():
        with open(filename, "r") as file:
            content = file.readlines()
        
        create_folder("Views/" + entity)
        modified_content = []
        body_to_add = ""
        attributs = attributes[entity]

        for data_type, name in attributs:
            body_to_add += "\t\t\t<dt class = \"col-sm-2\">\n"
            body_to_add += f"\t\t\t\t@Html.DisplayNameFor(model => model.{name})\n"
            body_to_add += "\t\t\t</dt>\n"
            body_to_add += "\t\t\t<dd class = \"col-sm-2\">\n"
            body_to_add += f"\t\t\t\t@Html.DisplayFor(model => model.{name})\n"
            body_to_add += "\t\t\t</dd>\n"

        for line in content:
            if "{entity}" in line:
                line = line.replace("{entity}",entity)
            if "//data" in line:
                line = body_to_add + "\n"
            if "{PrimaryKey}" in line:
                line = line.replace("{PrimaryKey}",get_primary_key_name(entity))
            modified_content.append(line)

        with open("Views/" + entity + "/Details.cshtml", "w") as file:
            file.writelines(modified_content)

            
            
    