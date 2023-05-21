import click
import os
import re

from configuration import generate_sponsoring_association, generate_key, generate_many_to_one, generate_many_to_many, generate_inheritance_tph, generate_inheritance_tpt
from utils import insert_lines_v2, insert_lines, get_key


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
    

    is_sponsor = False
    relations_code = ""
    for relation_type, related_entity, *other_entities in relations:
        attribute,primary_key=attributes[0]
        if relation_type == "SponsoringAssociation":
            is_sponsor = True
            related_entity2 = other_entities[0]
            result, result_property = generate_associations(entity1=entity_name,primary_key=primary_key, entity2=related_entity, association=relation_type, entity3=related_entity2)
            relations_code += result_property
        else:
            result, result_property = generate_associations(entity1=entity_name,primary_key=primary_key, entity2=related_entity, association=relation_type)
            relations_code += result_property

    if attributes:
        attribute, attribute_type = attributes[0]
        if 'id' in attribute.lower():
            entity_code = entity_template.replace("{entity_name}", entity_name)
            attributes_code = f"        public {attribute_type} {attribute} {{ get; set; }}\n"
        elif (is_sponsor == False):
            inherits = input ("Does this entity inherits another entity? (y/n)\n")
            if (inherits == "y") or (inherits == "yes"):
                entity_code = entity_template.replace("{entity_name}", generate_inheritance(entity_name))
                attributes_code = f"        public {attribute_type} {attribute} {{ get; set; }}\n"
            else:
                entity_code = entity_template.replace("{entity_name}", entity_name)
                is_fluent=input("Do you want the priamry key to be configured with Fluent API?\n")
                
                if is_fluent == "y" or is_fluent == "yes":
                    generate_key(entity_name, attribute)
                    attributes_code = f"        public {attribute_type} {attribute} {{ get; set; }}\n"
                else:
                    attributes_code = f"        [Key]\n        public {attribute_type} {attribute} {{ get; set; }}\n"  
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
    insert_lines_v2("// Add DBsets Here", dbSet, "Configurations/ExamContext.cs")
    click.echo(f"Generated entity {entity_name} in {entity_file_path}")


def generate_associations(entity1, primary_key, entity2, association, entity3=None):

    primary_key_type = get_primary_key(entity2)
    if association == "OneToOne":
        entity1_property = f"        public {primary_key_type} {entity2}Fk {{ get; set; }}\n        [ForeignKey(\"{entity2}Fk\")]\n        public virtual {entity2} {entity2} {{ get; set; }}\n"
        entity2_property = f"        public {primary_key} {entity1}Fk {{ get; set; }}\n        [ForeignKey(\"{entity1}Fk\")]\n        public virtual {entity1} {entity1} {{ get; set; }}\n"
    if (association == "OneToMany"):
        entity1_property = f"        public virtual IList<{entity2}> {entity2}s{{ get; set; }}\n"
        entity2_property = f"        public {primary_key} {entity1}Fk {{ get; set; }}\n        [ForeignKey(\"{entity1}Fk\")]\n        public virtual {entity1} {entity1} {{ get; set; }}\n"
        generate_many_to_one(entity2, entity1)
    if (association == "ManyToOne"):
        entity1_property = f"        public {primary_key_type} {entity2}Fk {{ get; set; }}\n        [ForeignKey(\"{entity2}Fk\")]\n        public virtual {entity2} {entity2} {{ get; set; }}\n"
        entity2_property = f"        public virtual IList<{entity1}> {entity1}s{{ get; set; }}\n"
        generate_many_to_one(entity1, entity2)
        
    if (association == "ManyToMany"):
        entity1_property = f"        public virtual IList<{entity2}> {entity2}s{{ get; set; }}\n"
        entity2_property = f"        public virtual IList<{entity1}> {entity1}s{{ get; set; }}\n"
        generate_many_to_many(entity1,entity2)
        
    if (association == "SponsoringAssociation"):
        primary_key_type_entity_3 = get_primary_key(entity3)
        entity1_property = f"        public virtual {entity2} {entity2} {{ get; set; }}\n"
        entity1_property+= f"        public virtual {entity3} {entity3} {{ get; set; }}\n"
        entity2_property = f"        public virtual IList<{entity1}> {entity1}s{{ get; set; }}\n"
        entity3_property = f"        public virtual IList<{entity1}> {entity1}s{{ get; set; }}\n"
        insert_lines(entity3,'}',entity3_property,f"Domain/{entity3}.cs")
        generate_sponsoring_association(entity1, primary_key, entity2, entity3)
    insert_lines(entity2,'}',entity2_property,f"Domain/{entity2}.cs")
    return (entity1, entity1_property)



def get_primary_key(entity_name):
    file_path = f"Domain/{entity_name}.cs"
    with open(file_path, "r") as f:
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
        else:
            return (get_key(file_path)).strip().split(" ")[1]

        i += 1

def get_primary_key_name(entity_name):
    file_path = f"Domain/{entity_name}.cs"
    with open(file_path, "r") as f:
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
        else:
            return (get_key(file_path)).strip().split(" ")[2]

        i += 1



def generate_inheritance(entity_name):
    inherited_entity = input("What entity Does it inherit?\n")
    while True:
        if os.path.isfile(f"Domain/{inherited_entity}.cs"):
            break
        else:
            inherited_entity = input("Are you sure? Retype the inherited entity name:\n")
    while True:
        method = input ("TPT/TPH?\n")
        if (method == "TPT"):
            generate_inheritance_tpt(inherited_entity, entity_name)
            break
        if (method == "TPH"):
            generate_inheritance_tph(inherited_entity, entity_name)
            break
        else:
            method = input("Sorry, But TPT or TPH ?\n")
    return f"{entity_name}:{inherited_entity}"

