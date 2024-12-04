import os
import time
import argparse  # Import argparse for command-line arguments
import google.generativeai as genai
from dotenv import load_dotenv
from openpyxl import Workbook

# Load API key from .env file
load_dotenv()
api_key = os.getenv('GOOGLE_API_KEY')

# Configure the genai model
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Process Vietnamese comments with AI sentiment labeling.")
parser.add_argument("start_line", type=int, help="The starting line number to begin processing from (1-based).")
args = parser.parse_args()
start_line = args.start_line

# File paths
input_file = "pre-processed_data/vietnamese_text.txt"
output_file = "processed_data/labeled_vietnamese_text.txt"
excel_file = "processed_data/count_label.xlsx"

# Load Vietnamese comments from a file
with open(input_file, "r", encoding="utf-8") as file:
    comments = file.readlines()

# Initialize label counts
label_counts = {"tích cực": 0, "tiêu cực": 0, "trung lập": 0}

# List to store labeled comments
labeled_comments = []

try:
    # Label each comment starting from the specified line
    for index, comment in enumerate(comments[start_line - 1:], start=start_line):
        comment = comment.strip()  # Remove leading/trailing whitespace
        if not comment:  # Skip empty lines
            continue

        # Use AI model to determine the sentiment
        # prompt = (
        #     # f"Label the sentiment of the following Vietnamese text as "
        #     # f"'tích cực' (positive), 'tiêu cực' (negative), or 'trung lập' (neutral):\n\n{comment}"
        #     f"Hãy đánh giá sắc thái của bình luận sau và dán nhãn "
        #     f"'tích cực' (positive), 'tiêu cực' (negative), or 'trung lập' (neutral):\n\n{comment}"
        # )
        
        prompt = (
            f"Please label the sentiment of the following Vietnamese text as one of the following: "
            f"'tích cực' (positive), 'tiêu cực' (negative), or 'trung lập' (neutral).\n"
            f"The sentiment should be based on the general tone of the comment, including "
            f"subtle or implied expressions of positivity or negativity. For example:\n\n"
            f"- 'Công nhận, rất tinh tế' should be labeled as 'tích cực' because it expresses admiration and positivity.\n"
            f"- 'Tôi không thích điều này' should be labeled as 'tiêu cực' because it expresses dislike.\n"
            f"- 'Sản phẩm bình thường' should be labeled as 'trung lập' because it is neutral.\n\n"
            f"Now, please label the sentiment of the following comment:\n\n{comment}"
        )
        
        response = model.generate_content(prompt)
        label = response.text.strip().lower()  # Extract label from response and normalize

        # Ensure the label is valid
        if label not in label_counts:
            label = "trung lập"  # Default to neutral if label is invalid

        # Update counts and prepare labeled comment
        label_counts[label] += 1
        labeled_comments.append(f"[{label}] {comment}")

        # Sleep for 0.2 seconds between API calls to avoid rate limits
        time.sleep(0.2)

except Exception as e:
    # Save progress if an error occurs
    last_line = index
    error_output_file = f"{output_file.replace('.txt', '')}_line_{last_line}.txt"
    print(f"An error occurred at line {last_line}: {e}")
    with open(error_output_file, "w", encoding="utf-8") as file:
        file.write("\n".join(labeled_comments))
    print(f"Progress saved to: {error_output_file}")
    raise  # Re-raise the error after saving progress

# Save labeled comments to a file
with open(output_file, "w", encoding="utf-8") as file:
    file.write("\n".join(labeled_comments))

# Calculate total count and ratios
total_comments = sum(label_counts.values())
label_ratios = {label: count / total_comments for label, count in label_counts.items()}

# Save counts and ratios to an Excel file
wb = Workbook()
ws = wb.active
ws.title = "Label Counts"

# Write header
ws.append(["Label", "Count", "Ratio"])

# Write data
for label, count in label_counts.items():
    ws.append([label, count, f"{label_ratios[label]:.4f}"])

# Save the Excel workbook
wb.save(excel_file)

print("Processing complete!")
print(f"Labeled comments saved to: {output_file}")
print(f"Label counts saved to: {excel_file}")
