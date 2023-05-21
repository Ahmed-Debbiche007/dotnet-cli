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
        


def create_folder(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"Folder created: {folder_path}")
    else:
        print(f"Folder already exists: {folder_path}")
