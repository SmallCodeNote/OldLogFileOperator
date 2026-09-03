# OldLogOperator

OldLogOperator is a lightweight Python desktop application designed to automate the management of old log files. It allows users to define rules for automatically **compressing** or **deleting** files and directories based on their age and specific path patterns.

## 🌟 Features
- **Automated Task Execution**: Automatically checks and runs tasks every minute (if the date has changed).
- **Dynamic Path Resolution**: Supports placeholders in file paths that are replaced with real dates/times at runtime:
    - `YYYY`: Year (e.g., 2026)
    - `YYYYMMDD`: Date (e.g., 20260904)
    - `YYYYMM`: Month (e.g., 202609)
    - `HH`: Hour (e.g., 14)
    - `mm`: Minute (e.g., 30)
- **Action Support**: Supports two primary actions:
    - `Compress`: Converts a file into a `.zip` archive and deletes the original.
    - `Delete`: Permanently removes files or directories.
- **JSON Configuration**: Save and load your task lists easily using JSON files.
- **User-Friendly GUI**: Built with PySide6 for an intuitive experience.

## 🛠 Prerequisites
Before running this application, ensure you have Python installed on your system. You will also need to install the `PySide6` library:

```bash
pip install PySide6
```

## 🚀 How to Use

1. **Launch the Application**: Run the script using Python.
2. **Configure Tasks**: In the "Task List" area, enter your rules in the following format:
   `Action,DaysElapsed,PathFormat`
   - **Action**: `Compress` or `Delete` (Case-insensitive).
   - **DaysElapsed**: The number of days since the last modification. If a file is older than this value, the action will trigger.
   - **PathFormat**: The path to your logs using the placeholders mentioned in the Features section.

### Example Task List:
```text
Compress,30,C:\Log\YYYY\YYYYMMDD
Delete,60,C:\Log\YYYY\YYYYMMDD.7z
Delete,120,D:\Log\YYYY\YYYYMM\YYYYMMDD\HH\mm.mp4
```

3. **Save Configuration**: Click "Save JSON" to export your current task list to a file. You can reload this file later using the "Load JSON" button.
4. **Start/Stop**: 
   - Click **Start** to begin the monitoring service. The app will immediately run the tasks and then check every minute for new daily tasks.
   - Click **Stop** to pause the automatic checks.

## ⚙️ Technical Details
- **Language**: Python 3.x
- **GUI Framework**: PySide6 (Qt for Python)
- **File Handling**: Uses `pathlib` for robust path manipulation and `shutil`/`zipfile` for file operations.
- **Scheduling**: Utilizes `QTimer` to perform non-blocking periodic checks.

## ⚠️ Important Notes
- **Permissions**: Ensure the application has sufficient permissions to read, write, and delete files in the target directories.
- **Overwrite Warning**: When using the `Compress` action, if a `.zip` file with the same name already exists, it will be deleted before creating the new one.
- **Irreversible Actions**: The `Delete` action is permanent. Please double-check your path formats before starting the service to avoid accidental data loss.
