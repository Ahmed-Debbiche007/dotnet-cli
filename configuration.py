from camel_case import to_camel_case
import os
from utils import insert_lines_v2

def generate_key(entity,key):
    filename = 'templates/configuration_template.txt'

    with open(filename, 'r') as f:
        file_content = f.read()
    
    config = f"\t\tbuilder.HasKey(p => p.{key})"
    new_file_content = file_content.replace('{entity}', entity)
    new_file_content = file_content.replace('{config}', config)
    new_filename = os.path.join('Configurations',f"{to_camel_case(entity)}Configuration.cs")

    # Write the updated file content to the new file
    with open(new_filename, 'w') as f:
        f.write(new_file_content)
        

def generate_sponsoring_association(entity1, primary_key, entity2, entity3):
    filename = 'templates/configuration_template.txt'

    with open(filename, 'r') as f:
        file_content = f.read()

    sponsoring_config=f"\t\tbuilder.HasOne(p => p.{entity2})\n"
    sponsoring_config+=f"\t\t\t.WithMany(p => p.{entity1}s)\n"
    sponsoring_config+=f"\t\t\t.HasForeignKey(p => p.{entity2}Fk)\n"
    sponsoring_config+=f"\t\t\t.OnDelete(DeleteBehavior.Restrict);\n\n"

    sponsoring_config+=f"\t\tbuilder.HasOne(p => p.{entity3})\n"
    sponsoring_config+=f"\t\t\t.WithMany(p => p.{entity1}s)\n"
    sponsoring_config+=f"\t\t\t.HasForeignKey(p => p.{entity3}Fk)\n"
    sponsoring_config+=f"\t\t\t.OnDelete(DeleteBehavior.Restrict);\n\n"


    sponsoring_config+="\t\tbuilder.HasKey(p => new {\n"
    sponsoring_config+=f"\t\t\tp.{entity2}FK,\n"
    sponsoring_config+=f"\t\t\tp.{entity3}Fk,\n"
    sponsoring_config+=f"\t\t\tp.{primary_key}\n"
    sponsoring_config+="\t\t});\n\n"

    # Replace all occurrences of '{entity}' with the new entity name
    new_file_content = file_content.replace('{entity}', entity1)
    new_file_content = file_content.replace('{config}', sponsoring_config)

    # Define the new file name
    new_filename = os.path.join('Configurations',f"{to_camel_case(entity1)}Configuration.cs")
    if (os.path.isfile(new_filename)):
        insert_lines_v2("//add config", sponsoring_config, new_filename)
    # Write the updated file content to the new file
    else:
        with open(new_filename, 'w') as f:
            f.write(new_file_content)


def generate_many_to_one(entity1, entity2):
    filename = 'templates/configuration_template.txt'

    with open(filename, 'r') as f:
        file_content = f.read()

    sponsoring_config=f"\t\tbuilder.HasOne(p => p.{entity2})\n"
    sponsoring_config+=f"\t\t\t.WithMany(p => p.{entity1}s)\n"
    sponsoring_config+=f"\t\t\t.HasForeignKey(p => p.{entity2}Fk)\n"
    sponsoring_config+=f"\t\t\t.OnDelete(DeleteBehavior.Restrict);\n\n"

    

    # Replace all occurrences of '{entity}' with the new entity name
    new_file_content = file_content.replace('{entity}', entity1)

    # Define the new file name
    new_filename = os.path.join('Configurations',f"{to_camel_case(entity1)}Configuration.cs")

    # Write the updated file content to the new file
    if (os.path.isfile(new_filename)):
        insert_lines_v2("//add config", sponsoring_config, new_filename)
    # Write the updated file content to the new file
    else:
        with open(new_filename, 'w') as f:
            f.write(new_file_content)
    
    insert_lines_v2("//add config", sponsoring_config, new_filename)

def generate_many_to_many(entity1, entity2):
    filename = 'templates/configuration_template.txt'

    with open(filename, 'r') as f:
        file_content = f.read()

    sponsoring_config=f"\t\tbuilder.HasMany(p => p.{entity2}s)\n"
    sponsoring_config+=f"\t\t\t.WithMany(p => p.{entity1}s)\n"
    sponsoring_config+=f"\t\t\tUsingEntity(j => j.ToTable(\"{entity1}{entity2}\"))\n\n"


    # Replace all occurrences of '{entity}' with the new entity name
    new_file_content = file_content.replace('{entity}', entity1)

    # Define the new file name
    new_filename = os.path.join('Configurations',f"{to_camel_case(entity1)}Configuration.cs")

    # Write the updated file content to the new file
    if (os.path.isfile(new_filename)):
        insert_lines_v2("//add config", sponsoring_config, new_filename)
    # Write the updated file content to the new file
    else:
        with open(new_filename, 'w') as f:
            f.write(new_file_content)