import google.generativeai as genai
from typing import List
from models.chat_message import ChatMessage
from config import GEMINI_API_KEY

class SummaryService:
    def __init__(self):
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-pro')
    
    def generate_summary(self, messages: List[ChatMessage]) -> str:
        """
        Generate meeting summary using Gemini API
        
        Args:
            messages (List[ChatMessage]): List of filtered chat messages
            
        Returns:
            str: Generated summary
        """
        chat_content = "\n".join([
            f"{msg.sender}: {msg.content}" 
            for msg in messages
        ])
        
        prompt = f"""
        Please create a concise meeting minutes summary from the following chat discussion:
        
        {chat_content}
        
        Please include:
        1. Key discussion points
        2. Decisions made
        3. Action items
        4. Next steps
        
        Format the summary in a clear, professional manner.
        """
        
        response = self.model.generate_content(prompt)
        return response.text