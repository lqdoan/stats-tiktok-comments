import os
import openpyxl

# Function to count the number of lines in each .txt file and save to an Excel file
def count_lines_in_files(folder_path, output_file):
    # Create a new workbook and sheet
    wb = openpyxl.Workbook()
    sheet = wb.active
    sheet.title = 'Comment Counts'

    # Add header row
    sheet['A1'] = 'Url'
    sheet['B1'] = 'Số comment'

    row = 2  # Start from the second row for data
    # Iterate through all .txt files in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):
            file_path = os.path.join(folder_path, filename)
            
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    lines = file.readlines()
                    # Write the filename and line count to the Excel sheet
                    sheet[f'A{row}'] = filename
                    sheet[f'B{row}'] = len(lines)
                    row += 1
            except Exception as e:
                print(f"Error reading file {filename}: {e}")

    # Save the workbook to the output file
    wb.save(output_file)
    print(f"Data has been saved to {output_file}")

if __name__ == '__main__':
    # Define the folder path containing the .txt files
    folder_path = 'pre-processed_data/clean_vietnamese_text'
    
    # Define the output Excel file path
    output_file = 'comment_counts.xlsx'
    
    # Count lines and save the data to the Excel file
    count_lines_in_files(folder_path, output_file)