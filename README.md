# CURSOR and Windsurf AI Telemetry Bypass Script
### Disclaimer
This script is provided for educational and experimental purposes only. Use it responsibly and ensure compliance with any relevant terms of service or policies. The author is not liable for any misuse or damages arising from the use of this script.

### Description

This Python script is a utility for modifying telemetry-related JSON values in the `storage.json` file associated with Cursor and Windsurf AI. It generates random UUID-like strings for telemetry keys and saves the updated data back to the file.

---

## Features

- **Generates Random UUIDs**: Uses Python's `uuid` library to create random identifiers.
- **JSON Data Manipulation**: Reads, modifies, and writes JSON data.
---

## Requirements

- Python 3.6 or higher
- `pyfiglet` library (install with `pip install pyfiglet`)

---

## Usage

1. Clone this repository:
   ```bash
   git clone https://github.com/FilippoDeSilva/cursor-windsurf-ai-bypass.git
2. Update the `json_file_path` variable in the script to point to your `storage.json` file. (Only if you aren't using Windows OS otherwise don't touch anything)
3. Run the script:
   ```bash
   python main.py



## License

This project is licensed under the **MIT License**.

**MIT License**:

```
MIT License

Copyright (c) [2024] [Filippo De Silva]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
```

## Contributing

If you'd like to contribute to this project, please fork the repository and submit a pull request. Contributions are always welcome.

## Acknowledgments

- [pyfiglet](https://github.com/pwaller/pyfiglet) for the ASCII art library.
- Special thanks to anyone who contributed ideas or feedback to make this tool better.

---

**Remember**: Always act responsibly when using this tool. Test only on networks you own or have explicit permission to test. Unauthorized access to networks is illegal.
