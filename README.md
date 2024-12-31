# CURSOR AI Utility Script

This Python script is a utility for modifying telemetry-related JSON values in the `storage.json` file associated with Cursor AI. It generates random UUID-like strings for telemetry keys and saves the updated data back to the file.

---

## Features

- **Generates Random UUIDs**: Uses Python's `uuid` library to create random identifiers.
- **JSON Data Manipulation**: Reads, modifies, and writes JSON data.
- **ASCII Art Display**: Creates ASCII art for "CURSOR AI" using the `pyfiglet` library.

---

## Requirements

- Python 3.6 or higher
- `pyfiglet` library (install with `pip install pyfiglet`)

---

## Usage

1. Clone this repository.
2. Update the `json_file_path` variable in the script to point to your `storage.json` file.
3. Run the script:
   ```bash
   python cursor_ai_utility.py
