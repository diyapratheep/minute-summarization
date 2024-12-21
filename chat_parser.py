from datetime import datetime

def parse_chat_messages(chat_data, start_time, end_time):
    """
    Filter chat messages within the specified time period
    
    Args:
        chat_data (list): List of chat messages with timestamp and content
        start_time (str): Start time in HH:MM format (24-hour)
        end_time (str): End time in HH:MM format (24-hour)
    
    Returns:
        list: Filtered chat messages
    """
    start_dt = datetime.strptime(start_time, "%H:%M")
    end_dt = datetime.strptime(end_time, "%H:%M")
    
    filtered_messages = []
    for message in chat_data:
        msg_time = datetime.strptime(message['timestamp'], "%H:%M")
        if start_dt <= msg_time <= end_dt:
            filtered_messages.append(message)
    
    return filtered_messages