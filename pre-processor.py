import os
import re

# Define helper functions for classification
def is_vietnamese(char):
    return bool(re.match(r'[a-zA-Záàảãạăắằẳẵặâấầẩẫậđéèẻẽẹêếềểễệíìỉĩịóòỏõọôốồổỗộơớờởỡợúùủũụưứừửữựýỳỷỹỵ]', char))

def is_chinese(char):
    return '\u4e00' <= char <= '\u9fff'

def is_emoji(char):
    emoji_ranges = [
        (0x1F600, 0x1F64F),  # Emoticons
        (0x1F680, 0x1F6FF),  # Transport and Map Symbols
        (0x2600, 0x26FF),    # Miscellaneous Symbols
        (0x1F300, 0x1F5FF),  # Miscellaneous Symbols and Pictographs
        (0x2700, 0x27BF),    # Dingbats
        (0x1F900, 0x1F9FF),  # Supplemental Symbols and Pictographs
        (0x1FA70, 0x1FAFF),  # Symbols and Pictographs Extended-A
    ]
    for start, end in emoji_ranges:
        if start <= ord(char) <= end:
            return True
    return False

def classify_text(text):
    vietnamese_text = []
    chinese_text = []
    emojis = []

    # Split text into words, keeping spaces intact
    words = re.split(r'(\s+)', text)

    for word in words:
        if all(is_vietnamese(char) or char.isspace() for char in word):
            vietnamese_text.append(word)
        elif all(is_chinese(char) or char.isspace() for char in word):
            chinese_text.append(word)
        elif all(is_emoji(char) or char.isspace() for char in word):
            emojis.append(word)
        else:
            for char in word:
                if is_vietnamese(char):
                    vietnamese_text.append(char)
                elif is_chinese(char):
                    chinese_text.append(char)
                elif is_emoji(char):
                    emojis.append(char)
                else:
                    vietnamese_text.append(char)  # Default to Vietnamese

    return ''.join(vietnamese_text), ''.join(chinese_text), ''.join(emojis)

def process_file(input_file_path, vietnamese_folder, chinese_folder, emoji_folder):
    # Read the content of the file
    with open(input_file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Classify text into categories
    vietnamese_text, chinese_text, emojis = classify_text(content)

    # Ensure output folders exist
    os.makedirs(vietnamese_folder, exist_ok=True)
    os.makedirs(chinese_folder, exist_ok=True)
    os.makedirs(emoji_folder, exist_ok=True)

    # Get the filename from the path and use it for saving classified texts
    filename = os.path.basename(input_file_path)

    # Save the classified text to corresponding folders
    with open(os.path.join(vietnamese_folder, filename), 'w', encoding='utf-8') as file:
        file.write(vietnamese_text)

    with open(os.path.join(chinese_folder, filename), 'w', encoding='utf-8') as file:
        file.write(chinese_text)

    with open(os.path.join(emoji_folder, filename), 'w', encoding='utf-8') as file:
        file.write(emojis)

    print(f"Processed {filename} and saved classified text.")

def process_all_files(input_folder):
    # Define output folders for classified content
    vietnamese_folder = 'vietnamese'
    chinese_folder = 'chinese'
    emoji_folder = 'emoji'

    # Iterate through all .txt files in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith('.txt'):
            input_file_path = os.path.join(input_folder, filename)
            process_file(input_file_path, vietnamese_folder, chinese_folder, emoji_folder)

if __name__ == '__main__':
    # Define the input folder containing the .txt files
    input_folder = 'data/all_comments'

    # Process all .txt files in the folder
    process_all_files(input_folder)

    print("All files have been processed and saved in their respective folders.")