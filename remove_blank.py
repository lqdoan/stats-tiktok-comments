import re

# Function to remove invisible characters except for newline
def remove_invisible_characters_except_newline(text):
    return ''.join(c for c in text if c.isprintable() or c == '\n')

# Read the file and clean lines
with open('pre-processed_data/vietnamese_text.txt', 'r') as file:
    lines = file.readlines()

# Remove invisible characters except for the newline
cleaned_lines = [remove_invisible_characters_except_newline(line) for line in lines]

# Print out lengths and content for debugging
for line in cleaned_lines:
    print(f"Line length: {len(repr(line))}, Content: {repr(line)}")

# Remove lines that are completely empty or contain only whitespace
non_blank_lines = [line for line in cleaned_lines if line.strip()]

# Write the cleaned non-blank lines back to the file or to a new file
with open('pre-processed_data/vietnamese_text.txt', 'w') as file:
    file.writelines(non_blank_lines)