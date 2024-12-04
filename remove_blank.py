import os
import re

# Function to remove invisible characters except for newline
def remove_invisible_characters_except_newline(text):
    return ''.join(c for c in text if c.isprintable() or c == '\n')

# Function to clean a single file
def clean_file(input_file_path, output_file_path):
    try:
        with open(input_file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        # Remove invisible characters except for the newline
        cleaned_lines = [remove_invisible_characters_except_newline(line) for line in lines]

        # Remove lines that are completely empty or contain only whitespace
        non_blank_lines = [line for line in cleaned_lines if line.strip()]

        # Remove duplicate lines
        seen = set()
        unique_lines = []
        for line in non_blank_lines:
            if line not in seen:
                unique_lines.append(line)
                seen.add(line)

        # Write the cleaned content to the new output file
        with open(output_file_path, 'w', encoding='utf-8') as outfile:
            outfile.writelines(unique_lines)
        
        print(f"Cleaned file saved to {output_file_path}")

    except Exception as e:
        print(f"Error cleaning file {input_file_path}: {e}")

# Function to process all files in the input folder
def process_all_files(input_folder, output_folder):
    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Iterate through all .txt files in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith('.txt'):
            input_file_path = os.path.join(input_folder, filename)
            output_file_path = os.path.join(output_folder, filename)
            clean_file(input_file_path, output_file_path)

if __name__ == '__main__':
    # Define the input and output folders
    input_folder = 'pre-processed_data/vietnamese'
    output_folder = 'pre-processed_data/clean_vietnamese_text'

    # Process all .txt files in the input folder
    process_all_files(input_folder, output_folder)

    print("All files have been cleaned and saved.")