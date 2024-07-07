import json
import glob

def read_json_files(file_paths):
    data = []
    for file_path in file_paths:
        with open(file_path, 'r') as file:
            data.extend(json.load(file))
    return data

def write_jsonl(data, output_file):
    with open(output_file, 'w') as file:
        for item in data:
            file.write(json.dumps(item) + '\n')

# List of JSON files to read
json_files = glob.glob('meta/sys/training/*.json')  # Assumes all 5 JSON files are in the current directory

# Read data from JSON files
combined_data = read_json_files(json_files)

# Write data to a JSONL file
output_file = 'meta/sys/training/combined_training_data.jsonl'
write_jsonl(combined_data, output_file)

print(f"Combined data written to {output_file}")
