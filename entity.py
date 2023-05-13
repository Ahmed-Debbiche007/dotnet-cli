import click
import os
import re
associations = ['OneToOne', 'OneToMany', 'ManyToOne', 'ManyToMany', 'SponsoringAssociation']
net_data_types = ['boolean', 'double', 'int', 'string', 'DateTime', 'relation', 'Enum']
def generate_entity(entity_name):
    """Generate entity code"""
    attributes = []
    relations = []
    while True:
        attribute = input("Enter attribute name (leave empty to finish):\n")
        if not attribute:
            break
        # Prompt for attribute type and validate input
        while True:
            attribute_type = input(f"Enter attribute type ({', '.join(net_data_types)}):\n")
            if attribute_type in net_data_types:
                break
            else:
                print(f"Invalid attribute type '{attribute_type}', please try again.")
        if attribute_type == 'Enum':
            attribute_type = input("Enter the enum Name: \n")
        # Prompt for relation type and validate input
        if attribute_type == 'relation':
            while True:
                relation_type = input(f"Enter relation type ({', '.join(associations)}):\n")
                if relation_type in associations:
                    break
                else:
                    print(f"Invalid relation type '{relation_type}', please try again.")
            if relation_type == "SponsoringAssociation":
                related_entity = input("Enter first related entity name: ")
                related_entity2 = input("Enter second related entity name: ")
                relations.append((relation_type, related_entity, related_entity2))
            else:
                related_entity = input("Enter related entity name: ")
                relations.append((relation_type, related_entity))

        else:
            attributes.append((attribute, attribute_type))
        
        # Prompt the user to add another attribute
        add_another = input("Do you want to add another attribute?")
        if add_another == 'n':
            break
        
    # Read the template file
    with open("templates/entity_template.txt", "r") as f:
        entity_template = f.read()

    # Replace placeholders in the template with actual values
    entity_code = entity_template.replace("{entity_name}", entity_name)


    relations_code = ""
    for relation_type, related_entity, *other_entities in relations:
        attribute,primary_key=attributes[0]
        if relation_type == "SponsoringAssociation":
            related_entity2 = other_entities[0]
            result, result_property = generate_associations(entity1=entity_name,primary_key=primary_key, entity2=related_entity, association=relation_type, entity3=related_entity2)
            relations_code += result_property
        else:
            result, result_property = generate_associations(entity1=entity_name,primary_key=primary_key, entity2=related_entity, association=relation_type)
            relations_code += result_property

    if attributes:
        attribute, attribute_type = attributes[0]
        if 'id' in attribute_type or 'Id' in attribute_type or 'ID' in attribute_type:
            attributes_code = f"        public {attribute_type} {attribute} {{ get; set; }}\n"
        else:
            is_fluent=input("Do you want the priamry key to be configured with Fluent API?")
            is_fluent = bool(is_fluent)
            if is_fluent:
                pass
            else:
                attributes_code = f"        \[Key\]\n        public {attribute_type} {attribute} {{ get; set; }}\n"  

        # Generate code for remaining attributes
        for attribute, attribute_type in attributes[1:]:
            attributes_code += f"        public {attribute_type} {attribute} {{ get; set; }}\n"

    entity_code = entity_code.replace("{attributes}", attributes_code)
    entity_code = entity_code.replace("{relations}", relations_code)

    # Write the generated code to a file
    entity_file_path = os.path.join('Domain',f"{entity_name}.cs")
    with open(entity_file_path, "w") as f:
        f.write(entity_code)
    
    dbSet = [f"\t\tpublic DbSet<{entity_name}> {entity_name}s {{ get; set; }}\n"]
    insert_lines_v2("// Add DBsets Here", dbSet)
    click.echo(f"Generated entity {entity_name} in {entity_file_path}")


def generate_associations(entity1, primary_key, entity2, association, entity3=None):

    primary_key_type = get_primary_key(entity2)
    if association == "OneToOne":
        entity1_property = f"        public {primary_key_type} {entity2}Fk {{ get; set; }}\n        [ForeignKey(\"{entity2}Fk\")]\n        public virtual {entity2} {entity2} {{ get; set; }}\n"
        entity2_property = f"        public {primary_key} {entity1}Fk {{ get; set; }}\n        [ForeignKey(\"{entity1}Fk\")]\n        public virtual {entity1} {entity1} {{ get; set; }}\n"
    if (association == "OneToMany"):
        entity1_property = f"        public virtual IList<{entity2}> {entity2}{{ get; set; }}\n"
        entity2_property = f"        public {primary_key} {entity1}Fk {{ get; set; }}\n        [ForeignKey(\"{entity1}Fk\")]\n        public virtual {entity1} {entity1} {{ get; set; }}\n"
    if (association == "ManyToOne"):
        entity1_property = f"        public {primary_key_type} {entity2}Fk {{ get; set; }}\n        [ForeignKey(\"{entity2}Fk\")]\n        public virtual {entity2} {entity2} {{ get; set; }}\n"
        entity2_property = f"        public virtual IList<{entity1}> {entity1}{{ get; set; }}\n"
        
    if (association == "ManyToMany"):
        entity1_property = f"        public virtual IList<{entity2}> {entity2}{{ get; set; }}\n"
        entity2_property = f"        public virtual IList<{entity1}> {entity1}{{ get; set; }}\n"
    if (association == "SponsoringAssociation"):
        primary_key_type_entity_3 = get_primary_key(entity3)
        entity1_property = f"        public virtual {entity2} {entity2} {{ get; set; }}\n"
        entity1_property+= f"        public virtual {entity3} {entity3} {{ get; set; }}\n"
        entity2_property = f"        public virtual IList<{entity1}> {entity1}{{ get; set; }}\n"
        entity3_property = f"        public virtual IList<{entity1}> {entity1}{{ get; set; }}\n"
        insert_lines(entity3,'}',entity3_property)
    insert_lines(entity2,'}',entity2_property)
    return (entity1, entity1_property)



def get_primary_key(entity_name):
    with open(f"Domain/{entity_name}.cs", "r") as f:
        entity = f.readlines()
    # Check if the primary key is annotated with [Key]
    results = []
    i = 0
    while i < len(entity):
        line = entity[i]

        if '[Key]' in line:
            if i+1 < len(entity):
                words = entity[i+1].strip().split()
                return words[1]
        
        elif 'id' in line or 'Id' in line or 'ID' in line:
            words = line.strip().split()
            return words[1]

        i += 1

def insert_lines(entity,keyword, code):
    # Read in the file as a list of lines
    with open(f"Domain/{entity}.cs", "r") as f:
        lines = f.readlines()

    # Find the index of the second-to-last closing brace
    last_brace_index = len(lines) - 1
    second_last_brace_index = None
    brace_count = 0
    for i in range(len(lines)-1, -1, -1):
        line = lines[i]
        brace_count += line.count(keyword)
        if brace_count == 2:
            second_last_brace_index = i
            break
        elif brace_count > 2:
            last_brace_index = i

    # Insert the lines to be added before the second-to-last closing brace
    if second_last_brace_index is not None:
        lines[second_last_brace_index:second_last_brace_index] = code
    else:
        lines[last_brace_index:last_brace_index] = code

    # Write the modified lines back to the file
    with open(f"Domain/{entity}.cs", "w") as f:
        f.writelines(lines)


def insert_lines_v2(keyword, lines_to_add):
    # Read in the file as a list of lines
    with open("Configurations/ExamContext.cs", "r") as f:
        lines = f.readlines()

    # Find the index of the line containing the keyword
    keyword_index = None
    for i, line in enumerate(lines):
        if keyword in line:
            keyword_index = i
            break

    # If the keyword is found, insert the lines before it
    if keyword_index is not None:
        lines = lines[:keyword_index] + lines_to_add + lines[keyword_index:]

    # Write the modified lines back to the file
    with open("Configurations/ExamContext.cs", "w") as f:
        f.writelines(lines)


