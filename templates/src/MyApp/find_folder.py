import os
import re

def find_folder(start_path, folder_name):
    regex_pattern = re.compile('.*' + folder_name + '$')
    for root, dirs, files in os.walk(start_path):
        for dir in dirs:
            if re.match(regex_pattern, dir) and dir.endswith(folder_name):
                return os.path.abspath(os.path.join(root, dir))
    for dir in dirs:
        path = find_folder(os.path.join(start_path, dir), regex_pattern)
        if path is not None:
            return path