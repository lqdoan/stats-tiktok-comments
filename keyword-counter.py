import csv
from collections import Counter
from openpyxl import Workbook
import re

# Read the text from a file
with open('./pre-processed_data/extracted_keywords.txt', 'r', encoding='utf-8') as file:
    text = file.read()

# Split the text into keywords by spaces and newlines
keywords = text.split()

# Filter special characters
keywords = [keyword for keyword in keywords if re.search(r'[a-zA-Z0-9áàảãạăắằẳẵặâấầẩẫậđéèẻẽẹêếềểễệíìỉĩịóòỏõọôốồổỗộơớờởỡợúùủũụưứừửữựýỳỷỹỵÁÀẢÃẠĂẮẰẲẴẶÂẤẦẨẪẬĐÉÈẺẼẸÊẾỀỂỄỆÍÌỈĨỊÓÒỎÕỌÔỐỒỔỖỘƠỚỜỞỠỢÚÙỦŨỤƯỨỪỬỮỰÝỲỶỸỴ]', keyword)]

# Count the occurrences of each keyword
keyword_count = Counter(keywords)

# Total number of keywords (for calculating ratio)
total_count = sum(keyword_count.values())

# Create a list of (keyword, count, ratio) tuples
keyword_data = [(keyword, count, count / total_count) for keyword, count in keyword_count.items()]

# Sort the list by occurrence count (descending)
sorted_keywords = sorted(keyword_data, key=lambda x: x[1], reverse=True)

# Output to file 1: all keywords sorted by occurrence in CSV format
with open('output_all_keywords.csv', 'w', newline='', encoding='utf-8') as file1:
    writer = csv.writer(file1)
    writer.writerow(['Keyword', 'Count', 'Ratio'])  # Write header
    for keyword, count, ratio in sorted_keywords:
        writer.writerow([keyword, count, f"{ratio:.4f}"])  # Write keyword, count, and ratio

# Output to file 2: top 100 keywords sorted by occurrence in Excel format
top_100_keywords = sorted_keywords[:100]

# Create a new Excel workbook for the top 100 keywords
wb_top_100 = Workbook()
ws_top_100 = wb_top_100.active
ws_top_100.title = "Top 100 Keywords"

# Write the header row for top 100 keywords
ws_top_100.append(['Keyword', 'Count', 'Ratio'])

# Write the data for top 100 keywords
for keyword, count, ratio in top_100_keywords:
    ws_top_100.append([keyword, count, f"{ratio:.4f}"])  # Append row to Excel

# Save the workbook for top 100 keywords as an Excel file
wb_top_100.save('output_top_100_keywords.xlsx')

# Output to file 3: all keywords in Excel format
wb_all_keywords = Workbook()
ws_all_keywords = wb_all_keywords.active
ws_all_keywords.title = "All Keywords"

# Write the header row for all keywords
ws_all_keywords.append(['Keyword', 'Count', 'Ratio'])

# Write the data for all keywords
for keyword, count, ratio in sorted_keywords:
    ws_all_keywords.append([keyword, count, f"{ratio:.4f}"])  # Append row to Excel

# Save the workbook for all keywords as an Excel file
wb_all_keywords.save('output_all_keywords.xlsx')

print("CSV and Excel files have been written successfully.")