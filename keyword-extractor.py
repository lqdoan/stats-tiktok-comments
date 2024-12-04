import os
import py_vncorenlp

# Load VnCoreNLP from the local working folder that contains both `VnCoreNLP-1.2.jar` and `models` 
model = py_vncorenlp.VnCoreNLP(save_dir='/root/Work/')

def extract_keywords_from_file(input_file_path, output_file_path):
    keyword_list = []
    try:
        with open(input_file_path, 'r', encoding='utf-8') as file:
            # Read the file line by line
            for i_line, line in enumerate(file, 1):
                try:
                    keywords = model.word_segment(text=line.lower())
                    keyword_list += keywords
                except:
                    print(f'Error at line {i_line}: {line}')
                    continue

        # Write the extracted keywords to a separate file
        with open(output_file_path, 'w', encoding='utf-8') as file:
            file.writelines(keyword + '\n' for keyword in keyword_list)
        print(f"Keywords extracted and saved to {output_file_path}")
    except Exception as e:
        print(f"Error processing file {input_file_path}: {e}")

def process_all_files(input_folder, output_folder):
    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Iterate through all .txt files in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith('.txt'):
            input_file_path = os.path.join(input_folder, filename)
            output_file_path = os.path.join(output_folder, f'{os.path.splitext(filename)[0]}_keywords.txt')
            extract_keywords_from_file(input_file_path, output_file_path)

if __name__ == '__main__':
    # Define the input and output folders
    input_folder = 'pre-processed_data/vietnamese'
    output_folder = 'extracted_keywords'

    # Process all .txt files in the input folder
    process_all_files(input_folder, output_folder)

    print("All files have been processed and keywords saved.")