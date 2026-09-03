import sys
import os
import json
import shutil
import zipfile
from datetime import datetime, timedelta
from pathlib import Path
from PySide6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, 
                                 QWidget, QPushButton, QLabel, QTextEdit, QFileDialog)
from PySide6.QtCore import Qt, QTimer

class OldLogOperator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("OldLogOperator")
        self.resize(800, 600)

        # State management variables
        self.is_running = False
        self.last_run_date = None
        self.config_file = "OldLogOperator.json"

        self.init_ui()
        self.load_settings()  # Run at startup
        
        # Timer for date checking (runs every minute)
        self.timer = QTimer()
        self.timer.timeout.connect(self.check_date_and_run)

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # label_TaskListSample (Using QTextEdit instead of QLabel to allow copying, set as read-only)
        layout.addWidget(QLabel("TaskList Sample:"))
        self.label_TaskListSample = QTextEdit()
        self.label_TaskListSample.setReadOnly(True)
        self.label_TaskListSample.setText(
            "Compress,30,C:\\Log\\YYYY\\YYYYMMDD\n"
            "Delete,60,C:\\Log\\YYYY\\YYYYMMDD.7z\n"
            "Delete,120,D:\\Log\\YYYY\\YYYYMM\\YYYYMMDD\\HH\\mm.mp4"
        )
        layout.addWidget(self.label_TaskListSample)

        # textBoxMultiLine_TaskList
        layout.addWidget(QLabel("Task List:"))
        self.textBoxMultiLine_TaskList = QTextEdit()
        layout.addWidget(self.textBoxMultiLine_TaskList)

        # Buttons Row
        btn_layout = QHBoxLayout()
        self.button_SaveJson = QPushButton("Save JSON")
        self.button_LoadJson = QPushButton("Load JSON")
        self.button_StartTask = QPushButton("Start")
        
        btn_layout.addWidget(self.button_SaveJson)
        btn_layout.addWidget(self.button_LoadJson)
        btn_layout.addWidget(self.button_StartTask)
        layout.addLayout(btn_layout)

        # label_LastTaskRun
        self.label_LastTaskRun = QLabel("Last Run: Never")
        layout.addWidget(self.label_LastTaskRun)

        # Signals (Qt Connections)
        self.button_SaveJson.clicked.connect(self.save_settings)
        self.button_LoadJson.clicked.connect(self.load_settings)
        self.button_StartTask.clicked.connect(self.toggle_task)

    def load_settings(self):
        """Load settings from JSON file and reflect them in the UI controls"""
        if not os.path.exists(self.config_file):
            return # Do nothing if the file does not exist

        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
                # Update corresponding controls only if values are present in JSON
                if "textBoxMultiLine_TaskList" in data:
                    self.textBoxMultiLine_TaskList.setPlainText(data["textBoxMultiLine_TaskList"])
                
                if "label_TaskListSample" in data:
                    self.label_TaskListSample.setText(data["label_TaskListSample"])
                    
        except Exception as e:
            print(f"Error loading JSON: {e}")

    def save_settings(self):
        """Save current control values as a JSON file"""
        # Set default path to "OldLogOperator.json" in the same directory as the script
        default_path = os.path.join(os.path.dirname(__file__), self.config_file)
        
        path, _ = QFileDialog.getSaveFileName(self, "Save Configuration", default_path)
        if path:
            try:
                # Retrieve current values from target controls
                data = {
                    "textBoxMultiLine_TaskList": self.textBoxMultiLine_TaskList.toPlainText(),
                    "label_TaskListSample": self.label_TaskListSample.toPlainText()
                }
                with open(path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=4, ensure_ascii=False)
            except Exception as e:
                print(f"Error saving JSON: {e}")

    def toggle_task(self):
        if not self.is_running:
            # When the Start button is pressed
            self.is_running = True
            self.button_StartTask.setText("Stop")
            self.run_tasks() # Execute immediately
            self.timer.start(60000) # Start checking every minute
        else:
            # When the Stop button is clicked (when label shows "Stop")
            self.is_running = False
            self.button_StartTask.setText("Start")
            self.timer.stop()

    def check_date_and_run(self):
        current_date = datetime.now().date()
        if self.last_run_date != current_date:
            self.run_tasks()
            self.last_run_date = current_date

    def run_tasks(self):
        lines = self.textBoxMultiLine_TaskList.toPlainText().strip().split('\n')
        for line in lines:
            if not line or ',' not in line:
                continue
            
            parts = line.split(',')
            if len(parts) < 3:
                continue

            task_name = parts[0].strip()
            try:
                days_elapsed = int(parts[1].strip())
            except ValueError:
                continue
            path_format = parts[2].strip()

            # Parse and execute the path format
            self.process_task(task_name, days_elapsed, path_format)

        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.label_LastTaskRun.setText(f"Last Run: {now_str}")

    def process_task(self, name, days, path_format):
        # Replace placeholders (expand based on current date/time)
        now = datetime.now()
        resolved_path = path_format.replace("YYYY", str(now.year)) \
                                     .replace("YYYYMMDD", now.strftime("%Y%m%d")) \
                                     .replace("YYYYMM", now.strftime("%Y%m")) \
                                     .replace("HH", now.strftime("%H")) \
                                     .replace("mm", now.strftime("%M"))

        path_obj = Path(resolved_path)

        # Check if the file/directory exists
        if path_obj.exists():
            # Determine elapsed days (based on the file's last modified time)
            mtime = datetime.fromtimestamp(path_obj.stat().st_mtime)
            if (datetime.now() - mtime).days >= days:
                try:
                    if name.lower() == "compress":
                        self.compress_file(path_obj)
                    elif name.lower() == "delete":
                        self.delete_file(path_obj)
                except Exception as e:
                    print(f"Error processing {path_format}: {e}")

    def delete_file(self, path_obj):
        if path_obj.is_file():
            os.remove(path_obj)
            print(f"Deleted: {path_obj}")
        elif path_obj.is_dir():
            shutil.rmtree(path_obj)
            print(f"Deleted Dir: {path_obj}")

    def compress_file(self, path_obj):
        if path_obj.is_file():
            zip_path = path_obj.with_suffix('.zip')
            # If a ZIP with the same name already exists, delete it before creating (overwrite support)
            if zip_path.exists():
                os.remove(zip_path)
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                zipf.write(path_obj, arcname=path_obj.name)
            os.remove(path_obj)
            print(f"Compressed: {path_obj}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = OldLogOperator()
    window.show()
    sys.exit(app.exec())
