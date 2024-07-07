# rjaswal_gpt
 
## Overview

The [rjaswal_gpt](www.google.com) folder contains utilities and scripts related to the integration with OpenAI's language models, specifically for the purpose of generating insights and summaries based on user queries.

This folder includes functionality for interpreting user queries, generating GraphQL queries, fetching data from the backend, and using the OpenAI API to generate summaries and insights.

## Key Files and Modules

- `_gpt_graphql.py`: This is the main entry point for the OpenAI integration. It handles the process of translating user queries into GraphQL queries, fetching data, and generating summaries using the OpenAI API.
- `utils/query_extractor.py`: This module contains the [QueryExtractor](www.google.com) class, which is responsible for extracting relevant information from user queries, such as brand, region, category, and affiliate IDs, as well as fiscal year dates.
- `utils/logging_new.py`: This module provides a custom logger setup for the project.

## Installation

1. Clone the repository or navigate to the [rjaswal_gpt](www.google.com) folder.

2. Create a virtual environment (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # For Unix/Linux
   venv\Scripts\activate.bat  # For Windows
   ```

3. Install the required packages:
   ```
   pip install -r reqs.txt
   ```

## Usage

To use the `_gpt_graphql.py` script, you can run it from the command line with the following options:

```
python _gpt_graphql.py [-h] [-q QUERY] [-s]
```

- `-h`, `--help`: Show the help message and exit.
- `-q QUERY`, `--query QUERY`: Provide a user query to generate insights for.
- `-s`, `--synthetics`: Provide synthetic queries to generate insights for.

### Examples

1. Generate insights for a specific user query:
   ```
   python _gpt_graphql.py -q "What was the number of new Clinique consumers in North America for skincare in Q3 of fiscal year 2022?"
   ```

2. Generate a summary of predefined (synthetic) queries and their results:
   ```
   python _gpt_graphql.py -s
   ```

## Configuration

The following configuration variables are used in the `_gpt_graphql.py` script:

- `AZURE_OPENAI_API_KEY`: The API key for accessing the Azure OpenAI service.
- `AZURE_OPENAI_ENDPOINT`: The endpoint URL for the Azure OpenAI service.
- `GRAPHQL_API_ENDPOINT`: The endpoint URL for the GraphQL API.
- `SCHEMA_PATH`: The path to the JSON file containing the GraphQL schema.
- `API_VERSION`: The version of the Azure OpenAI API to use.
- `MODEL_NAME`: The name of the OpenAI model to use for generating summaries.

Make sure to set these variables with the appropriate values before running the script.

## Dependencies

The bare-minimum key dependencies for this project are listed in the `reqs.txt` file.

Please refer to the `reqs.txt` file for the complete list of dependencies and their versions.