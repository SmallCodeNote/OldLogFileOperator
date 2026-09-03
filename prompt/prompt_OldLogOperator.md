**Prompt:**

Please develop a Python application named `OldLogOperator.py` based on the following specifications:

### **Environment & Libraries**
- **OS**: Windows 11
- **Python Version**: 3.12.10
- **GUI Framework**: PySide6

### **Core Functionality**
The program manages and processes log files based on their age. It identifies files in various directory structures, checks if they exceed a specified number of days, and performs actions like compression or deletion.

#### **Configuration & Persistence (JSON)**
- **Save Logic**: When `button_SaveJson` is clicked, open a "Save File" dialog. Save the current values of all relevant controls into a JSON file at the user-specified path. The default save path should be `OldLogOperator.json` in the same directory as the script.
- **Load Logic**: On startup, attempt to load configuration from `OldLogOperator.json` in the script's folder. 
    - If the file is missing: Do nothing (use default values).
    - If the file exists: Initialize control values from the JSON data. Skip any controls that do not have corresponding keys in the JSON.

#### **UI Components & Behavior**
- `textBoxMultiLine_TaskList`: A multi-line text box where users input tasks.
- `label_TaskListSample`: Display copyable examples of "Compress" and "Delete" formats (see TaskList Format below).
- `button_StartTask`: 
    - Clicking it starts the task execution and changes its label to **"Stop"**.
    - While in the **"Stop"** state, the program should automatically execute the tasks whenever the system date changes.
    - If clicked while the label is **"Stop"**, change the label back to **"Start"**.
- `label_LastTaskRun`: Display the timestamp of the last successful task execution.

#### **Data Format (TaskList)**
The input in `textBoxMultiLine_TaskList` must follow this CSV-like format:
`TaskName,DaysElapsed,TargetLogFilePathFormat`

*Examples:*
- `Compress,30,C:\Log\YYYY\YYYYMMDD`
- `Delete,60,C:\Log\YYYY\YYYYMMDD.7z`
- `Delete,120,D:\Log\YYYY\YYYYMM\YYYYMMDD\HH\mm.mp4`

*(Note: YYYY, YYYYMM, etc., in the path format should be treated as placeholders for date/time components.)*
