# Read the file and remove blank lines
with open('pre-processed_data/vietnamese_text.txt', 'r') as file:
    lines = file.readlines()

# Remove blank lines (lines that are just empty or contain only whitespace)
non_blank_lines = [line for line in lines if line.strip()]

# Write the non-blank lines back to the file or to a new file
with open('pre-processed_data/vietnamese_text.txt', 'w') as file:
    file.writelines(non_blank_lines)