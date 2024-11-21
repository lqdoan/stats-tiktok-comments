import os
import json

def extract_comments_from_json_files(folder_path, output_file):
    # Open the output file in append mode
    with open(output_file, 'a', encoding='utf-8') as output:
        # Traverse through all files in the folder
        for filename in os.listdir(folder_path):
            if filename.endswith('.json'):
                json_file_path = os.path.join(folder_path, filename)
                
                # Read the json file
                with open(json_file_path, 'r', encoding='utf-8') as json_file:
                    try:
                        comments_data = json.load(json_file)
                        
                        # Iterate through each comment and extract the 'text' field
                        for comment in comments_data:
                            comment_text = comment.get('text', '')
                            if comment_text:
                                # Append the comment text to the output file
                                output.write(comment_text + '\n')  # Add newline for separation
                    except json.JSONDecodeError:
                        print(f"Error decoding JSON in file {json_file_path}")


if __name__ == '__main__':
    # Define folder path and output file
    folder_path = 'crawl_data'  # Make sure 'data' is the correct folder path
    output_file = 'all_comments.txt'

    # Call the function to extract comments
    extract_comments_from_json_files(folder_path, output_file)

    print(f"All comments have been extracted to {output_file}")