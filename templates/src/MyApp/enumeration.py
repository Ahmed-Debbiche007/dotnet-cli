import click
import os
import shutil

def generate_enum(enum_name):
    """Generate enum code"""
    values = []
    while True:
        value = click.prompt("Enter enum value (leave empty to finish): ", default='')
        if not value:
            break
        values.append(value)

    # Read the enum template file
    with open("templates/enum_template.txt", "r") as f:
        enum_template = f.read()

    # Replace placeholders in the template with actual values
    enum_code = enum_template.replace("{enum_name}", enum_name)

    values_code = ""
    for value in values:
        values_code += f"        {value},\n"

    enum_code = enum_code.replace("{values}", values_code)

    # Write the generated code to a file
    enum_file_path = os.path.join(f"{enum_name}.cs")
    with open(enum_file_path, "w") as f:
        f.write(enum_code)

    click.echo(f"Generated enum {enum_name} in {enum_file_path}")