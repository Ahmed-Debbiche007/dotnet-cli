import os
def insert_lines_v2(keyword, lines_to_add, file_path):
    # Read in the file as a list of lines
    with open(file_path, "r") as f:
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
    with open(file_path, "w") as f:
        f.writelines(lines)


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
