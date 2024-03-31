# DLL Injector Project

This project provides a Python-based tool for injecting DLLs (Dynamic Link Libraries) into running processes. It's designed for educational purposes, debugging, and testing DLLs in a controlled environment. To successfully inject a DLL into a process, the script must be run with administrative privileges. This is necessary to allow the script to modify other processes, which is typically restricted to prevent unauthorized system changes.

## Features

- Inject a DLL into a specified process by name.
- Automatically resolve the process name to its PID.
- Simple command-line interface for easy operation.
- Error handling for common issues encountered during injection.
- You can also now download a GUI version on the Release Page [Virustotal](https://www.virustotal.com/gui/file/f36e940df6c319aaf735bb11362b1454e5dbc91a4e624213cf8c39a668adbbfc/detection)


## Requirements

- Python 3.6 or newer.
- `psutil` and `pyinjector` Python packages.

## Installation

1. Ensure Python 3.6+ is installed on your system.
2. Clone this repository or download the source code.
3. Install required Python packages:

```bash
pip install psutil pyinjector
```

## Usage

Run the tool from the command line, specifying the target process name and the path to the DLL you wish to inject:

```bash
python dll-injector.py <process_name> <path_to_dll>
```

For example, to inject `example.dll` into `targetapp.exe`, use:

```bash
python dll-injector.py targetapp.exe C:\path\to\example.dll
```

## Contributing

Contributions to the project are welcome. Please adhere to conventional coding standards and provide documentation for any new features or changes.

## License

This project is open-source and free to use. It is released under the MIT License.

## Disclaimer

This tool is provided as-is without any warranty. The authors or contributors are not responsible for any misuse or damage caused by this tool. It is intended for educational and testing purposes only. Use it responsibly and ethically, ensuring you have appropriate permissions to interact with the target processes.