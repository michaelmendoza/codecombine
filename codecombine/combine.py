"""
CodeCombine: A Code File Combining Utility

This script combines code files from a directory structure into consolidated text files,
organized by folder. It allows for specifying file types to include and folders to ignore.

Usage examples:
codecombine -r /path/to/project -o /path/to/output
codecombine -r /path/to/project -o /path/to/output -t .py .js .html
codecombine -r /path/to/project -o /path/to/output -i vendor temp
codecombine -r /path/to/project -o /path/to/output -t .py .js -i node_modules
"""

import os
import sys
import argparse

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

def main():
    """
    Main function to parse command-line arguments and run the code file combining process.
    """
    parser = argparse.ArgumentParser(
        description="CodeCombine: Combine code files by folder with specified file types.",
        epilog="""
Examples:
  %(prog)s -r /path/to/project -o /path/to/output
  %(prog)s -r /path/to/project -o /path/to/output -t .py .js .html
  %(prog)s -r /path/to/project -o /path/to/output -i vendor temp
  %(prog)s -r /path/to/project -o /path/to/output -t .py .js -i node_modules
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("-r", "--root", default=".", help="Root folder to start combining files (default: current directory)")
    parser.add_argument("-o", "--output", default="output", help="Output folder for combined files (default: 'output')")
    parser.add_argument("-t", "--types", nargs="+", default=[".jsx", ".js", ".scss", ".html"],
                        help="File types to include (default: .jsx .js .scss .html)")
    parser.add_argument("-i", "--ignore", nargs="*", default=None,
                        help="Folder names to ignore (default: node_modules .git)")

    args = parser.parse_args()

    root_folder = os.path.abspath(args.root)
    output_folder = os.path.abspath(args.output)
    file_types = args.types if args.types else [".jsx", ".js", ".scss", ".css", ".html"]
    
    # Set default ignore folders if not specified
    default_ignore = ["node_modules", ".git"]
    ignore_folders = args.ignore if args.ignore is not None else default_ignore

    print(f"CodeCombine: A Code File Combining Utility")
    print(f"Root folder: {root_folder}")
    print(f"Output folder: {output_folder}")
    print(f"File types: {', '.join(file_types)}")
    print(f"Ignored folders: {', '.join(ignore_folders)}")

    combine_files_by_folder(root_folder, output_folder, file_types, ignore_folders)

if __name__ == "__main__":
    main()