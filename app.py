from flask import Flask, render_template, request, jsonify
from summarizer import generate_summary  # Import the function from summarizer.py
from utils.time_validator import validate_time_format, validate_date_format
from data.sample_chat_data import SAMPLE_CHAT_DATA

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/summarize', methods=['POST'])
def summarize():
    try:
        data = request.json
        date = data['date']
        start_time = data['start_time']
        end_time = data['end_time']
        group_id = data.get('group_id', 'Unknown Group')  # Default group ID if not provided
        
        # Validate date and time formats
        if not validate_date_format(date):
            return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD format'}), 400
        if not all(validate_time_format(t) for t in [start_time, end_time]):
            return jsonify({'error': 'Invalid time format. Use HH:MM format'}), 400
        
        # Get messages in time range (replace this with your actual filtering logic)
        messages = [msg for msg in SAMPLE_CHAT_DATA if msg['date'] == date and start_time <= msg['timestamp'] <= end_time]
        
        if not messages:
            return jsonify({'error': 'No messages found in the specified time period'}), 404
        
        # Generate summary using the new summarizer
        summary_data = generate_summary(messages, start_time, end_time, date, group_id)
        
        # Check if the response contains an error or a valid summary
        if 'error' in summary_data:
            return jsonify(summary_data), 500
        
        return jsonify(summary_data['response'])  # Ensure only the 'response' part is returned
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
