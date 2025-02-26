from datetime import date, timedelta
import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Specify your YouTrack URL and access token from environment variables
base_url = os.getenv('YOUTRACK_URL')
token = os.getenv('YOUTRACK_TOKEN')

# Path to the configuration file
config_file_path = 'tasks.json'

# Check if the configuration file exists
if not os.path.exists(config_file_path):
    print(f"Configuration file {config_file_path} not found")
    exit(1)

# Read configuration from the file
with open(config_file_path, 'r') as config_file:
    tasks = json.load(config_file)

# Create a date object for today's date
today = date.today()

# Determine the current week
start_of_week = today - timedelta(days=today.weekday())

# Request headers
headers = {
    'Authorization': f'Bearer {token}',
    'Content-Type': 'application/json'
}

# Send requests for each task
for task in tasks:
    issue_id = task['id']
    time_spent_hours = task['time_spent_hours']
    time_spent_minutes = int(time_spent_hours * 60)  # Convert hours to minutes
    work_type_id = task['work_type']
    comment = task['comment']
    day_of_week = task['day_of_week']

    # Determine the date for the specified day of the week in the current week
    days_until_day_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'].index(day_of_week)
    task_date = start_of_week + timedelta(days=days_until_day_of_week)

    # Data for the request
    data = {
        "issueId": issue_id,
        "duration": {
                "minutes": time_spent_minutes
            },
        "date": int(task_date.strftime("%s")) * 1000,  # Date in milliseconds
        "text": comment,
        "type": {
                "id": work_type_id
            }
    }

    # URL for adding time
    url = f'{base_url}/issues/{issue_id}/timeTracking/workItems'

    # Send the request
    response = requests.post(url, headers=headers, data=json.dumps(data))

    # Check the response
    if response.status_code == 200:
        print(f"Time successfully logged for task {issue_id} on date {task_date} with comment '{comment}'")
    else:
        print(f"Error for task {issue_id}: {response.status_code}")
        print(response.text)