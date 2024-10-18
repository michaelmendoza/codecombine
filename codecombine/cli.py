"""
CodeCombine CLI: A Code File Combining Utility

This script combines code files from a directory structure into consolidated text files,
organized by folder. It allows for specifying file types to include and folders to ignore.

Usage examples:
codecombine -r /path/to/project -o /path/to/output
codecombine -r /path/to/project -o /path/to/output -t .py .js .html
codecombine -r /path/to/project -o /path/to/output -i vendor temp
codecombine -r /path/to/project -o /path/to/output -t .py .js -i node_modules
"""

import os
import argparse
from .core import combine_files_by_folder

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