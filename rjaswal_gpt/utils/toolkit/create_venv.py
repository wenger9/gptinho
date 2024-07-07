import subprocess
import argparse
import sys
import os

from getpass import getuser

def download_spacy_models():
    print("Downloading spaCy models...")
    models = ["en_core_web_sm", "en_core_web_md", "en_core_web_lg"]  # Add more models if needed
    for model in models:
        subprocess.run(f"conda run -n {venv_name} python -m spacy download {model}", shell=True, check=True)
    print("spaCy models downloaded successfully.")

# Get the current user's username
username = getuser()
# Create an ArgumentParser object
parser = argparse.ArgumentParser(description='Create a virtual environment.')
# Add an optional argument for the virtual environment name
parser.add_argument('--venv', type=str, help='Name of the virtual environment', required=False)
# Parse the arguments
args = parser.parse_args()

# Check if the venv argument is provided
if args.venv:
    venv_name = args.venv
else:
    # Define the default virtual environment name
    venv_name = f"gpt-mtm-{username}"

# Check if the virtual environment exists
try:
    subprocess.run(["conda", "env", "list"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    venv_exists = venv_name in str(subprocess.run(["conda", "env", "list"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout)
except (subprocess.CalledProcessError, FileNotFoundError):
    venv_exists = False

# If the virtual environment exists, check if all the requirements are installed
if venv_exists:
    try:
        subprocess.run(f"conda run -n {venv_name} && pip freeze", shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        installed_packages = set(line.split("==")[0] for line in subprocess.run(f"conda run -n {venv_name} && pip freeze", shell=True,  check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.decode().splitlines())
        requirements_path = os.path.join(os.path.dirname(__file__), "..", "requirements.txt")
        with open(requirements_path, "r") as f:
            required_packages = set(line.strip() for line in f)
        missing_packages = required_packages - installed_packages
        if missing_packages:
            print(f"Installing missing packages in {venv_name} virtual environment...")
            # subprocess.run(f"conda run -n {venv_name} pip install -r {requirements_path}", shell=True, check=True)
            # subprocess.run(f"conda install -n {venv_name} pip -y", shell=True, check=True)
            download_spacy_models()
            print("spaCy models downloaded successfully.")
            print("Validating spaCy installation...")
            subprocess.run(f"conda run -n {venv_name} python -m spacy validate", shell=True, check=True)
            print("spaCy installation validated successfully.")
        else:
            print(f"{venv_name} virtual environment is up-to-date.")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print(f"Error checking or installing packages in {venv_name} virtual environment.")
        sys.exit(1)

# If the virtual environment doesn't exist, create it and install the requirements
else:
    try:
        print(f"Creating {venv_name} virtual environment...")
        subprocess.run(f"conda create -n {venv_name} python=3.9 -y", shell=True, check=True)
        
        # Install pip in the newly created virtual environment
        print(f"Installing pip in {venv_name} virtual environment...")
        subprocess.run(f"conda install -n {venv_name} pip -y", shell=True, check=True)

        print(f"Installing requirements in {venv_name} virtual environment...")
        requirements_path = os.path.join(os.path.dirname(__file__), "..", "requirements.txt")
        # subprocess.run(f"conda run -n {venv_name} && pip install -r {requirements_path}", shell=True, check=True)
        # subprocess.run(f"conda run -n {venv_name} {venv_name}/bin/pip install -r {requirements_path}", shell=True, check=True)
        subprocess.run(f"conda run -n {venv_name} {sys.prefix}/envs/{venv_name}/bin/pip install -r {requirements_path}", shell=True, check=True)

        download_spacy_models()
        print("spaCy models downloaded successfully.")
        print("Validating spaCy installation...")
        subprocess.run(f"conda run -n {venv_name} python -m spacy validate", shell=True, check=True)
        print("spaCy installation validated successfully.")        
        print(f"{venv_name} virtual environment created and requirements installed.")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print(f"Error creating or installing packages in {venv_name} virtual environment.")
        sys.exit(1)
