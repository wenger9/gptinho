import argparse
import datetime
from copy import deepcopy
import json
import re

from openai import AzureOpenAI
from pathlib import Path

from utils.query_extractor import QueryExtractor
from utils.query_generator import QueryGenerator
from utils.data_retriever import DataRetriever
from utils.the_validator import TheValidator
# from utils.log_sessions import SessionLogger
# from utils.the_formatter import TheFormatter
from utils.toolkit.logging import setup_logger

from config import AZURE_OPENAI_API_KEY, AZURE_OPENAI_ENDPOINT, GRAPHQL_API_ENDPOINT, SCHEMA_PATH, API_VERSION, MODEL_NAME
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Azure OpenAI credentials and endpoint
AZURE_OPENAI_API_KEY = "9601fea95578484abc7e188e63911f2d"
AZURE_OPENAI_ENDPOINT = "https://cog-am-eus2-d-dsf-openai.openai.azure.com/"
GRAPHQL_API_ENDPOINT = "https://app-am-eastus-dev-dsf-cgmapp-mtmdev.ase-am-eastus-nonprod-shared-ase-dsf.am.elcompanies.net/graphql/"
SCHEMA_PATH = "meta/schema/mtm_graphql_dims+metrics_wo_affiliateId.json"
API_VERSION = "2024-02-15-preview"
MODEL_NAME = 'GPT4-TEST'
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

logger = setup_logger(__name__)

messages_path = Path(__file__).parent.joinpath('meta', 'roles',
                                               'messages_graphql_query.json')
with open(messages_path, 'r') as f:
    MESSAGES = json.load(f)
logger.debug(f"\n--------------------------\nMESSAGES: {MESSAGES}\n--------------------------\n")





# schema_path = Path(__file__).parent.parent.joinpath('data_assets', 'fixtures',
#                                              'data_assets',
#                                              'graphql_schema.json')

schema_path = Path(__file__).parent.joinpath('meta', 'schema',
                                             'mtm_graphql_dims+metrics_wo_affiliateId.json')
with open(schema_path, 'r') as f:
    schema_json = json.load(f)
SCHEMA_DESCRIPTION= json.dumps(schema_json, indent=2)

def load_and_serialize_schema(schema_path):
    with open(schema_path, 'r') as file:
        schema = json.load(file) 
        schema_str = json.dumps(schema, indent=2)
        return schema_str


# def check_missing_ids(brand_id, region_id, category_id):
#     # Check if any of the required identifiers are None and handle the error
#     if brand_id is None or region_id is None or category_id is None:
#         missing_ids = []
#         if brand_id is None:
#             missing_ids.append("brand_id")
#         if region_id is None:
#             missing_ids.append("region_id")
#         if category_id is None:
#             missing_ids.append("category_id")
#         error_message = f"Missing identifiers: {', '.join(missing_ids)}. No query generated."
#         logger.error(error_message)
#         raise ValueError(error_message)

# def generate_graphql_query(client, messages, brand_id, region_id, category_id, start_date, end_date, data_key, data_metrics):
#     updated_content = messages[3]["content"]

#     # Update the query template with the actual IDs.
#     if brand_id:
#         updated_content = updated_content.replace("{brand_id}", str(brand_id))
#     else:
#         updated_content = updated_content.replace("brandId: {brand_id}", "")

#     if region_id:
#         updated_content = updated_content.replace("{region_id}", str(region_id))
#     else:
#         updated_content = updated_content.replace("regionId: {region_id}", "")

#     if category_id:
#         updated_content = updated_content.replace("{category_id}", str(category_id))
#     else:
#         updated_content = updated_content.replace("categoryId: {category_id}", "")
    
#     if start_date:
#         updated_content = updated_content.replace("{start_date}", str(start_date))
#     else:
#         updated_content = updated_content.replace("startDate: {start_date}", "")
    
#     if end_date:
#         updated_content = updated_content.replace("{end_date}", str(end_date))
#     else:
#         updated_content = updated_content.replace("endDate: {end_date}", "")
    
#     if data_key:
#         updated_content = updated_content.replace("{data_key}", str(data_key))
#     else:
#         updated_content = updated_content.replace("dataKey: {data_key}", "")
    
#     if data_metrics:
#         updated_content = updated_content.replace("{data_metrics}", str(data_metrics))
#     else:
#         updated_content = updated_content.replace("dataMetrics: {data_metrics}", "")
    
#     messages[3]["content"] = updated_content

#     logger.debug(f"\n--------------------------\nmessages[0]['content']: SYS INSTRUCTION 0 {messages[0]['content']}\n--------------------------\n")
#     logger.debug(f"\n--------------------------\nmessages[1]['content']: SYS INSTRUCTION 1 {messages[1]['content']}\n--------------------------\n")
#     logger.debug(f"\n--------------------------\nmessages[2]['content']: SYS INSTRUCTION 2 {messages[2]['content']}\n--------------------------\n")
#     logger.debug(f"\n--------------------------\nmessages[3]['content']: UPDATED USER MESSAGE {messages[3]['content']}\n--------------------------\n")

#     try:
#         response = client.chat.completions.create(
#             model=MODEL_NAME,
#             messages=messages,
#             temperature=0.0
#         )
#         generated_graphql_query = response.choices[0].message.content.strip() if response.choices else "No query generated."
#         logger.debug(f"\n--------------------------\nresponse.choices[0].message.content: GENERATED GRAPHQL QUERY:\n\n{generated_graphql_query}\n--------------------------\n")

#         # Remove \n and \" characters from the generated query
#         cleaned_graphql_query = generated_graphql_query.replace('\\n', '').replace('\\"', '"')
#         # Remove tickmarks from the beginning and end of the generated graphql query
#         # cleaned_graphql_query = cleaned_graphql_query.strip('"')
#         logger.debug(f"\n--------------------------\nCleaned GraphQL Query:\n\n{cleaned_graphql_query}\n--------------------------\n")

#         return cleaned_graphql_query
    
#     except Exception as e:
#         logger.exception("Error generating GraphQL query:")
#         return "No query generated."

# def fetch_graphql_data(query):

#     headers = {"Content-Type": "application/json"}
#     payload = {"query": query}
#     response = requests.post(GRAPHQL_API_ENDPOINT, json=payload, headers=headers)

#     logger.debug(f"\n--------------------------\nGenerated GraphQL Query:\n\n{query}\n--------------------------\n")
#     logger.debug(f"\n--------------------------\nFetched GraphQL Data:\n\n{response.json()}\n--------------------------\n")
    
#     return response.json()

# def ai_generate_summary(client, data, data_key, data_metrics, brand_id, brand_name, region_id, region_name, category_id, category_name, start_date, end_date, user_query):

#     context_data_dimensions = f"Brand ID: {brand_id}, Brand Name: {brand_name}, Region ID: {region_id}, Region Name: {region_name}, Category ID: {category_id}, Category Name: {category_name}, Start Date: {start_date}, End Date: {end_date}, Data: {data}, Data Key: {data_key}, Data Metric Values: {data_metrics}, User Query: {user_query}"
#     print("\n\n\n context_data_dimensions: ", context_data_dimensions, "\n\n\n")
#     prompt = f"""
#     Please provide a concise, friendly, human-like, and professional summary in 1-2 sentences, in response to the user query: {user_query}. Please refer to the following for context:
#     {context_data_dimensions}

#     """

#     messages = [
#         {"role": "system", "content": "You are an AI assistant with the task of summarizing business data in a concise and professional manner."},
#         {"role": "user", "content": prompt}
#     ]

#     response = client.chat.completions.create(
#         model="GPT4-TEST",  
#         messages=messages,
#         temperature=0.0
#     )

#     try:
#         summary = response.choices[0].message.content
#     except Exception as e:
#         summary = f"Error in generating summary: {str(e)}"

#     return summary

# def save_session_log(session_info):
#     timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
#     log_filename = f"log/session/session_log_{timestamp}.json"
    
#     with open(log_filename, "w") as log_file:
#         json.dump(session_info, log_file, indent=2)


# def user_permitted_for_query(query, user):
#     brand_match = re.search(r'brandId:\s+(\d+)', query)
#     if brand_match:
#         query_brand_id = int(brand_match.group(1))
#         if not user.brands.filter(mtm_id=query_brand_id).exists():
#             return False

#     region_match = re.search(r'regionId:\s+(\d+)', query)
#     if region_match:
#         query_region_id = int(region_match.group(1))
#         if not user.regions.filter(mtm_id=query_region_id).exists():
#             return False

#     return True


def complete_gpt_query(client, extractor: QueryExtractor, generator: QueryGenerator, retriever: DataRetriever, validator: TheValidator, messages, query): #logger: SessionLogger,  user=None  formatter: TheFormatter,
    
    brand_name, brand_id = extractor.get_brand_id(query)
    region_name, region_id = extractor.get_region_id(query)
    category_name, category_id = extractor.get_category_id(query)

    logger.debug(f"\n--------------------------\nuser query: {query}\n--------------------------\n")
    # affiliate_name, affiliate_id = extractor.get_affiliate_id(query)
    start_date, end_date = extractor.extract_fy_dates(query)
    data_key_and_metrics = extractor.detect_data_key_ai(query, client)
     # Preprocess data_key and extract singular data_key and metrics_values
    data_key, data_metrics = extractor.extract_data_key_and_metrics(data_key_and_metrics)
    # data_key_ml= extractor.detect_data_key_ml(query)

    data_key_and_metrics_nuanced = extractor.extract_dimensions_and_metrics(query, client)
    # data_key_nuanced, data_metrics_nuanced = extractor.extract_data_key_and_metrics(data_key_and_metrics_nuanced)


    logger.debug(f"\n--------------------------\ndata_key via ai: {data_key}\n--------------------------\n")
    # logger.debug(f"\n--------------------------\ndata_key via ml: {data_key_ml}\n--------------------------\n")
    logger.debug(f"\n--------------------------\ndata_key_nuanced: {data_key_and_metrics_nuanced}\n--------------------------\n")
    logger.debug(f"\n--------------------------\ndata_metrics: {data_metrics}\n--------------------------\n")
    logger.debug(f"\n--------------------------\nbrand_name: {brand_name}\n--------------------------\n")
    logger.debug(f"\n--------------------------\nbrand_id: {brand_id}\n--------------------------\n")
    logger.debug(f"\n--------------------------\nregion_name: {region_name}\n--------------------------\n")
    logger.debug(f"\n--------------------------\nregion_id: {region_id}\n--------------------------\n")
    logger.debug(f"\n--------------------------\ncategory_name: {category_name}\n--------------------------\n")
    logger.debug(f"\n--------------------------\ncategory_id: {category_id}\n--------------------------\n")
    logger.debug(f"\n--------------------------\nstart_date: {start_date}\n--------------------------\n")
    logger.debug(f"\n--------------------------\nend_date: {end_date}\n--------------------------\n")
    
    # yield json.dumps({'type': 'debug', 'text': f"Brand Name: {brand_name}, Brand ID: {brand_id}"})
    # yield json.dumps({'type': 'debug', 'text': f"Region Name: {region_name}, Region ID: {region_id}"})
    # yield json.dumps({'type': 'debug', 'text': f"Category Name: {category_name}, Category ID: {category_id}"})
    # # yield json.dumps({'type': 'debug', 'text': f"Affiliate Name: {affiliate_name}, Affiliate ID: {affiliate_id}"})
    # yield json.dumps({'type': 'debug', 'text': f"Start Date: {start_date}, End Date: {end_date}"})
    # yield json.dumps({'type': 'debug', 'text': f"Data Key: {data_key}"})
    # yield json.dumps({'type': 'debug', 'text': f"Data Metrics: {data_metrics}"})
    # yield json.dumps({'type': 'debug', 'text': f"Extracted IDs: brand_id={brand_id}, region_id={region_id}, category_id={category_id}, affiliate_id={affiliate_id}, start_date={start_date}, end_date={end_date}, data_key={data_key}"})

    # # Check if any of the required identifiers are None and handle the error
    # try:
    #     brand_id, region_id, category_id = validator.check_missing_ids(brand_id, region_id, category_id)
    # except ValueError as e:
    #     yield json.dumps({'type': 'error', 'text': e})
    #     return
    
    # Initialize the system messages that will be used for chat completions.
    # and ensure the message strings are correctly formatted.
    messages = deepcopy(MESSAGES['graphql_query_messages'])
    # messages[0]['content'] = messages[0]['content'].format(schema_description=SCHEMA_DESCRIPTION)
    # messages[1]['content'] = messages[1]['content'].format()
    # messages[2]['content'] = messages[2]['content'].format()
    # messages[3]['content'] = messages[3]['content'].format(
    #     data_key=data_key or "",
    #     data_metrics=data_metrics or "",
    #     brand_id=brand_id or "None",
    #     region_id=region_id or "None", 
    #     category_id=category_id or "None",
    #     start_date=start_date or "None",
    #     end_date=end_date or "None",
    #     affiliate_id="None",
    #     user_query=query
    # )

    logger.debug(f"\n--------------------------\nmessages[3]['content']: {messages[3]['content']}\n--------------------------\n")

    # sys_msg_formatted = formatter.format_sys_msg(messages, SCHEMA_DESCRIPTION, data_key, data_metrics, brand_id, region_id, category_id, start_date, end_date, query)

    # messages = messages_graphql_query['graphql_query_messages']
    messages[3]['content'] = messages[3]['content'].replace('{category_id}', str(category_id) if category_id is not None else "None")
    messages[3]['content'] = messages[3]['content'].replace('{data_metrics}', str(data_metrics) if data_metrics is not None else "None")
    # messages[2]['content'] = messages[2]['content'].replace('{affiliate_id}', str(affiliate_id) if affiliate_id is not None else "None")
    messages[3]['content'] = messages[3]['content'].replace('{region_id}', str(region_id) if region_id is not None else "None")
    messages[3]['content'] = messages[3]['content'].replace('{start_date}', start_date if start_date is not None else "None")
    messages[3]['content'] = messages[3]['content'].replace('{brand_id}', str(brand_id) if brand_id is not None else "None")
    messages[3]['content'] = messages[3]['content'].replace('{end_date}', end_date if end_date is not None else "None")
    messages[3]['content'] = messages[3]['content'].replace('{data_key}', data_key if data_key is not None else "")
    messages[0]['content'] = messages[0]['content'].replace('{schema_description}', SCHEMA_DESCRIPTION)
    messages[3]['content'] = messages[3]['content'].replace('{user_query}', query)

    logger.debug(f"\n--------------------------\nmessages[3]['content']: {messages[3]['content']}\n--------------------------\n")

    # sys_msg_updated = formatter.update_sys_msg(messages, brand_id, region_id, category_id, start_date, end_date, data_key, data_metrics)
    # # Translate user query into GraphQL query
    graphql_query = generator.generate_graphql_query(MODEL_NAME, client, messages, brand_id,
        region_id, category_id, start_date, end_date, data_key, data_metrics) # formatter,
    
    logger.debug(f"\n--------------------------\ngraphql_query: {graphql_query}\n--------------------------\n")

    logger.debug(f"\n--------------------------\ndata_metrics: {data_metrics}\n--------------------------\n")

    # Execute the query
    retrieved_data = retriever.fetch_graphql_data(graphql_query)
    yield json.dumps({'type': 'debug',
                      'text': 'GraphQL Query: \n' + json.dumps(retrieved_data, indent=2)})

    # Summarize data in plain English
    summary = retriever.ai_generate_summary(client, retrieved_data, data_key,
        data_metrics, brand_id, brand_name, region_id, region_name, category_id, category_name, start_date, end_date, query)
    yield json.dumps({'type': 'final',
                      'text': 'Summary: \n' + summary})
    
    # Log query info / save session log
    # log_n_save = logger.log_query_info(query, brand_id, region_id, category_id, start_date, end_date, data_key, data_metrics, graphql_query, retrieved_data, summary)


def main():
    # Initializations
    client = AzureOpenAI(api_key=AZURE_OPENAI_API_KEY,
        api_version=API_VERSION,
        azure_endpoint=AZURE_OPENAI_ENDPOINT)
    
    extractor = QueryExtractor()
    generator = QueryGenerator(schema=SCHEMA_DESCRIPTION)
    retriever = DataRetriever(graphql_api_endpoint=GRAPHQL_API_ENDPOINT, model_name=MODEL_NAME)
    validator = TheValidator()
    # logger = SessionLogger()
    # formatter = TheFormatter()

    # Setup argument parser for: 1. User Query
    parser = argparse.ArgumentParser(description='Process user query:')
    parser.add_argument('-q', '--query', type=str, help='User query to interpret and execute')
    parser.add_argument('-s', '--synthetic', action='store_true', help='Execute preset queries from synthetic_queries*.json')
    args = parser.parse_args()
    
    if args.synthetic:
        # Load preset queries from synthetic_queries*.json
        with open('test/synthetic_queries_test_default.json', 'r') as file:
            synthetic_queries = json.load(file)

        # # Record session start time
        # session_info = {
        #     "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        #     "queries": []
        # }

        # Execute each preset query
        for index, query_data in enumerate(synthetic_queries, start=1):
            user_query = query_data['query']
            # expected_result = query_data['expectedResult']
            brand_name, brand_id = extractor.get_brand_id(user_query)
            region_name, region_id = extractor.get_region_id(user_query) 
            category_name, category_id = extractor.get_category_id(user_query)
            # affiliate_name, affiliate_id = extractor.get_affiliate_id(user_query)
            # affiliate_id = None # force affiliateId to be null
            
            start_date, end_date = extractor.extract_fy_dates(user_query)
            
            data_key_and_metrics = extractor.detect_data_key_ai(user_query, client)
            data_key, data_metrics = extractor.extract_data_key_and_metrics(data_key_and_metrics) # preprocess data_key and extract singular data_key and metrics

            # Load preset template, messages_graphql_query.json
            with open('meta/roles/messages_graphql_query.json', 'r') as file:
                messages_graphql_query = json.load(file)

            # # Replace placeholders in the template with actual values for:
            # # Dimensions: brand_id, region_id, category_id, start_date, end_date (add affiliate_id at a later stage)
            # # Payload Response: data
            # # Table Name: data_key
            # # Table Metrics: data_metrics
            # messages = messages_graphql_query['graphql_query_messages']
            # messages[2]['content'] = messages[2]['content'].replace('{category_id}', str(category_id) if category_id is not None else "None")
            # messages[2]['content'] = messages[2]['content'].replace('{data_metrics}', str(data_metrics) if data_metrics is not None else "None")
            # # messages[2]['content'] = messages[2]['content'].replace('{affiliate_id}', str(affiliate_id) if affiliate_id is not None else "None")
            # messages[2]['content'] = messages[2]['content'].replace('{region_id}', str(region_id) if region_id is not None else "None")
            # messages[2]['content'] = messages[2]['content'].replace('{start_date}', start_date if start_date is not None else "None")
            # messages[2]['content'] = messages[2]['content'].replace('{brand_id}', str(brand_id) if brand_id is not None else "None")
            # messages[2]['content'] = messages[2]['content'].replace('{end_date}', end_date if end_date is not None else "None")
            # messages[2]['content'] = messages[2]['content'].replace('{data_key}', data_key if data_key is not None else "")
            # messages[0]['content'] = messages[0]['content'].replace('{schema_description}', SCHEMA_DESCRIPTION)
            # messages[2]['content'] = messages[2]['content'].replace('{user_query}', user_query),

            # sys_msg_updated = formatter.update_sys_msg(messages_graphql_query, brand_id, region_id, category_id, start_date, end_date, data_key, data_metrics)

            # Translate user query into GraphQL query
            # generated_graphql_query = generate_graphql_query(client, messages, brand_id,  region_id, category_id, start_date, end_date)
            # generated_graphql_query = generate_graphql_query(client, messages, brand_id, region_id, category_id, start_date, end_date, data_key, data_metrics)
            graphql_query = generator.generate_graphql_query(MODEL_NAME, client, messages, brand_id, region_id, category_id, start_date, end_date, data_key, data_metrics)
            # With correct graphql query, fetch the data
            retrieved_data = retriever.fetch_graphql_data(graphql_query)
            summary = retriever.ai_generate_summary(client, retrieved_data, data_key, data_metrics, brand_id, brand_name, region_id, region_name, category_id, category_name, start_date, end_date, user_query)

            if "being calculated" in summary.lower():
                print("The response is still being calculated. Please try again in a few minutes as the GPT servers are busy.")
            else:
                print(f"-----------------\nSummary:\n {summary}\n-----------------\n")

            # query_info = {
            #     "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            #     "user_query": user_query,
            #     # "expected_result": expected_result,
            #     # "actual_result": table_data,
            #     "brand_id": brand_id,
            #     "region_id": region_id,
            #     "category_id": category_id,
            #     # "affiliate_id": affiliate_id,
            #     "start_date": start_date,
            #     "end_date": end_date,
            #     "data_key": data_key,
            #     "data_metrics": data_metrics,
            #     "generated_graphql_query": generated_graphql_query,
            #     "summary": summary
            # }

            # Log query info / save session log
            # log_n_save = logger.log_query_info(user_query, brand_id, region_id, category_id, start_date, end_date, data_key, data_metrics, graphql_query, summary)

    else:
        # # Record session start time
        # session_info = {
        #     "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        #     "queries": []
        # }
        # Execute user-defined query
        user_query = args.query

        # dims_and_mets = extractor.extract_dimensions_and_metrics(user_query, client)
        # logger.debug(f"\n--------------------------\ndims_and_mets: {dims_and_mets}\n--------------------------\n")

        if user_query:
            # for output in complete_gpt_query(client, extractor, generator, retriever, validator, logger, formatter, user_query):
            for output in complete_gpt_query(client, extractor, generator, retriever, validator, MESSAGES, user_query): #logger, formatter,
                output_dict = json.loads(output)
            if output_dict['type'] == 'debug':
                logger.debug(output_dict['text'])
            if output_dict['type'] == 'warning':
                logger.warning(output_dict['text'])
            if output_dict['type'] == 'error':
                logger.error(output_dict['text'])
            if output_dict['type'] == 'final':
                print(output_dict['text'])

        else:
            print("Please provide a query using the --query argument.")

if __name__ == "__main__":
    main()