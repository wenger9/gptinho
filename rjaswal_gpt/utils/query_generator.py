# from utils.the_formatter import TheFormatter

class QueryGenerator:
    '''
    This class is used to generate a GraphQL query from a user query.
    It uses the TheFormatter class to format the user query with the brand, region, category, start date, end date, data key, and data metrics.
    It then uses the OpenAI API to generate a GraphQL query from the formatted user query.
    '''
    def __init__(self, schema):
        self.schema = schema

    def generate_graphql_query(self, MODEL_NAME, client, messages, brand_id, region_id, category_id, start_date, end_date, data_key, data_metrics): # formatter: TheFormatter
        # updated_content = messages[3]["content"]

        # # Update the query template with the actual IDs.
        # if brand_id:
        #     updated_content = updated_content.replace("{brand_id}", str(brand_id))
        # else:
        #     updated_content = updated_content.replace("brandId: {brand_id}", "")

        # if region_id:
        #     updated_content = updated_content.replace("{region_id}", str(region_id))
        # else:
        #     updated_content = updated_content.replace("regionId: {region_id}", "")

        # if category_id:
        #     updated_content = updated_content.replace("{category_id}", str(category_id))
        # else:
        #     updated_content = updated_content.replace("categoryId: {category_id}", "")
        
        # if start_date:
        #     updated_content = updated_content.replace("{start_date}", str(start_date))
        # else:
        #     updated_content = updated_content.replace("startDate: {start_date}", "")
        
        # if end_date:
        #     updated_content = updated_content.replace("{end_date}", str(end_date))
        # else:
        #     updated_content = updated_content.replace("endDate: {end_date}", "")
        
        # if data_key:
        #     updated_content = updated_content.replace("{data_key}", str(data_key))
        # else:
        #     updated_content = updated_content.replace("dataKey: {data_key}", "")
        
        # if data_metrics:
        #     updated_content = updated_content.replace("{data_metrics}", str(data_metrics))
        # else:
        #     updated_content = updated_content.replace("dataMetrics: {data_metrics}", "")
        
        # messages[3]["content"] = updated_content

        # messages[3]["content"] = formatter.update_sys_msg(messages[3]["content"], brand_id, region_id, category_id, start_date, end_date, data_key, data_metrics)

        # logger.debug(f"\n--------------------------\nmessages[0]['content']: SYS INSTRUCTION 0 {messages[0]['content']}\n--------------------------\n")
        # logger.debug(f"\n--------------------------\nmessages[1]['content']: SYS INSTRUCTION 1 {messages[1]['content']}\n--------------------------\n")
        # logger.debug(f"\n--------------------------\nmessages[2]['content']: SYS INSTRUCTION 2 {messages[2]['content']}\n--------------------------\n")
        # logger.debug(f"\n--------------------------\nmessages[3]['content']: UPDATED USER MESSAGE {messages[3]['content']}\n--------------------------\n")

        try:
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=messages,
                temperature=0.0
            )
            generated_graphql_query = response.choices[0].message.content.strip() if response.choices else "No query generated."
            # logger.debug(f"\n--------------------------\nresponse.choices[0].message.content: GENERATED GRAPHQL QUERY:\n\n{generated_graphql_query}\n--------------------------\n")

            # Remove \n and \" characters from the generated query
            cleaned_graphql_query = generated_graphql_query.replace('\\n', '').replace('\\"', '"')
            # Remove tickmarks from the beginning and end of the generated graphql query
            # cleaned_graphql_query = cleaned_graphql_query.strip('"')
            # logger.debug(f"\n--------------------------\nCleaned GraphQL Query:\n\n{cleaned_graphql_query}\n--------------------------\n")
            

            return cleaned_graphql_query
        
        except Exception as e:
            # logger.exception("Error generating GraphQL query:")
            return "No query generated."