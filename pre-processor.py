import re

# Define helper functions for classification
def is_vietnamese(char):
    # Match Vietnamese letters and diacritics
    return bool(re.match(r'[a-zA-Záàảãạăắằẳẵặâấầẩẫậđéèẻẽẹêếềểễệíìỉĩịóòỏõọôốồổỗộơớờởỡợúùủũụưứừửữựýỳỷỹỵ]', char))

def is_chinese(char):
    # Match Chinese characters in the CJK Unified Ideographs range
    return '\u4e00' <= char <= '\u9fff'

def is_emoji(char):
    # Match emojis using Unicode ranges
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
        # Check the classification of each character in the word
        if all(is_vietnamese(char) or char.isspace() for char in word):
            vietnamese_text.append(word)
        elif all(is_chinese(char) or char.isspace() for char in word):
            chinese_text.append(word)
        elif all(is_emoji(char) or char.isspace() for char in word):
            emojis.append(word)
        else:
            # Handle mixed content (e.g., "你好Chào" or "😄Chào")
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

def process_file(input_file_path):
    # Step 1: Read the content of the file
    with open(input_file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Step 2: Classify text into categories
    vietnamese_text, chinese_text, emojis = classify_text(content)

    # Step 3: Save the categorized text to separate files
    with open('vietnamese_text.txt', 'w', encoding='utf-8') as file:
        file.write(vietnamese_text)

    with open('chinese_text.txt', 'w', encoding='utf-8') as file:
        file.write(chinese_text)

    with open('emojis.txt', 'w', encoding='utf-8') as file:
        file.write(emojis)

    print("Text has been separated and saved.")

# Example usage
input_file_path = 'data/all_comments.txt'
process_file(input_file_path)