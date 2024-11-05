from datetime import datetime, timedelta
import re

def get_update_time(ago_time_string):
    # Get the current time
    current_time = datetime.now()
    updated_time = None
    # Extract the time value and unit using regex
    match = re.search(r'Cập nhật(\d+)\s*(\w+)\s*trước', ago_time_string)
    if match:
        value = int(match.group(1))
        unit = match.group(2)
        
        # Calculate the updated time based on the unit
        if unit == 'giây':
            updated_time = current_time - timedelta(seconds=value)
        elif unit == 'phút':
            updated_time = current_time - timedelta(minutes=value)
        elif unit == 'giờ':
            updated_time = current_time - timedelta(hours=value)
        elif unit == 'ngày':
            updated_time = current_time - timedelta(days=value)
        elif unit == 'tuần':
            updated_time = current_time - timedelta(weeks=value)
        elif unit == 'tháng':
            updated_time = current_time - timedelta(days=30 * value)
        elif unit == 'năm':
            updated_time = current_time - timedelta(days=365 * value)
        else:
            updated_time = None  # Handle unexpected units if needed
    
    return updated_time

# Helper function to try converting text to a float, or return text if not possible
def parse_value(value_text):
    match = re.search(r'(\d+,\d+|\d+)', value_text)
    if match:
        number_str = match.group(0).replace(',', '.')
        return float(number_str)
    return value_text  # Return original text if no number is found