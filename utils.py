import os
def insert_lines_v2(keyword, lines_to_add, file_path):
    # Read in the file as a list of lines
    with open(file_path, "r") as f:
        lines = f.readlines()
    last_slash_index = file_path.rindex("/")
    entity = "".join(file_path[last_slash_index + 1:])
    entity = entity.replace("Configuration.cs","")
    # Find the index of the line containing the keyword
    keyword_index = None
    for i, line in enumerate(lines):
        if keyword in line:
            keyword_index = i
            break

    # If the keyword is found, insert the lines before it
    if keyword_index is not None:
        lines = lines[:keyword_index] + [lines_to_add] + lines[keyword_index:]

    # Write the modified lines back to the file
    with open(file_path, "w") as f:
        for line in lines:
            try:
                line = line.replace("{entity}", entity)
                f.writelines(line)
            except:
                pass


def insert_lines(entity,keyword, code, file_path):
    # Read in the file as a list of lines
    with open(file_path, "r") as f:
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
    with open(file_path, "w") as f:
        f.writelines(lines)

def replace_tph_config(file_path, search_string, replacement_string):
    try:
        with open(file_path, 'r+') as file:
            file_content = file.read()
            search_index = file_content.find(search_string)
            if search_index != -1:
                semicolon_index = file_content.find(';', search_index)
                if semicolon_index != -1:
                    updated_content = file_content[:semicolon_index] + replacement_string + file_content[semicolon_index+1:]
                    file.seek(0)
                    file.write(updated_content)
                    file.truncate()
                    return True
                else:
                    return False
            else:
                return False
    except FileNotFoundError:
        print("File not found.")
        return None
    
def string_exists_in_file(file_path, search_string):
    try:
        with open(file_path, 'r') as file:
            file_content = file.read()
            if search_string in file_content:
                return True
            else:
                return False
    except FileNotFoundError:
        print("File not found.")
        return False


