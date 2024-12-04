import os
import pandas as pd
from collections import Counter

# Define the path to the folder containing the text files
folder_path = "processed_data/sentiment_label"

# Function to process each text file
def process_file(file_path):
    labels = []
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            # Extract the label from each line (assuming the label is enclosed in [])
            label = line.split(']')[0].strip('[')
            labels.append(label)
    return labels

# Get a list of all text files in the folder
files = [f for f in os.listdir(folder_path) if f.endswith('.txt')]

# Initialize a dictionary to store the label counts for each file
file_label_counts = {}
all_labels = []

# Process each file and store the label counts
for file in files:
    file_path = os.path.join(folder_path, file)
    labels = process_file(file_path)
    label_counts = Counter(labels)
    file_label_counts[file] = label_counts
    all_labels.extend(labels)

# Create a DataFrame for the summary (all files)
all_label_counts = Counter(all_labels)
summary_data = {"Label": list(all_label_counts.keys()), "Count": list(all_label_counts.values())}
summary_df = pd.DataFrame(summary_data)
summary_df["Ratio"] = summary_df["Count"] / summary_df["Count"].sum()

# Create an Excel writer
with pd.ExcelWriter('label_counts_summary.xlsx') as writer:
    # Write the summary to the first sheet
    summary_df.to_excel(writer, sheet_name='Summary', index=False)
    
    # Process each file and write the counts and ratios to a separate sheet
    for file, label_counts in file_label_counts.items():
        label_data = {"Label": list(label_counts.keys()), "Count": list(label_counts.values())}
        df = pd.DataFrame(label_data)
        df["Ratio"] = df["Count"] / df["Count"].sum()
        # Write to the respective sheet named after the file
        df.to_excel(writer, sheet_name=file, index=False)

print("Excel file 'label_counts_summary.xlsx' has been created.")