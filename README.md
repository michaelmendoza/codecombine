# CodeCombine

CodeCombine is a powerful utility for combining code files from a directory structure into consolidated text files, organized by folder. It's designed to help developers and teams easily create snapshots or summaries of their codebase, making it easier to review, share, or archive project structures. Mostly, I was inspired to make this project to make it easier to share my codebase with ChatGPT o1-mini which currently didn't include support for including files, but you can copy and past code which i generated using this tool.

## Features

- Combine multiple code files into single text files, preserving folder structure
- Specify which file types to include
- Ignore specific folders (e.g., `node_modules`, `.git`)
- Customizable output location
- Easy-to-use command-line interface

## Installation

You can install CodeCombine using pip:

```
pip install codecombine
```

## Usage

Basic usage:

```
codecombine -r /path/to/project -o /path/to/output
```

This will combine all default file types (`.jsx`, `.js`, `.scss`, `.html`) from the specified project directory into text files in the output directory.

### Options

- `-r`, `--root`: Root folder to start combining files (default: current directory)
- `-o`, `--output`: Output folder for combined files (default: 'output')
- `-t`, `--types`: File types to include (default: .jsx .js .scss .html)
- `-i`, `--ignore`: Folder names to ignore (default: node_modules .git)

### Examples

Include only Python and JavaScript files:
```
codecombine -r /path/to/project -o /path/to/output -t .py .js
```

Ignore 'vendor' and 'temp' folders:
```
codecombine -r /path/to/project -o /path/to/output -i vendor temp
```

Combine Python and JavaScript files, ignoring 'node_modules':
```
codecombine -r /path/to/project -o /path/to/output -t .py .js -i node_modules
```

## Output

CodeCombine creates a text file for each folder in your project (including the root). Each file contains the contents of all matching files in that folder, separated by headers indicating the original file path.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

If you encounter any problems or have any questions, please open an issue on the [GitHub repository](https://github.com/michaelmendoza/codecombine).