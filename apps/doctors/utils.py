from datetime import datetime
from django.utils.dateparse import parse_date
from django.utils.timezone import make_aware
from django.conf import settings

def format_availability(days, time_range):
    """
    Utility function to format the availability of a doctor.

    Args:
        days (list): List of days the doctor is available.
        time_range (tuple): Tuple containing start and end time for availability.

    Returns:
        str: Formatted availability string.
    """
    if not days or not time_range:
        return "No availability set."

    days_str = ', '.join(days)
    start_time, end_time = time_range
    time_str = f"{start_time} - {end_time}"
    return f"Available on: {days_str} from {time_str}"

def parse_datetime(datetime_str, format='%Y-%m-%d %H:%M:%S'):
    """
    Utility function to parse a datetime string into a timezone-aware datetime object.

    Args:
        datetime_str (str): The datetime string to parse.
        format (str): The format of the datetime string. Default is '%Y-%m-%d %H:%M:%S'.

    Returns:
        datetime: Parsed timezone-aware datetime object.
    """
    try:
        naive_datetime = datetime.strptime(datetime_str, format)
        return make_aware(naive_datetime)
    except ValueError as e:
        raise ValueError(f"Error parsing datetime: {e}")

def format_datetime(dt, format='%Y-%m-%d %H:%M:%S'):
    """
    Utility function to format a datetime object into a string.

    Args:
        dt (datetime): The datetime object to format.
        format (str): The format for the datetime string. Default is '%Y-%m-%d %H:%M:%S'.

    Returns:
        str: Formatted datetime string.
    """
    if not dt:
        return ""
    return dt.strftime(format)

def parse_date_input(date_str):
    """
    Utility function to parse a date string into a date object.

    Args:
        date_str (str): The date string to parse.

    Returns:
        date: Parsed date object or None if parsing fails.
    """
    try:
        return parse_date(date_str)
    except ValueError as e:
        raise ValueError(f"Error parsing date: {e}")

def validate_time_range(start_time, end_time):
    """
    Utility function to validate if a given time range is correct.

    Args:
        start_time (str): The start time of the range.
        end_time (str): The end time of the range.

    Returns:
        bool: True if the time range is valid, False otherwise.
    """
    try:
        start = datetime.strptime(start_time, '%H:%M').time()
        end = datetime.strptime(end_time, '%H:%M').time()
        return start < end
    except ValueError as e:
        raise ValueError(f"Error validating time range: {e}")
