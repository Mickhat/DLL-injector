import psutil
from pyinjector import inject
import sys

def find_process_id(process_name):
    """Find the first process with the given name and return its PID."""
    for proc in psutil.process_iter(['name', 'pid']):
        if proc.info['name'] == process_name:
            return proc.info['pid']
    return None

def inject_dll(pid, dll_path):
    try:
        inject(pid, dll_path)  # pyinjector expects a PID here
        print("DLL injected successfully.")
    except Exception as e:
        print(f"Failed to inject DLL: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <process_name> <dll_path>")
        sys.exit(1)

    process_name = sys.argv[1]
    dll_path = sys.argv[2]

    pid = find_process_id(process_name)
    if pid:
        print(f"Found {process_name} with PID: {pid}")
        inject_dll(pid, dll_path)
    else:
        print(f"Could not find process: {process_name}")
