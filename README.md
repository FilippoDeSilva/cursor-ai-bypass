# CURSOR and Windsurf AI Telemetry Bypass & Automation Toolkit

## Disclaimer

This project is provided for educational and research purposes only. You are responsible for compliance with all applicable terms of service and laws. The author is not liable for misuse or damages.

---

## Overview

This Python toolkit automates several tasks for Cursor and Windsurf AI, including:

- Bypassing telemetry and version checks by manipulating key files (`storage.json`, product version, machine ID, etc.).
- Registering new Cursor accounts using temporary/disposable email services (Temp-Mail-Plus).
- Resetting machine identifiers and cleaning up telemetry data.
- Supports Windows, macOS, and Linux.

---

## Features

- **Telemetry Bypass**: Randomizes telemetry IDs in `storage.json` for Cursor and Windsurf AI.
- **Version Bypass**: Modifies version information to bypass version checks.
- **Automated Registration**: Registers new Cursor accounts using headless browser automation and disposable email.
- **Cross-Platform**: Detects OS and adapts file paths as needed.
- **Safe Backups**: Backs up key files before modification.
- **Configurable**: Uses a YAML/JSON config file for paths, credentials, and options.
- **Colorful CLI**: Uses `pyfiglet` for ASCII art and `colorama` for colored output.

---

## Requirements

- Python 3.6 or higher

### Main dependencies

- `selenium`
- `pyyaml`
- `requests`
- `pyfiglet`
- `colorama`

Install all dependencies with:
```bash
pip install -r requirements.txt
pip install pyfiglet colorama```
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
- [colorama](https://github.com/tartley/colorama) for the terminal coloring library.
- Special thanks to anyone who contributed ideas or feedback to make this tool better.

---

**Remember**: Always act responsibly when using this tool.