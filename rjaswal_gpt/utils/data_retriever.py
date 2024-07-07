import requests
# from utils.log_sessions import logger
from config import GRAPHQL_API_ENDPOINT, MODEL_NAME

class DataRetriever:
    def __init__(self, graphql_api_endpoint, model_name):
        self.graphql_api_endpoint = GRAPHQL_API_ENDPOINT
        self.model_name = MODEL_NAME

    def fetch_graphql_data(self, query):
        headers = {"Content-Type": "application/json"}
        payload = {"query": query}
        response = requests.post(self.graphql_api_endpoint, json=payload, headers=headers)

        # logger.debug(f"\n--------------------------\nGenerated GraphQL Query:\n\n{query}\n--------------------------\n")
        # logger.debug(f"\n--------------------------\nFetched GraphQL Data:\n\n{response.json()}\n--------------------------\n")

        return response.json()

    def ai_generate_summary(self, client, data, data_key, data_metrics, brand_id, brand_name, region_id, region_name, category_id, category_name, start_date, end_date, user_query):
        context_data_dimensions = f"Brand ID: {brand_id}, Brand Name: {brand_name}, Region ID: {region_id}, Region Name: {region_name}, Category ID: {category_id}, Category Name: {category_name}, Start Date: {start_date}, End Date: {end_date}, Data: {data}, Data Key: {data_key}, Data Metric Values: {data_metrics}, User Query: {user_query}"
        print("\n\n\n context_data_dimensions: ", context_data_dimensions, "\n\n\n")
        prompt = f"""
        Please provide a concise, friendly, human-like, and professional summary in 1-2 sentences, in response to the user query: {user_query}. Please refer to the following for context:
        {context_data_dimensions},

        and to be exact, please describe the relevant data metrics {data_metrics} that pertain to the specific brand {brand_name}, region {region_name}, and category {category_name} that the user query has requested information about.

        """

        messages = [
            {"role": "system", "content": "You are an AI assistant with the task of summarizing business data in a concise and professional manner."},
            {"role": "user", "content": prompt}
        ]

        response = client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            temperature=0.0
        )

        try:
            summary = response.choices[0].message.content
        except Exception as e:
            summary = f"Error in generating summary: {str(e)}"

        return summary