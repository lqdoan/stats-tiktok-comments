import py_vncorenlp

# py_vncorenlp.download_model(save_dir='/root/Work/')

# Load VnCoreNLP from the local working folder that contains both `VnCoreNLP-1.2.jar` and `models` 
model = py_vncorenlp.VnCoreNLP(save_dir='/root/Work/')

keyword_list = []
with open('pre-processed_data/vietnamese_text.txt', 'r') as file:
    # Read the file line by line
    for i_line, line in enumerate(file,1):
        try:
            keywords = model.word_segment(text=line.lower())
        except:
            print(f'error at {i_line}: {line}')
            continue
        keyword_list += keywords

with open('extracted_keywords.txt', 'w') as file:
    file.writelines(line + '\n' for line in keyword_list)