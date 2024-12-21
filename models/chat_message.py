from dataclasses import dataclass
from datetime import datetime

@dataclass
class ChatMessage:
    timestamp: str
    date: str  # Added date field
    sender: str
    content: str
    
    def get_datetime(self):
        """Convert timestamp and date string to datetime object"""
        datetime_str = f"{self.date} {self.timestamp}"
        return datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")