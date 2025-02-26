# YouTrack Time Tracking Script

This script allows you to automatically log time for regular activities in YouTrack via the API.

It is designed to be used once a week to account for the time spent on regular activities during the current week.

#### Limitations
- **Duplicate Check:** The script does not check if time has already been logged for a task on the specified day. If you run the script twice in a week, the time will be logged twice.

- **Missing Values:** If you do not specify some values for a task (e.g., work_type or comment), the script may throw an error or handle the data incorrectly. Ensure all required fields are filled in `tasks.json`.

- **Error Handling:** The script does not contain detailed error handling for all possible cases. In case of issues, please submit a PR.

## Installation

0. Install the repository dependencies and navigate to the script directory
    ```
    python3 -m pip install -r requirements.txt
    cd ./youtrack-timesheet
    ```

1. Fill in the `tasks.json` configuration file with your tasks. Example file content:
   ```json
   [
       {
           "id": "YOUR-123",                                # Issue number on YouTrack
           "time_spent_hours": 1,                           # Time in hours
           "work_type": "22-8",                             # Work type identifier
           "comment": "Completed feature implementation",   # Comment
           "day_of_week": "Monday"                          # Day of the week
       },
       {
           "id": "YOUR-456",
           "time_spent_hours": 0.5,
           "work_type": "22-24",
           "comment": "Performed initial testing",
           "day_of_week": "Tuesday"
       }
   ]
   ```

2. Specify your YouTrack URL and access token in the `.env` file.

## Usage

   ```bash
   python3 timesheet.py
   ```