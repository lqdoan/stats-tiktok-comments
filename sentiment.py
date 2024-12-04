import os
import time
# import argparse  # Import argparse for command-line arguments
# import google.generativeai as genai
from dotenv import load_dotenv
from openai import OpenAI


# Load API key from .env file
load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI()

input_file_path='processed_data/sentiment_label/vt-tiktok-com-ZSjm7D3LN.txt'
output_file_path = 'output_sentiments.txt'

with open(input_file_path, 'r', encoding='utf-8') as file:
    content = file.read()

completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {
            "role": "user",
            "content": f'''
I have this prompt:
Label the sentiment of the following Vietnamese comments (Positive, Negative, Neutral) related to a video about learning Chinese. Format the output as "[{{label}}] {{comment}}". 

Guidelines:
1. **Positive**: Comments that express curiosity, interest, or appreciation. This includes requests for more information, like "Cho hỏi ..." or " [...] là gì".
2. **Negative**: Comments that express dissatisfaction, criticism, or frustration.
3. **Neutral**: Comments that are neither positive nor negative, such as those expressing neutral observations or facts.

Be sure to apply the correct label based on the overall tone and intent of the comment. Output the labels in the exact format specified, with no additional explanations or bullet points.

---

**Input Comments:**
[Start of input text]
{content}
[End of input text]'''
        }
    ]
)

# print(completion.choices[0].message)

# Write the response to the output file
with open(output_file_path, 'w', encoding='utf-8') as file:
    file.write(completion.choices[0].message)

print(f"Sentiment labels have been written to {output_file_path}")

# import os
# from dotenv import load_dotenv
# import openai

# # Load API key from .env file
# load_dotenv()
# api_key = os.getenv('OPENAI_API_KEY')

# # Set the API key for OpenAI
# openai.api_key = api_key

# # Input and output file paths
# input_file_path = 'processed_data/sentiment_label/vt-tiktok-com-ZSjm7D3LN.txt'
# output_file_path = 'output_sentiments.txt'

# # Read content from the input file
# with open(input_file_path, 'r', encoding='utf-8') as file:
#     content = file.read()

# # Create a chat completion
# completion = openai.ChatCompletion.create(
#     model="gpt-3.5-turbo",
#     messages=[
#         {"role": "system", "content": "You are a helpful assistant."},
#         {
#             "role": "user",
#             "content": f'''
# I have this prompt:
# Label the sentiment of the following Vietnamese comments (Positive, Negative, Neutral) related to a video about learning Chinese. Format the output as "[{{label}}] {{comment}}". 

# Guidelines:
# 1. **Positive**: Comments that express curiosity, interest, or appreciation. This includes requests for more information, like "Cho hỏi ..." or " [...] là gì".
# 2. **Negative**: Comments that express dissatisfaction, criticism, or frustration.
# 3. **Neutral**: Comments that are neither positive nor negative, such as those expressing neutral observations or facts.

# Be sure to apply the correct label based on the overall tone and intent of the comment. Output the labels in the exact format specified, with no additional explanations or bullet points.

# ---

# **Input Comments:**
# [Start of input text]
# {content}
# [End of input text]'''
#         }
#     ]
# )

# # Get the response text
# response_text = completion['choices'][0]['message']['content']

# # Write the response to the output file
# with open(output_file_path, 'w', encoding='utf-8') as file:
#     file.write(response_text)

# print(f"Sentiment labels have been written to {output_file_path}")