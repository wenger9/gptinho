import json
import os
import sys
import time
from pathlib import Path

from openai import AzureOpenAI

sys.path.append('rjaswal_gpt')

from rjaswal_gpt.utils.query_extractor import QueryExtractor
from rjaswal_gpt.utils.query_generator import QueryGenerator
from rjaswal_gpt.utils.data_retriever import DataRetriever
from rjaswal_gpt.utils.log_sessions import SessionLogger
from rjaswal_gpt.utils.the_validator import TheValidator
# from rjaswal_gpt.utils.the_formatter import TheFormatter
from rjaswal_gpt._gpt_graphql import complete_gpt_query

schema_path = Path(__file__).parent.parent.joinpath('rjaswal_gpt', 'meta', 'schema',
    'mtm_graphql_dims+metrics_wo_affiliateId.json')
with open(schema_path, 'r') as f:
    schema_json = json.load(f)
SCHEMA_DESCRIPTION= json.dumps(schema_json, indent=2)


# Azure OpenAI credentials and endpoint
AZURE_OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
AZURE_OPENAI_ENDPOINT = os.environ.get('OPENAI_ENDPOINT')
GRAPHQL_API_ENDPOINT = os.environ.get('GRAPHQL_ENDPOINT')
API_VERSION = "2024-02-15-preview"
GPT_MODEL = "GPT4-TEST"

# Variables and objects to use in getting GPT data
EXTRACTOR = QueryExtractor()
GENERATOR = QueryGenerator(SCHEMA_DESCRIPTION)
RETRIEVER = DataRetriever(GRAPHQL_API_ENDPOINT, GPT_MODEL)
VALIDATOR = TheValidator()
LOGGER = SessionLogger()
# FORMATTER = TheFormatter()

with open('rjaswal_gpt/meta/sys/roles/messages_graphql_query.json', 'r') as f:
    MESSAGES = json.load(f)

# Initialize the OpenAI client with Azure credentials
CLIENT = AzureOpenAI(
    api_key=AZURE_OPENAI_API_KEY,
    api_version=API_VERSION,
    azure_endpoint=AZURE_OPENAI_ENDPOINT
)

def get_mtm_response(query, user):
    """Iterate through steps of calling GPT on user query."""
    for output in complete_gpt_query(CLIENT, EXTRACTOR, GENERATOR, RETRIEVER, VALIDATOR, MESSAGES, query):
        time.sleep(0.01) # Won't work without sleep
        output_dict = json.loads(output)
        if output_dict['type'] == 'debug':
            yield json.dumps({'type': 'intermediate',
                              'text': output_dict['text']})
        if output_dict['type'] == 'final':
            yield json.dumps({'type': 'final',
                              'text': output_dict['text']})
        if output_dict['type'] == 'error' or output_dict['type'] == 'warning':
            yield json.dumps({'type': 'final',
                              'text': output_dict['text']})
