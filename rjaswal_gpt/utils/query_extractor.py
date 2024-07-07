import re
import json
import spacy
import joblib
# import logging

from spacy.vocab import Vocab
from spacy.tokens import Doc

from utils.toolkit.logging import setup_logger

from collections import Counter
from openai import AzureOpenAI
from pathlib import Path

from fuzzywuzzy import process, fuzz
from datetime import datetime
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Azure OpenAI credentials and endpoint
AZURE_OPENAI_API_KEY = "9601fea95578484abc7e188e63911f2d"
AZURE_OPENAI_ENDPOINT = "https://cog-am-eus2-d-dsf-openai.openai.azure.com/"
GRAPHQL_API_ENDPOINT = "https://app-am-eastus-dev-dsf-cgmapp-mtmdev.ase-am-eastus-nonprod-shared-ase-dsf.am.elcompanies.net/graphql/"
SCHEMA_PATH = "meta/schema/mtm_graphql_dims+metrics_trunc.json"
API_VERSION = "2024-02-15-preview"
MODEL_NAME = 'GPT4-TEST'
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

MAPS_PATH = Path(__file__).parent.parent.joinpath('meta', 'maps')

class QueryExtractor:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_lg")
        self.logger = setup_logger(__name__)
        self.table_themes = json.load(open(MAPS_PATH.joinpath('data_tables', 'mtm_data_table_themes.json')))
        self.brand_mapping = self.load_mapping(MAPS_PATH.joinpath('dimensions', 'mtm_brandname_to_brandid.json'))
        self.region_mapping = self.load_mapping(MAPS_PATH.joinpath('dimensions', 'mtm_regionname_to_regionid.json'))
        self.category_mapping = self.load_mapping(MAPS_PATH.joinpath('dimensions', 'mtm_categoryname_to_categoryid.json'))
        self.affiliate_mapping = self.load_mapping(MAPS_PATH.joinpath('dimensions', 'mtm_affiliatename_to_affiliateid.json'))

    @staticmethod
    def load_mapping(file_path):
        '''
        _______________________________________________________________
        - loads a JSON file and returns the content.
        - returns an error message if the file is not found or if the content is not valid.
        '''
        try:
            path = Path(file_path)
            with path.open('r', encoding='utf-8') as file:
                data = json.load(file)
            # print(f"\n---------------------\nSuccessfully loaded file: {file_path}\n---------------------\n\n")
            return data
        except FileNotFoundError:
            print(f"File not found: {file_path}")
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON from {file_path}: {e}")
        except Exception as e:
            print(f"An error occurred while loading {file_path}: {e}")

    def get_id_from_query(self, query, mapping):
        '''
        _______________________________________________________________
        - extracts the ID from a user query.
        - returns the best match for the parameterName, and the parameterId.
        '''
        if mapping is None:
            return None, 0
        
        # Convert mapping keys to lowercase and store in a new dictionary
        lower_mapping = {k.lower(): v for k, v in mapping.items()}
        
        # Split the query into words and look for the best match for each word
        query_words = query.lower().split()
        # logger.debug(f"query_words: {query_words}, mapping: {mapping}, lower_mapping: {lower_mapping}")
        
        # Initialize variables to track the best match and its score
        best_match, highest_score = None, 0
        
        # Check each word in the query against all lowercased names
        for word in query_words:
            # Use fuzzywuzzy's process.extractOne to find the best match for the current word
            result = process.extractOne(word, lower_mapping.keys(), scorer=fuzz.token_set_ratio, score_cutoff=85)
            # logger.debug(f"lower_mapping.keys(): {lower_mapping.keys()}")
            # logger.debug(f"Testing the word, '{word}'. The match score is: {result}")
            
            if result:
                match, score = result
                # logger.debug(f"This is the closest match for {word}: {match} with a match score of {score}")
                print("\n\n\n match: ", match, "\n\n\n")
                print("\n\n\n score: ", score, "\n\n\n")
                if score > highest_score:
                    best_match, highest_score = match, score
                    # logger.debug(f"The best match for {word} is {best_match} with a score of {highest_score}")
        
        if best_match:
            return best_match, lower_mapping.get(best_match)
        else:
            return None, 0
    

    # def get_brand_id(self, query):
    #     '''
    #     _______________________________________________________________
    #     - extracts the brand ID from a user query.
    #     - returns the best match for the brand ID, and the brand ID.
    #     '''
    #     try:
    #         best_match, brand_id = self.get_id_from_query(query, self.brand_mapping)
    #         print("\n\n\n hello # 1 \n\n\n")

    #         if brand_id is None:
    #             brand_id = list(self.brand_mapping.values())
    #             print("\n\n\n hello \n\n\n")
    #             print("\n\n\nbrand_id: ", brand_id, "\n\n\n")
    #         self.logger.debug(f"The best match for brand_id found in the user query, {query}, is {best_match} with a brand_id of {brand_id}")    

    #         return best_match, brand_id
    #     except AttributeError:
    #         self.logger.debug("Failed to get brand ID. Check if brand_mapping is properly initialized.")
    #         return None, None

    def get_brand_id(self, query):
        try:
            best_match, brand_id = self.get_id_from_query(query, self.brand_mapping)
            if brand_id is None:
                # If brand_id is None (Total Brands), use all available brand IDs except 0
                best_match = 'Total Brands'
                brand_id = 0
            return best_match, brand_id
        except AttributeError:
                self.logger.debug("Failed to get brand ID. Check if brand_mapping is properly initialized.")
                return None, None

    def get_region_id(self, query):
        '''
        _______________________________________________________________
        - extracts the region ID from a user query.
        - returns the best match for the region ID, and the region ID.
        '''
        try:
            best_match, region_id = self.get_id_from_query(query, self.region_mapping)
            if region_id is None:
                best_match = "All Regions"
                region_id = 0
            return best_match, region_id
        except AttributeError:
            self.logger.debug("Failed to get region ID. Check if region_mapping is properly initialized.")
            return None, None

    def get_category_id(self, query):
        '''
        _______________________________________________________________
        - extracts the category ID from a user query.
        - returns the best match for the category ID, and the category ID.
        '''
        try:
            best_match, category_id = self.get_id_from_query(query, self.category_mapping)
            if category_id is None:
                best_match = "All Categories"
                category_id = 0
            return best_match, category_id
        except AttributeError:
            self.logger.debug("Failed to get category ID. Check if category_mapping is properly initialized.")
            return None, None

    # def get_affiliate_id(self, query):
    #     '''
    #     _______________________________________________________________
    #     - extracts the affiliate ID from a user query.
    #     - returns the best match for the affiliate ID, and the affiliate ID.
    #     '''
    #     try:
    #         best_match, affiliate_id = self.get_id_from_query(query, self.affiliate_mapping)
    #         if affiliate_id is None:
    #             affiliate_id = list(self.affiliate_mapping.values())
    #         return best_match, affiliate_id
    #     except AttributeError:
    #         self.logger.debug("Failed to get affiliate ID. Check if affiliate_mapping is properly initialized.")
    #         return None, None

    def extract_fy_dates(self, query):
        '''
        _______________________________________________________________
        - extracts the fiscal year dates from a user query.
        - returns the start and end dates in YYYY-MM-DD format.
        '''
        # Extended regular expression to capture various FY mentions
        fy_pattern = r'(?:fiscal year|fiscal|FY)\s*(\d{2,4})'
        year_pattern = r'\b(\d{2,4})\b'  # Standalone year pattern

        # Search for fiscal year patterns first
        fy_match = re.search(fy_pattern, query, re.IGNORECASE)
        if fy_match:
            year = int(fy_match.group(1))
        else:
            # If no explicit fiscal year, look for any standalone year mention
            year_match = re.search(year_pattern, query)
            if year_match:
                year = int(year_match.group(1))
            else:
                return None, None

        # Adjust for two-digit year format
        if year < 100:
            year += 2000  # Assuming current century

        # Compute the fiscal year dates
        start_date = f"{year-1}-07-01"
        end_date = f"{year}-06-30"

        if start_date is None or end_date is None:
            end_date = datetime.now().strftime("%Y-%m-%d")
            start_date = (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d")
       
        return start_date, end_date

    def extract_data_key_and_metrics(self, data_key_string):
        '''
        _______________________________________________________________
        - extracts the data key and metrics from a data key string.
        - returns the data key and metrics.
        '''
        parts = data_key_string.strip().replace('"', '').replace("'", '').replace(' ', '').replace('[', '').replace(']', '').split(':')
        data_key = parts[0]
        data_metrics = parts[1].strip().replace("'", "").replace(" ", "").replace("[", "").replace("]", "")
        self.logger.debug(f"\n-----------------------------------------------------------------------------------\nTable Name    ---> {data_key}\n\nTable Metrics ---> {data_metrics}\n-----------------------------------------------------------------------------------\n")

        return data_key, data_metrics
        
    def detect_data_key_ai(self, user_query, client):
        '''
        _______________________________________________________________
        - detects the data key from a user query using AI.
        - returns the data key.
        '''
        data_key_explanation = """
        The data_key is a string that represents the key in the key:value pairs shown in the following JSON schema. The value(s) to this key are the specific metrics that are available for this key, in the key:value pairs. Please use the following JSON schema to detect which specific, singular data_key maps to the metric, or metrics, that are explicitly or implicitly identified from the user query:

        {
            "consumerAggregate": ["new", "projection", "reactivated", "retained"],
            "consumerTable": ["newAmount", "newPlan", "newYoy", "projection", "reactivatedAmount", "reactivatedPlan", "reactivatedYoy", "repeat", "repeatYoy", "retainedAmount", "retainedPlan", "retainedYoy", "retention", "retentionYoy", "totalAmount", "totalPlan", "totalYoy"],
            "financeCard": ["estimate", "grossToNetAmount", "grossToNetBudget", "grossToNetLe", "grossToNetYoy", "marginAmount", "marginBudget", "marginLe", "marginYoy", "netAmount", "netBudget", "netLe", "netYoy", "nopAmount", "nopBudget", "nopLe", "nopYoy"],
            "footTrafficTable": ["footTrafficYoy", "footTraffic"],
            "influencerTable": ["brands"],
            "innovation": ["launches"],
            "inventory": ["cogsNet", "cogsNetMom", "cogsNetTarget", "cogsNetVariance", "excess", "excessMom", "excessVariance", "excessTarget", "fillRate", "fillRateMom", "fillRateTarget", "fillRateVariance", "inventory", "inventoryMom", "inventoryTarget", "inventoryVariance", "lag", "lagMom", "lagTarget", "lagVariance"],
            "marketRankTable": ["aggregationLevel", "brands"],
            "ownedMedia": ["sources"],
            "ownedSocial": ["channels"],
            "productRole": ["roles"],
            "regions": ["abbreviation", "active", "displayName", "id", "name", "superRegion"],
            "retailCard": ["retailAmount", "retailYoy"],
            "smapTable": ["advertising", "advertisingNetPct", "advertisingPy", "advertisingYoy", "estimate", "marketing", "marketingNetPct", "marketingPy", "marketingYoy", "promotion", "promotionNetPct", "promotionPy", "promotionYoy", "selling", "sellingNetPct", "sellingPy", "sellingYoy", "total", "totalNetPct", "totalPy", "totalYoy"],
            "topRetailers": ["retailers", "retailer", "retail", "retailYoy"],
            "trafficShareTables": ["aggregationLevel", "brands"],
            "trafficTable": ["aggregationLevel", "bounceRate", "bounceRateYoy", "conversionRate", "conversionRateYoy", "pagesPerSession", "pagesPerSessionYoy", "quality", "qualityYoy", "sessionDuration", "sessionDurationYoy", "sessions", "sessionsYoy"],
            "mediaTable": ["brands"]
        }        
        """

        prompt = f"""
        Given the following user query: "{user_query}",

        and the following JSON schema: "{data_key_explanation}",

        please determine the single most-relevant data_key that maps to the metric, or metrics, required to answer the query. Respond with only the "key:value" pair as a string, separated by a comma, without any additional text, explanation, or quotes.
        """

        messages = [
            {"role": "system", "content": "You are an AI assistant that helps determine the most relevant data_key for a given user query."},
            {"role": "user", "content": prompt}
        ]

        response = client.chat.completions.create(
            model="GPT4-TEST",
            messages=messages,
            temperature=0.0
        )

        data_key_and_metrics = response.choices[0].message.content.strip()

        return data_key_and_metrics

    def detect_data_key_ml(self, user_query):
        # Load the saved model and vectorizer
        classifier_path = Path(__file__).parent.parent.joinpath('ml', 'classifier.pkl')
        vectorizer_path = Path(__file__).parent.parent.joinpath('ml', 'vectorizer.pkl')
        classifier = joblib.load(classifier_path)
        vectorizer = joblib.load(vectorizer_path)

        user_query_vector = vectorizer.transform([user_query])
        predicted_table = classifier.predict(user_query_vector)[0]
        return predicted_table

    # def extract_dimensions_and_metrics(self, user_query, client):

    #     data_schema_explanation = """
    #     The following schema defines the structure of each table, including the accepted arguments (dimensions) and fields (parameters/metrics):

    #     {
    #         "retailCard": {
    #             "arguments": [
    #                 "affiliateId: Int",
    #                 "brandId: Int",
    #                 "businessTypeId: Int",
    #                 "categoryId: Int",
    #                 "channelId: Int",
    #                 "endDate: Date",
    #                 "overlay: String",
    #                 "regionId: Int",
    #                 "startDate: Date"
    #             ],
    #             "fields": [
    #                 "retailAmount: BigInt",
    #                 "retailYoy: Float",
    #                 "dates: DatesType"
    #             ]
    #         },
    #         "consumerTable": {
    #             "arguments": [
    #                 "affiliateId: Int",
    #                 "brandId: Int",
    #                 "businessTypeId: Int",
    #                 "channelId: Int",
    #                 "endDate: Date",
    #                 "projection: String",
    #                 "regionId: Int",
    #                 "startDate: Date"
    #             ],
    #             "fields": [
    #                 "newAmount: Int",
    #                 "newYoy: Float",
    #                 "newPlan: Float",
    #                 "retainedAmount: Int",
    #                 "retainedYoy: Float",
    #                 "retainedPlan: Float",
    #                 "reactivatedAmount: Int",
    #                 "reactivatedYoy: Float",
    #                 "reactivatedPlan: Float",
    #                 "totalAmount: Int",
    #                 "totalYoy: Float",
    #                 "totalPlan: Float",
    #                 "repeat: Float",
    #                 "repeatYoy: Float",
    #                 "retention: Float",
    #                 "retentionYoy: Float",
    #                 "projection: String"
    #             ]
    #         },
    #         "consumerAggregate": {
    #             "arguments": [
    #                 "affiliateId: Int",
    #                 "brandId: Int",
    #                 "businessTypeId: Int",
    #                 "channelId: Int",
    #                 "endDate: Date",
    #                 "projection: String",
    #                 "regionId: Int"
    #             ],
    #             "fields": [
    #                 "new: Int",
    #                 "retained: Int",
    #                 "reactivated: Int",
    #                 "projection: String",
    #                 "dates: DatesType"
    #             ]
    #         }
    #     }
    #     """

    def extract_dimensions_and_metrics(self, user_query, client):

        data_schema_nuances = """
        1. If the user query contains a request for retail sales, please note this has no relation to the region of travel retail. Rather, this is a reference to a retail sales amount.
        2. If the user query contains a request for market share, please assign the data_key the value of "marketRankTable".
        3. If the user query contains a request for foot traffic, please assign the data_key the value of "footTrafficTable".
        4. If the user query contains a request for top retailers, please assign the data_key the value of "topRetailers".
        5. If the user query contains a request for traffic sources, please assign the data_key the value of "trafficSourceTable".
        6. If the user query contains a request for traffic share, please assign the data_key the value of "trafficShareTables".
        7. If the user query contains a request for consumer loyalty information, please assign the data_key the value of "consumerTable".
        8. If the user query contains a request for consumer aggregate information, please assign the data_key the value of "consumerAggregate".
        9. If the user query contains a request for marketing, advertising, and/or promotional information, please assign the data_key the value of "smapTable".
        """

        example_output = """
        {
            "data_key": "retailCard",
            "data_metrics": "retailAmount,retailYoy",
            "brand_name": "Clinique",
            "brand_id": 2,
            "region_name": "All Regions", 
            "region_id": 0,
            "category_name": "All Categories",
            "category_id": 0,
            "start_date": "2022-07-01",
            "end_date": "2023-06-30"
        }
        """

        prompt = f"""
        Given the following user query: {user_query},

        please adhere to the following rules to better contextualize and interpret the user query: {data_schema_nuances},

        with the sole purpose of:
            1. identifying and extracting the correct graphql query arguments (i.e. Brand Name, Region Name, Category Name, and DateTime references).
            2. identifying and extracting the correct graphql query fields (i.e. metric variables).

        An example of the expected output that utilizie the above rules is as follows:
        {example_output}
        """

        # prompt = """
        # Given the following user query: "{user_query}",

        # please adhere to the following rules to better contextualize and interpret the user query: "{data_schema_nuances}",

        # with the sole purpose of:
        #     1. identifying and extracting the correct graphql query arguments (i.e. Brand Name, Region Name, Category Name, and DateTime references).
        #     2. identifying and extracting the correct graphql query fields (i.e. metric variables).

        # An example of the expected output that utilizie the above rules is as follows:
        # {
        #     "data_key": "retailCard",
        #     "data_metrics": "retailAmount,retailYoy",
        #     "brand_name": "Clinique",
        #     "brand_id": 2,
        #     "region_name": "All Regions", 
        #     "region_id": 0,
        #     "category_name": "All Categories",
        #     "category_id": 0,
        #     "start_date": "2022-07-01",
        #     "end_date": "2023-06-30"
        # }
        # """

        messages = [
            {"role": "system", "content": "You are an AI assistant that helps extract dimensions and metrics from a user query based on a provided schema."},
            {"role": "user", "content": prompt}
        ]

        response = client.chat.completions.create(
            model="GPT4-TEST",
            messages=messages,
            temperature=0.0
        )

        dimensions_and_metrics = response.choices[0].message.content.strip()

        return dimensions_and_metrics