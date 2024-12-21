import google.generativeai as genai
import json
from config import GEMINI_API_KEY

def setup_gemini():
    """Initialize Gemini API with specific configuration"""
    print("Setting up Gemini API...")  # Debug: Log setup
    genai.configure(api_key=GEMINI_API_KEY)

    generation_config = {
        "temperature": 0.8,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 8192,
    }

    model = genai.GenerativeModel(
        model_name='gemini-pro',
        generation_config=generation_config
    )

    return model

def clean_json_response(response_text):
    """Clean the Gemini response to remove duplicates and malformed sections."""
    try:
        response_json = json.loads(response_text)
        
        # Clean duplicates in 'action_items'
        if "action_items" in response_json:
            seen_assignees = set()
            clean_action_items = []
            for item in response_json["action_items"]:
                assignee = item.get("assignee")
                if assignee not in seen_assignees:
                    seen_assignees.add(assignee)
                    clean_action_items.append(item)
            response_json["action_items"] = clean_action_items
        
        return response_json
    
    except json.JSONDecodeError:
        print("Failed to clean JSON response.")
        return None

def generate_summary(messages, start_time, end_time, date, group_id):
    """
    Generate meeting summary using Gemini API and return JSON format
    
    Args:
        messages (list): List of filtered chat messages
        start_time (str): Start time of the meeting
        end_time (str): End time of the meeting
        date (str): Date of the meeting
        group_id (str): Identifier for the group
    
    Returns:
        dict: Generated summary as a dictionary
    """
    print("Generating summary...")  # Debug: Log start of summary generation
    model = setup_gemini()

    chat_content = "\n".join([f"{msg['sender']}: {msg['content']}" for msg in messages])

    prompt = f"""
    Please create a concise meeting minutes summary in JSON format from the following chat discussion.
    
    Input details:
    - Chat Content: {chat_content}
    - Start Time: {start_time}
    - End Time: {end_time}
    - Group ID: {group_id}
    - Date: {date}
    
    The format should be as follows:
    {{
        "headline": "Meeting Summary: [Insert topic]",
        "date": "[Insert date]",
        "time": "[Insert time]",
        "attendees": ["[List of attendees]"],
        "key_discussion_points": ["[List of key discussion points]"],
        "decisions_made": ["[List of decisions made]"],
        "action_items": [
            {{
                "assignee": "[Assignee Name]",
                "tasks": ["[Task description]"]
            }}
        ],
        "next_steps": ["[Next steps to be taken]"]
    }}
    """

    # Send prompt to Gemini API and get response
    response = model.generate_content(prompt)
    print(f"Gemini API response: {response.text}")  # Debug: Log API response
    
    # Clean the response to ensure it is valid JSON
    cleaned_response = clean_json_response(response.text)
    if not cleaned_response:
        return {"error": "Failed to generate or clean JSON summary", "raw_response": response.text}
    
    response_data = {
        "response": cleaned_response,
        "response_mime_type": "application/json"
    }
    
    return response_data

    
    # try:
    #     # Convert the response from text to JSON
    #     summary_json = json.loads(response.text)  # 'response.text' contains the actual response
    #     response_data = {
    #         "response": summary_json,
    #         "response_mime_type": "application/json"
    #     }
    #     return response_data
    # except json.JSONDecodeError:
    #     print(f"Failed to parse JSON response: {response.text}")  # Debug: Log parse failure
    #     return {"error": "Failed to generate JSON summary", "raw_response": response.text}
