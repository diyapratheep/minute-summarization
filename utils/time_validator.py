from datetime import datetime

def validate_time_format(time_str):
    """Validate if the time string is in correct HH:MM format"""
    try:
        datetime.strptime(time_str, "%H:%M")
        return True
    except ValueError:
        return False

def validate_date_format(date_str):
    """Validate if the date string is in correct YYYY-MM-DD format"""
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False