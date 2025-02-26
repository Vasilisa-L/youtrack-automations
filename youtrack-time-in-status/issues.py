import requests
import json
import os
from datetime import datetime
from dotenv import load_dotenv

# Get variables from .env file
load_dotenv()

YOUTRACK_URL = os.getenv('YOUTRACK_URL')
YOUTRACK_TOKEN = os.getenv('YOUTRACK_TOKEN')

def get_all_issues(project_id, yt_filter):
    """
    Retrieves all issues from a specified project based on a given filter.

    Args:
        project_id (str): The ID of the project.
        yt_filter (str): The filter to apply to the issues query.

    Returns:
        dict: A JSON object containing the issues if the request is successful.
        None: If there is an error in the request.

    Raises:
        None
    """
    if not "project:" in yt_filter.lower():
        yt_filter =  f"project: {project_id} " + yt_filter

    headers = {
        'Authorization': f'Bearer {YOUTRACK_TOKEN}',
        'Accept': 'application/json'
    }
    params = {
        'fields': 'idReadable,summary,created,updated,resolved,fields(projectCustomField(field(name)),value(name,minutes))',
        'query': f'{yt_filter}'
    }
    url = f'{YOUTRACK_URL}/api/issues'
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f'Error: {response.status_code}')
        return None

def create_dataframe(issue_list):
    """
    Creates a list of dictionaries from a list of issues, suitable for converting into a DataFrame.

    Args:
        issue_list (list): A list of issue dictionaries containing detailed information about each issue.

    Returns:
        list: A list of dictionaries, each representing a row of data for a DataFrame.
    """
    data = []
    
    for issue in issue_list:
        # Create a dictionary with data for the DataFrame
        row = {
            'issue_id': issue['idReadable'],
            'summary': issue['summary'],
            'created': issue['created'],
            'updated': issue['updated'],
            'resolved': issue['resolved'],
        }

        for field in issue['fields']:
            if type(field['value']) == dict:
                if "name" in field['value'].keys():
                    row[field['projectCustomField']['field']['name']] = field['value']['name']
                elif "minutes" in field['value'].keys():
                    row[field['projectCustomField']['field']['name']] = field['value']['minutes'] * 1000 * 60
            elif type(field['value']) == list and len(field['value']) != 0:
                # Temporary solution, take only one value from list
                row[field['projectCustomField']['field']['name']] = field['value'][0]['name']

        activity_list = issue['activities']
        
        # If there were no status changes yet
        if not activity_list:
            # The time setting the current status is the same as the creation time
            row[f"{row['State']}"] = row['created']
            
        else:
            # row_temp is used for cases if the status was returned multiple times
            # It stores the timestamp when the status was last set
            row_temp = {}

            for activity in activity_list:
                added_status = activity['added'][0]['name']
                removed_status = activity['removed'][0]['name']
        
                # If the removed status is not yet in the attributes of this issue, consider it was created with this status
                if removed_status not in row:
                    row[removed_status] = row['created']
                    row_temp[removed_status] = row['created']

                if added_status not in row:
                    row[added_status] = activity['timestamp']
                row_temp[added_status] = activity['timestamp']
                
                if f"{removed_status} duration" not in row:
                    row[f"{removed_status} duration"] = activity['timestamp'] - row_temp[removed_status]
                else:
                    row[f"{removed_status} duration"] += activity['timestamp'] - row_temp[removed_status]
        
        # If the issue is not closed, the time in the current status is calculated from the current time
        if row['resolved'] is None:
            current_time = datetime.now().timestamp() * 1000
            row[f"{row['State']} duration"] = current_time - row[f"{row['State']}"] # current time - time of status change
        
        data.append(row)

    return data
