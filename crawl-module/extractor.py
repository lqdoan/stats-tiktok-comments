import os
import json

def extract_comments_from_json_files(folder_path, output_folder):
    # Ensure the output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Traverse through all files in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith('.json'):
            json_file_path = os.path.join(folder_path, filename)
            output_file_path = os.path.join(output_folder, filename.replace('.json', '.txt'))
            
            # Open the output file for each JSON file
            with open(output_file_path, 'a', encoding='utf-8') as output:
                # Read the JSON file
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
    # Define folder path and output folder
    folder_path = 'crawl_data'  # Make sure 'crawl_data' is the correct folder path
    output_folder = 'all_comments'

    # Call the function to extract comments
    extract_comments_from_json_files(folder_path, output_folder)

    print(f"All comments have been extracted to the '{output_folder}' folder.")