from camel_case import to_camel_case
import os
from utils import insert_lines_v2, string_exists_in_file, replace_tph_config


def generate_key(entity, key):
    filename = 'templates/configuration_template.txt'
    new_filename = os.path.join('Configurations', f"{to_camel_case(entity)}Configuration.cs")
    config = f"\t\tbuilder.HasKey(p => p.{key}); \n\n"
    insert_config_to_file(entity, config, filename, new_filename)


def generate_sponsoring_association(entity1, primary_key, entity2, entity3):
    filename = 'templates/configuration_template.txt'
    new_filename = os.path.join('Configurations', f"{to_camel_case(entity1)}Configuration.cs")

    sponsoring_config = f"\t\tbuilder.HasOne(p => p.{entity2})\n"
    sponsoring_config += f"\t\t\t.WithMany(p => p.{entity1}s)\n"
    sponsoring_config += f"\t\t\t.HasForeignKey(p => p.{entity2}Fk)\n"
    sponsoring_config += f"\t\t\t.OnDelete(DeleteBehavior.Restrict);\n\n"

    sponsoring_config += f"\t\tbuilder.HasOne(p => p.{entity3})\n"
    sponsoring_config += f"\t\t\t.WithMany(p => p.{entity1}s)\n"
    sponsoring_config += f"\t\t\t.HasForeignKey(p => p.{entity3}Fk)\n"
    sponsoring_config += f"\t\t\t.OnDelete(DeleteBehavior.Restrict);\n\n"

    sponsoring_config += "\t\tbuilder.HasKey(p => new {\n"
    sponsoring_config += f"\t\t\tp.{entity2}FK,\n"
    sponsoring_config += f"\t\t\tp.{entity3}Fk,\n"
    sponsoring_config += f"\t\t\tp.{primary_key}\n"
    sponsoring_config += "\t\t});\n\n"

    insert_config_to_file(entity1, sponsoring_config, filename, new_filename)


def generate_many_to_one(entity1, entity2):
    filename = 'templates/configuration_template.txt'
    new_filename = os.path.join('Configurations', f"{to_camel_case(entity1)}Configuration.cs")

    sponsoring_config = f"\t\tbuilder.HasOne(p => p.{entity2})\n"
    sponsoring_config += f"\t\t\t.WithMany(p => p.{entity1}s)\n"
    sponsoring_config += f"\t\t\t.HasForeignKey(p => p.{entity2}Fk)\n"
    sponsoring_config += f"\t\t\t.OnDelete(DeleteBehavior.Restrict);\n\n"

    insert_config_to_file(entity1, sponsoring_config, filename, new_filename)


def generate_many_to_many(entity1, entity2):
    filename = 'templates/configuration_template.txt'
    new_filename = os.path.join('Configurations', f"{to_camel_case(entity1)}Configuration.cs")

    sponsoring_config = f"\t\tbuilder.HasMany(p => p.{entity2}s)\n"
    sponsoring_config += f"\t\t\t.WithMany(p => p.{entity1}s)\n"
    sponsoring_config += f"\t\t\t.UsingEntity(j => j.ToTable(\"{entity1}{entity2}\"));\n\n"

    insert_config_to_file(entity1, sponsoring_config, filename, new_filename)


def insert_config_to_file(entity, config, source_filename, destination_filename):
    with open(source_filename, 'r') as f:
        file_content = f.read()
    
    config_filename = os.path.join('Configurations', "ExamContext.cs")
    if os.path.isfile(destination_filename):
        pass
    else:
        with open(destination_filename, 'w') as f:
            f.write(file_content)
        insert_lines_v2("//config", f"\t\t\t\tmodelBuilder.ApplyConfiguration(new {entity}Configuration() );\n", config_filename)

    insert_lines_v2("//add config", config, destination_filename)


def generate_inheritance_tpt(mother_entity, inherited_entity):
    filename = 'templates/configuration_template.txt'
    new_filename = os.path.join('Configurations', f"{to_camel_case(mother_entity)}Configuration.cs")

    tpt_config = f"\n\t\t\tbuilder.ToTable({inherited_entity});\n\n"
    insert_config_to_file(inherited_entity, tpt_config, filename, new_filename)

def generate_inheritance_tph(mother_entity, inherited_entity):
    filename = 'templates/configuration_template.txt'
    new_filename = os.path.join('Configurations', f"{to_camel_case(mother_entity)}Configuration.cs")
    column = input("What do you want the Discriminator name to be ?")
    data_type = input("What do you want the Discriminator type to be ?")
    value = input("What do you want the value to be ?")
    tpt_config = f"\n\t\t\tbuilder.HasDiscriminator<{data_type}>(\"{column}\")"
    tpt_added_config = f"\n\t\t\t\t.HasValue<{inherited_entity}>(\"{value}\");\n\n" 
    if string_exists_in_file(new_filename, "builder.HasDiscriminator"):
        replace_tph_config(new_filename, "builder.HasDiscriminator", tpt_added_config)
    else:
        tpt_config += tpt_added_config
        insert_config_to_file(mother_entity, tpt_config, filename, new_filename)