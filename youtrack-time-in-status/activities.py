import requests
import json
import os
from datetime import datetime
from dotenv import load_dotenv

# Get variables from .env file
load_dotenv()

YOUTRACK_URL = os.getenv('YOUTRACK_URL')
YOUTRACK_TOKEN = os.getenv('YOUTRACK_TOKEN')

def get_issue_activities(issue_id):
    """
    Retrieves all activities for a specified issue from YouTrack.

    Args:
        issue_id (str): The ID of the issue for which activities are to be retrieved.

    Returns:
        dict: A dictionary containing the activities data if the request is successful.
        None: If there is an error in the request.

    Raises:
        None
    """
    url = f"{YOUTRACK_URL}/api/issues/{issue_id}/activities"
    headers = {
        'Authorization': f'Bearer {YOUTRACK_TOKEN}',
        'Accept': 'application/json'
    }
    categories = ['CustomFieldCategory', 'IssueCreatedCategory']
    params = {
        'categories': ','.join(categories),
        'fields': 'id,category,field(presentation),removed(name),added(name),timestamp'
    }

    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f'Error: {response.status_code}')
        return None

def filter_and_sort_activities(activities, status_field):
    """
    Filters and sorts activities based on a specific status field.

    Args:
        activities (list): A list of activity dictionaries.
        status_field (str): The name of the status field to filter by.

    Returns:
        list: A list of filtered activity dictionaries.
    """
    filtered_activities = []

    for activity in activities:
        if activity['$type'] == 'CustomFieldActivityItem':
            if activity['field']['presentation'] == status_field:
                filtered_activities.append(activity)
                
    return filtered_activities
