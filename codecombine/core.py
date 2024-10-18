"""
Core functions for the CodeCombine utility.
Includes functions for combining files by folder and sanitizing filenames.
"""

import os

def sanitize_filename(filename):
    """
    Sanitize a filename by replacing non-alphanumeric characters with underscores.
    
    Args:
    filename (str): The filename to sanitize.
    
    Returns:
    str: The sanitized filename.
    """
    return ''.join(c if c.isalnum() or c in ('-', '_') else '_' for c in filename)

def should_ignore_folder(folder_name, ignore_list):
    """
    Check if a folder should be ignored based on the ignore list.
    
    Args:
    folder_name (str): The name of the folder to check.
    ignore_list (list): List of folder names to ignore.
    
    Returns:
    bool: True if the folder should be ignored, False otherwise.
    """
    return any(ignore_name in folder_name for ignore_name in ignore_list)

def combine_files_by_folder(root_folder, output_folder, file_types, ignore_folders):
    """
    Combine code files from the root folder into consolidated text files, organized by folder.
    
    Args:
    root_folder (str): The root folder to start combining files from.
    output_folder (str): The folder to save the combined files.
    file_types (list): List of file extensions to include.
    ignore_folders (list): List of folder names to ignore.
    """
    if not os.path.exists(root_folder):
        print(f"Error: The folder '{root_folder}' does not exist.")
        return

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for current_folder, dirnames, filenames in os.walk(root_folder):
        # Skip ignored folders
        dirnames[:] = [d for d in dirnames if not should_ignore_folder(d, ignore_folders)]
        
        if should_ignore_folder(os.path.basename(current_folder), ignore_folders):
            continue

        matching_files = [f for f in filenames if any(f.endswith(ext) for ext in file_types)]
        
        if not matching_files:
            continue  # Skip this folder if no matching files are found

        relative_path = os.path.relpath(current_folder, root_folder)
        if relative_path == '.':
            output_filename = os.path.basename(root_folder)
        else:
            output_filename = os.path.basename(root_folder) + '_' + sanitize_filename(relative_path.replace(os.path.sep, '_'))
        
        output_file_path = os.path.join(output_folder, f"{output_filename}.txt")
        
        with open(output_file_path, 'w', encoding='utf-8') as outfile:
            for filename in matching_files:
                file_path = os.path.join(current_folder, filename)
                file_relative_path = os.path.relpath(file_path, root_folder)

                separator = f"# ===== {file_relative_path} ====="
                outfile.write(f'{separator}\n\n')

                try:
                    with open(file_path, 'r', encoding='utf-8') as infile:
                        outfile.write(infile.read())
                except UnicodeDecodeError:
                    print(f"Warning: Unable to read '{file_path}'. It may not be a text file or may use a different encoding.")
                    outfile.write(f"# Warning: Content of '{file_relative_path}' could not be included due to encoding issues.\n")

                outfile.write('\n\n')

        print(f"Combined {len(matching_files)} file(s) for '{relative_path}' into '{output_file_path}'.")
