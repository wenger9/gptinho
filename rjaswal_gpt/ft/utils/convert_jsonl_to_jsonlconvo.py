import json

def transform_to_conversational_format(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            data = json.loads(line)
            prompt = data["prompt"]
            completion = data["completion"]
            messages = [
                {"role": "system", "content": "You are a helpful assistant for business metrics extraction."},
                {"role": "user", "content": prompt},
                {"role": "assistant", "content": completion}
            ]
            output_data = {"messages": messages}
            json.dump(output_data, outfile)
            outfile.write('\n')

# Paths to your input and output files
training_input_file = 'meta/sys/ft/training/combined_training_data.jsonl'
training_output_file = 'meta/sys/ft/training/combined_training_data_conversational.jsonl'
validation_input_file = 'meta/sys/ft/training/validation/validation_data.jsonl'
validation_output_file = 'meta/sys/ft/training/validation/validation_data_conversational.jsonl'

# Transform the training and validation datasets
transform_to_conversational_format(training_input_file, training_output_file)
transform_to_conversational_format(validation_input_file, validation_output_file)
