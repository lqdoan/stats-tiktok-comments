import os
import json
import re
import urllib

def appendComments(comments, filename='comments.json'):
    # Check if the file exists
    if os.path.exists(filename):
        try:
            # Read the existing data from the file
            with open(filename, 'r', encoding='utf-8') as f:
                existing_data = json.load(f)
            
            # Ensure existing_data is a list, and extend it with the new comments
            if isinstance(existing_data, list):
                existing_data.extend([comment.to_dict() for comment in comments])
            else:
                # If it's not a list (shouldn't happen in this case), start a new list
                existing_data = [comment.to_dict() for comment in comments]
        except (json.JSONDecodeError, FileNotFoundError):
            # Handle cases where the file is empty or the JSON is malformed
            existing_data = [comment.to_dict() for comment in comments]
    else:
        # If the file doesn't exist, just create a new list
        existing_data = [comment.to_dict() for comment in comments]
    
    # Write the updated data back to the file (ensuring the format is still a single list)
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(existing_data, f, ensure_ascii=False, indent=4)

    # print(f"Comments have been successfully appended to {filename}")


def url2Filename(url):
    # Parse the URL to break it into its components
    parsed_url = urllib.parse.urlparse(url)
    
    # Replace special characters in the URL path and query with '-'
    normalized = re.sub(r'[^\w\s-]', '-', parsed_url.netloc + parsed_url.path)
    normalized = re.sub(r'[-\s]+', '-', normalized).strip('-')
    
    # Truncate to a reasonable length (255 characters)
    normalized = normalized[:255]
    
    # Ensure it doesn't start or end with a dash or space
    normalized = normalized.strip('-')
    
    return normalized