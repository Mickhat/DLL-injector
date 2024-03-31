import sys
import ctypes
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLineEdit, QLabel, 
                             QFileDialog, QDialog, QListWidget)

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
        process_name = process_info[0]
        self.parent().process_name_input.setText(process_name)
        self.accept()

class DLLInjectorGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        if not self.is_admin():
            self.request_admin()
            sys.exit()
        
        self.setWindowTitle('DLL Injector GUI')
        self.setGeometry(100, 100, 320, 250)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.process_name_label = QLabel('Process Name:')
        self.process_name_input = QLineEdit()

        self.select_process_button = QPushButton('Select Process')
        self.select_process_button.clicked.connect(self.openProcessListDialog)

        self.dll_path_label = QLabel('DLL Path:')
        self.dll_path_input = QLineEdit()

        self.browse_button = QPushButton('Browse...')
        self.browse_button.clicked.connect(self.openFileDialog)

        self.inject_button = QPushButton('Inject DLL')
        self.inject_button.clicked.connect(self.onInjectButtonClicked)

        self.status_label = QLabel('Status: Awaiting input...')

        layout.addWidget(self.process_name_label)
        layout.addWidget(self.process_name_input)
        layout.addWidget(self.select_process_button)
        layout.addWidget(self.dll_path_label)
        layout.addWidget(self.dll_path_input)
        layout.addWidget(self.browse_button)
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
        dll_path, _ = QFileDialog.getOpenFileName(self, "Select DLL file", "", "DLL Files (*.dll);;All Files (*)", options=options)
        if dll_path:
            self.dll_path_input.setText(dll_path)

    def find_process_id(self, process_name):
        for proc in psutil.process_iter(['name', 'pid']):
            if proc.info['name'] == process_name:
                return proc.info['pid']
        return None

    def inject_dll(self, pid, dll_path):
        try:
            inject(pid, dll_path)
            self.status_label.setText('DLL injected successfully.')
        except Exception as e:
            self.status_label.setText(f'Failed to inject DLL: {e}')

    def onInjectButtonClicked(self):
        process_name = self.process_name_input.text()
        dll_path = self.dll_path_input.text()
        pid = self.find_process_id(process_name)
        if pid:
            self.status_label.setText(f'Found {process_name} with PID: {pid}')
            self.inject_dll(pid, dll_path)
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