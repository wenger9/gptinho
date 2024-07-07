# Import necessary packages
from openai import AzureOpenAI
import time
import argparse

# Define function to parse command-line arguments
def parse_args():
    parser = argparse.ArgumentParser(description="Fine-tune GPT model with user-defined parameters.")
    parser.add_argument("--epochs", type=int, default=-1, help="Number of epochs to train the model.")
    parser.add_argument("--batch_size", type=int, default=-1, help="Batch size to use during training.")
    parser.add_argument("--learning_rate", type=float, default=1.0, help="Learning rate multiplier.")
    # parser.add_argument("--max_steps", type=int, default=None, help="Maximum number of steps to train the model.")
    return parser.parse_args()

def main():
    try:
        args = parse_args()

        # Azure OpenAI credentials and endpoint
        AZURE_OPENAI_API_KEY = "9601fea95578484abc7e188e63911f2d"
        AZURE_OPENAI_ENDPOINT = "https://cog-am-eus2-d-dsf-openai.openai.azure.com/"
        API_VERSION = "2024-02-01"
        MODEL_NAME = "gpt-35-turbo-0125"#"gpt-35-turbo-0613"

        print("Initializing AzureOpenAI client...")
        client = AzureOpenAI(
            azure_endpoint=AZURE_OPENAI_ENDPOINT, 
            api_key=AZURE_OPENAI_API_KEY,
            api_version=API_VERSION
        )

        training_file_name = 'meta/sys/ft/training/combined_training_data_conversational.jsonl'
        validation_file_name = 'meta/sys/ft/training/validation/validation_data_conversational.jsonl'

        # Upload the training and validation dataset files
        print("Uploading training file...")
        training_response = client.files.create(
            file=open(training_file_name, "rb"), purpose="fine-tune"
        )
        training_file_id = training_response.id

        print("Uploading validation file...")
        validation_response = client.files.create(
            file=open(validation_file_name, "rb"), purpose="fine-tune"
        )
        validation_file_id = validation_response.id

        print("Training file ID:", training_file_id)
        print("Validation file ID:", validation_file_id)

        # Ensure the files are processed
        def check_file_status(file_id):
            response = client.files.retrieve(file_id)
            return response.status

        print("Checking file processing status...")
        while True:
            training_status = check_file_status(training_file_id)
            validation_status = check_file_status(validation_file_id)
            
            print(f"Training file status: {training_status}")
            print(f"Validation file status: {validation_status}")

            if training_status == "processed" and validation_status == "processed":
                break
            elif training_status == "failed" or validation_status == "failed":
                raise Exception("File processing failed.")
            
            time.sleep(10)  # Check every 10 seconds

        print("Creating fine-tuning job...")
        response = client.fine_tuning.jobs.create(
            training_file = training_file_id,
            validation_file = validation_file_id,
            model = MODEL_NAME,  # Enter base model name. Note that in Azure OpenAI the model name contains dashes and cannot contain dot/period characters.
            hyperparameters={
                "n_epochs": args.epochs,
                "batch_size": args.batch_size,
                "learning_rate_multiplier": args.learning_rate
            },
            suffix = "rjaswal_202405211320"
            # max_steps=args.max_steps
        )

        job_id = response.id

        # You can use the job ID to monitor the status of the fine-tuning job.
        print("Job ID:", job_id)
        print("Status:", response.status)
        print(response)

        # Monitor the fine-tuning process
        def check_fine_tune_status(job_id):
            status = client.fine_tuning.jobs.retrieve(job_id)
            return status 

        # Check the status of the fine-tuning job
        while True:
            status = check_fine_tune_status(job_id)
            print(status)
            if status.status == 'succeeded':
                fine_tuned_model_id = status.fine_tuned_model
                print(f"Fine-tuning job completed successfully with model ID: {fine_tuned_model_id}")
                break
            elif status.status == 'failed':
                print("Fine-tuning job failed.")
                break
            time.sleep(60)  # Check every 60 seconds
    except Exception as e:
        print(f"An error occurred: {e}")    

if __name__ == "__main__":
    main()