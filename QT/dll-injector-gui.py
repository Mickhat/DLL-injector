import sys
import ctypes
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, 
                             QFileDialog, QDialog, QListWidget, QCheckBox, QTextEdit)
import psutil
from pyinjector import inject

class ProcessListDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Select a Process')
        self.setGeometry(100, 100, 400, 300)
        self.process_list_widget = QListWidget()
        self.populate_process_list()
        layout = QVBoxLayout(self)
        layout.addWidget(self.process_list_widget)
        self.process_list_widget.itemDoubleClicked.connect(self.process_selected)

    def populate_process_list(self):
        for proc in psutil.process_iter(['name', 'pid']):
            self.process_list_widget.addItem(f"{proc.info['name']} (PID: {proc.info['pid']})")

    def process_selected(self, item):
        process_info = item.text().split(" (PID: ")
        process_name = process_info[0][:-1]  # Remove the trailing ")"
        self.parent().process_name_input.setText(process_name)
        self.accept()

class DLLInjectorGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.settings_file = "dll_paths.txt"
        if not self.is_admin():
            self.request_admin()
            sys.exit()
        
        self.setWindowTitle('DLL Injector GUI')
        self.setGeometry(100, 100, 320, 300)  # Adjusted for additional UI elements
        self.initUI()
        self.load_dll_paths()

    def initUI(self):
        layout = QVBoxLayout()

        self.process_name_label = QLabel('Process Name:')
        self.process_name_input = QTextEdit()
        self.process_name_input.setText("metin2client.exe")
        self.process_name_input.setPlaceholderText("Enter process name here")
        self.process_name_input.setMaximumHeight(30)

        self.select_process_button = QPushButton('Select Process')
        self.select_process_button.clicked.connect(self.openProcessListDialog)

        self.dll_path_label = QLabel('DLL Path(s):')
        self.dll_path_input = QTextEdit()
        self.dll_path_input.setPlaceholderText("Enter DLL paths, one per line")

        self.browse_button = QPushButton('Browse...')
        self.browse_button.clicked.connect(self.openFileDialog)

        self.remember_dlls_checkbox = QCheckBox("Remember DLLs")
        
        self.inject_button = QPushButton('Inject DLL(s)')
        self.inject_button.clicked.connect(self.onInjectButtonClicked)

        self.status_label = QLabel('Status: Awaiting input...')

        layout.addWidget(self.process_name_label)
        layout.addWidget(self.process_name_input)
        layout.addWidget(self.select_process_button)
        layout.addWidget(self.dll_path_label)
        layout.addWidget(self.dll_path_input)
        layout.addWidget(self.browse_button)
        layout.addWidget(self.remember_dlls_checkbox)
        layout.addWidget(self.inject_button)
        layout.addWidget(self.status_label)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def openProcessListDialog(self):
        dialog = ProcessListDialog(self)
        dialog.exec_()

    def openFileDialog(self):
        options = QFileDialog.Options()
        dll_paths, _ = QFileDialog.getOpenFileNames(self, "Select one or more DLL files", "", "DLL Files (*.dll);;All Files (*)", options=options)
        if dll_paths:
            self.dll_path_input.setText("\n".join(dll_paths))

    def load_dll_paths(self):
        try:
            with open(self.settings_file, "r") as file:
                dll_paths = file.read().strip()
                if dll_paths:
                    self.dll_path_input.setText(dll_paths)
                    self.remember_dlls_checkbox.setChecked(True)
        except FileNotFoundError:
            pass

    def save_dll_paths(self):
        if self.remember_dlls_checkbox.isChecked():
            paths = self.dll_path_input.toPlainText().strip()
            with open(self.settings_file, "w") as file:
                file.write(paths)
        else:
            with open(self.settings_file, "w") as file:
                file.write("")  # Clear the stored paths if the checkbox is not checked

    def find_process_id(self, process_name):
        for proc in psutil.process_iter(['name', 'pid']):
            if proc.info['name'].lower() == process_name.lower():
                return proc.info['pid']
        return None

    def inject_dll(self, pid, dll_paths_str):
        dll_paths = dll_paths_str.split('\n')
        for dll_path in dll_paths:
            try:
                inject(pid, dll_path.strip())
                self.status_label.setText(f'DLL injected successfully: {dll_path.strip()}')
            except Exception as e:
                self.status_label.setText(f'Failed to inject DLL: {e}')
                break  # Stop on the first error

    def onInjectButtonClicked(self):
        process_name = self.process_name_input.toPlainText().strip()
        dll_paths_str = self.dll_path_input.toPlainText()
        pid = self.find_process_id(process_name)
        if pid:
            self.status_label.setText(f'Found {process_name} with PID: {pid}')
            self.inject_dll(pid, dll_paths_str)
            self.save_dll_paths()
        else:
            self.status_label.setText(f'Could not find process: {process_name}')

    def is_admin(self):
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False

    def request_admin(self):
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = DLLInjectorGUI()
    gui.show()
    sys.exit(app.exec_())
