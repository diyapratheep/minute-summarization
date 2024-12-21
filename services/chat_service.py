from datetime import datetime
from typing import List
from models.chat_message import ChatMessage

class ChatService:
    def __init__(self, chat_data):
        # Add default date if not provided in chat data
        for msg in chat_data:
            if 'date' not in msg:
                msg['date'] = '2024-02-20'  # Default date for testing
        self.chat_data = [ChatMessage(**msg) for msg in chat_data]
    
    def get_messages_in_timerange(self, date: str, start_time: str, end_time: str) -> List[ChatMessage]:
        """
        Filter chat messages within the specified date and time period
        
        Args:
            date (str): Date in YYYY-MM-DD format
            start_time (str): Start time in HH:MM format
            end_time (str): End time in HH:MM format
            
        Returns:
            List[ChatMessage]: Filtered messages
        """
        start_dt = datetime.strptime(f"{date} {start_time}", "%Y-%m-%d %H:%M")
        end_dt = datetime.strptime(f"{date} {end_time}", "%Y-%m-%d %H:%M")
        
        return [
            msg for msg in self.chat_data
            if msg.date == date and start_dt <= msg.get_datetime() <= end_dt
        ]