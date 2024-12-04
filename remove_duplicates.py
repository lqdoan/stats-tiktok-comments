def remove_duplicates(input_file, output_file):
    seen = set()  # This will track lines we've already seen
    with open(input_file, 'r') as infile:
        lines = infile.readlines()

    with open(output_file, 'w') as outfile:
        for line in lines:
            if line not in seen:  # If we haven't seen this line before
                outfile.write(line)  # Write the line to the output file
                seen.add(line)  # Mark this line as seen

# Example usage
input_file = 'pre-processed_data/vietnamese_text.txt'  # Input file containing lines
output_file = 'pre-processed_data/vietnamese_text.txt'  # Output file after removing duplicates
remove_duplicates(input_file, output_file)