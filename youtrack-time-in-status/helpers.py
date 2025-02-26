from datetime import timedelta
import pandas as pd

def create_column_mapping(columns):
    """
    Creates a dictionary mapping columns with "duration" to their shortened form without " duration".

    Args:
    columns (list): A list of columns to search for and shorten those containing "duration".

    Returns:
    dict: A dictionary where keys are the original columns with "duration" and values are these columns without " duration".
    """
    column_mapping = {col: col.replace(' duration', '') for col in columns if 'duration' in col}
    return column_mapping

def format_time(miliseconds):
    """
    Converts time in miliseconds to a human-readable format.
   
    :param seconds: float, time in seconds
    :return: str, time in the format "X days, HH:MM:SS"
    """
    if pd.isna(miliseconds):
        return "-"

    seconds = miliseconds / 1000
    td = timedelta(seconds=seconds)
    days = td.days
    hours, remainder = divmod(td.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    
    if days > 0:
        return f"{days} days, {hours:02d}:{minutes:02d}:{seconds:02d}"
    else:
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

