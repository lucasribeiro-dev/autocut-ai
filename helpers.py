import json 
import os
import inspect

def format_timestamp(seconds: float) -> str:
    """Helper function to format seconds into SRT timestamp format."""
    millis = int(round(seconds * 1000))
    hours = millis // (3600 * 1000)
    minutes = (millis % (3600 * 1000)) // (60 * 1000)
    secs = (millis % (60 * 1000)) // 1000
    msecs = millis % 1000
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{msecs:03d}"

def markdown_json_to_dict(md_json: str):
    lines = md_json.strip().splitlines()
    json_lines = [line for line in lines if not line.strip().startswith("```")]
    json_str = "\n".join(json_lines)
    return json.loads(json_str)

def timestamp_to_seconds(timestamp: str) -> float:
    """
    Convert timestamp string (HH:MM:SS or HH:MM:SS,mmm) to seconds.
    
    Args:
        timestamp: Timestamp string in format HH:MM:SS or HH:MM:SS,mmm
        
    Returns:
        Time in seconds (float)
    """
    # Split off milliseconds if present
    if ',' in timestamp:
        time_part, ms_part = timestamp.split(',')
        milliseconds = int(ms_part)
    else:
        time_part = timestamp
        milliseconds = 0

    hours, minutes, seconds = map(int, time_part.split(':'))
    total_seconds = hours * 3600 + minutes * 60 + seconds + milliseconds / 1000.0
    return total_seconds

def get_file_from_same_path(file_name: str) -> str:
    """
    Returns the absolute path to a file located in the same directory as the module that called this function.

    This function uses the `inspect` module to automatically determine the Python file (module) that invoked it,
    and constructs the absolute path for the specified file based on the caller's directory.

    Args:
        file_name (str): The name of the file to locate (e.g., 'prompt.txt').

    Returns:
        str: The absolute path to the specified file in the caller's directory.
    
    Example:
        path = get_file_from_same_path('prompt.txt')
    """
    import inspect
    import os

    caller_frame = inspect.stack()[1]
    caller_file = caller_frame.filename

    base_dir = os.path.dirname(os.path.abspath(caller_file))
    return os.path.join(base_dir, file_name)