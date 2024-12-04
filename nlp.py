import os
import re
import pandas as pd
from transformers import pipeline
from openpyxl import Workbook

# Directory paths
input_dir = "input_files"  # Directory containing input text files
output_dir = "output_files"  # Directory to save output files
os.makedirs(output_dir, exist_ok=True)

# Vietnamese Teen Slang Dictionary
slang_dict = {
    "khum": "không",
    "j": "gì",
    "dz": "d",
    "tr": "trời",
    "u là tr": "ôi là trời",
    "gòy": "rồi",
    "wa": "quá",
    "c oi": "chị ơi",
    "vui": "vui",
}

# Normalize Vietnamese slang
def normalize_vietnamese_slang(comment, slang_dict):
    for slang, standard in slang_dict.items():
        comment = re.sub(r'\b{}\b'.format(re.escape(slang)), standard, comment, flags=re.IGNORECASE)
    return comment

# Load Vietnamese sentiment analysis model
sentiment_pipeline = pipeline("sentiment-analysis", model="NlpHUST/vietnamese-sentiment")

# Sentiment analysis using NLP
def nlp_sentiment_analysis(comment):
    normalized_comment = normalize_vietnamese_slang(comment, slang_dict)  # Normalize slang
    analysis = sentiment_pipeline(normalized_comment)  # Run sentiment analysis
    label = analysis[0]['label']
    score = analysis[0]['score']
    
    # Map model labels to desired output format
    if label == "POS":
        return "[Positive]", {"Positive": score, "Negative": 0.0, "Neutral": 1.0 - score}
    elif label == "NEG":
        return "[Negative]", {"Positive": 0.0, "Negative": score, "Neutral": 1.0 - score}
    else:  # Treat anything else as Neutral
        return "[Neutral]", {"Positive": 0.0, "Negative": 0.0, "Neutral": 1.0}

# Process input files
summary_data = []
for file_name in os.listdir(input_dir):
    input_file_path = os.path.join(input_dir, file_name)
    output_file_name = f"{os.path.splitext(file_name)[0]}.xlsx"
    output_file_path = os.path.join(output_dir, output_file_name)

    data = []
    with open(input_file_path, 'r', encoding='utf-8') as infile:
        for line in infile:
            line = line.strip()
            if line:
                # Apply sentiment analysis
                label, tones = nlp_sentiment_analysis(line)
                data.append([label, line, tones["Positive"], tones["Negative"], tones["Neutral"]])

    # Save to Excel
    df = pd.DataFrame(data, columns=["Overall Label", "Comment Content", "Positive Tone", "Negative Tone", "Neutral Tone"])
    df.to_excel(output_file_path, index=False)

    # Summarize data
    summary_data.append({
        "File Name": file_name,
        "Positive Count": df[df["Overall Label"] == "[Positive]"].shape[0],
        "Negative Count": df[df["Overall Label"] == "[Negative]"].shape[0],
        "Neutral Count": df[df["Overall Label"] == "[Neutral]"].shape[0],
        "Total Comments": df.shape[0]
    })

# Create summary Excel file
summary_file_path = os.path.join(output_dir, "summary_labels_and_tones.xlsx")
summary_df = pd.DataFrame(summary_data)
summary_totals = {
    "File Name": "TOTAL",
    "Positive Count": summary_df["Positive Count"].sum(),
    "Negative Count": summary_df["Negative Count"].sum(),
    "Neutral Count": summary_df["Neutral Count"].sum(),
    "Total Comments": summary_df["Total Comments"].sum()
}
summary_df = pd.concat([summary_df, pd.DataFrame([summary_totals])], ignore_index=True)
summary_df.to_excel(summary_file_path, index=False)

print(f"Processing complete. Files saved in '{output_dir}' directory.")