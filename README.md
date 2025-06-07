# Cursor AI Telemetry Bypass Script 

## 🚀 Introduction

Welcome to the **Cursor AI Telemetry Bypass Script**—a powerful Python toolkit designed to bypass cursor AI usage limits.

---

## ⚠️ Disclaimer

This project is intended **for educational and research purposes only**. Users must comply with all applicable **terms of service** and **laws**. The author holds **no liability** for misuse or damages resulting from this tool.

---

## 🔍 Overview

This toolkit automates multiple tasks, including:

✅ **Bypassing telemetry & version checks** by manipulating key files (`storage.json`, product version, machine ID, etc.). 
 
✅ **Automated account registration** using temporary email services  (**Temp-Mail-Plus**). 

✅ **Resetting machine identifiers** and clearing telemetry data.
  
✅ **Cross-platform support** for **Windows**, **macOS**, and **Linux**.  

---

## ✨ Features

- **📡 Telemetry Bypass** – Randomizes telemetry IDs in `storage.json` for Cursor and Windsurf AI.  
- **🔄 Version Bypass** – Modifies version details to bypass compatibility checks.  (**Coming on the next release**) 
- **🤖 Automated Account Registration** – Registers new Cursor accounts using headless browser automation. (**Coming on the next release**) 
- **🖥️ Cross-Platform Compatibility** - detects OS and adjusts file paths. 
- **📁 Safe Backups** – Ensures backups of key files before modification.  
- **⚙️ Configurable Settings** – Uses YAML/JSON configuration for paths, credentials, and options.  
  

---

## 📦 Requirements

✅ Python **3.6** or higher  

### 🔗 Main Dependencies  

- `selenium`  
- `pyyaml`  
- `requests`   

## 📦 Installation

To install all required dependencies, run the following:

```bash 
pip install -r requirements.txt
```

---

## Usage

1. Clone the repository:

```bash
  git clone https://github.com/FilippoDeSilva/cursor-ai-bypass.git
    cd cursor-ai-bypass
```

2. Edit the configuration file:  
   Open `config.yaml` or `config.json` and set the variables based on your pc setup for more read `config.yaml`

3. Log out of your current Cursor account and close it. 

4. Go to your favorite temp mail provider (temp-mail.com) 

5. Run the script:

    ```bash
    python main.py --all #To run all the scripts
    python main.py --help 
#To see available flags
 
    ```
6. Login to cursor with the temp mail 

7. All done!

## Known Issues:

- **Automated registration is not working:** but to be fixed on the next release I'd be glad on collaboration. 
- **Version bypass isn't working:** it's a failsafe method I could come up with it's not that important unless the user doesn't want cursor to auto update the IDE. So for now I'll give it a low priority. 

## License

### MIT License
```bash
Copyright (c) [2025] [Filippo De Silva]

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

Developing this tool wouldn’t have been possible without the incredible contributions of open-source projects and supportive individuals and services. I sincerely appreciate:

- `selenium` – Web automation framework  
- `pyyaml` – YAML parsing and processing library  
- `requests` – HTTP requests handling library  
- `Temp Mail` – Temporary email service

---

**Remember**: Always act responsibly when using this tool.