from datetime import datetime
from chat_parser import parse_chat_messages
from summarizer import generate_summary

def get_time_input(prompt):
    """Get and validate time input from user"""
    while True:
        time_str = input(prompt)
        try:
            datetime.strptime(time_str, "%H:%M")
            return time_str
        except ValueError:
            print("Invalid time format. Please use HH:MM (24-hour format)")

def main():
    print("Meeting Minutes Summarizer")
    print("-------------------------")
    
    # Get time range from user
    start_time = get_time_input("Enter start time (HH:MM, 24-hour format): ")
    end_time = get_time_input("Enter end time (HH:MM, 24-hour format): ")
    
    # Sample chat data structure - replace this with your actual chat data source
    chat_data = [
        {
            "timestamp": "20:00",
            "sender": "John",
            "content": "Let's discuss the project timeline."
        },
        # Add more messages here
    ]
    
    # Filter messages for the specified time period
    filtered_messages = parse_chat_messages(chat_data, start_time, end_time)
    
    if not filtered_messages:
        print("No messages found in the specified time period.")
        return
    
    # Generate summary using Gemini
    try:
        summary = generate_summary(filtered_messages)
        
        print("\nMeeting Summary")
        print("==============")
        print(summary)
        
    except Exception as e:
        print(f"Error generating summary: {str(e)}")

if __name__ == "__main__":
    main()