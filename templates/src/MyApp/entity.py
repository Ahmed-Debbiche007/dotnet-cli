import click
import os
def generate_entity(entity_name):
    """Generate entity code"""
    net_data_types = ['boolean', 'double', 'int', 'string', 'DateTime', 'relation']
    associations = ['OneToOne', 'OneToMany', 'ManyToOne', 'ManyToMany', 'SponsoringAssociation']
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
        
        # Prompt for relation type and validate input
        if attribute_type == 'relation':
            while True:
                relation_type = input(f"Enter relation type ({', '.join(associations)}):\n")
                if relation_type in associations:
                    break
                else:
                    print(f"Invalid relation type '{relation_type}', please try again.")
            related_entity = input("Enter related entity name: ")
            relations.append((relation_type, related_entity))
        else:
            attributes.append((attribute, attribute_type))
        
        # Prompt the user to add another attribute
        add_another = input("Do you want to add another attribute?")
        if add_another == 'n':
            break
        
    # Read the template file
    with open("entity_template.txt", "r") as f:
        entity_template = f.read()

    # Replace placeholders in the template with actual values
    entity_code = entity_template.replace("{entity_name}", entity_name)

    attributes_code = ""
    for attribute, attribute_type in attributes:
        attributes_code += f"        public {attribute_type} {attribute} {{ get; set; }}\n"

    relations_code = ""
    for relation_type, related_entity in relations:
        relations_code += f"        public int {related_entity}Fk {{ get; set; }}\n        [ForeignKey(\"{related_entity}Fk\")]\n        public virtual {related_entity} {related_entity} {{ get; set; }}\n"

    entity_code = entity_code.replace("{attributes}", attributes_code)
    entity_code = entity_code.replace("{relations}", relations_code)

    # Write the generated code to a file
    entity_file_path = os.path.join('Domain',f"{entity_name}.cs")
    with open(entity_file_path, "w") as f:
        f.write(entity_code)

    click.echo(f"Generated entity {entity_name} in {entity_file_path}")




