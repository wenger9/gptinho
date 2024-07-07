import csv
import json

def merge_data():
    user_queries = {}
    graphql_payloads = {}
    graphql_responses = {}

    # Read user queries
    with open('user_queries.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row
        for row in reader:
            uid, user_query = row
            user_queries[uid] = user_query

    # Read GraphQL payloads
    with open('graphql_payloads.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row
        for row in reader:
            uid, payload = row
            graphql_payloads[uid] = payload

    # Read GraphQL responses
    with open('graphql_responses.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row
        for row in reader:
            uid, response = row
            graphql_responses[uid] = json.loads(response)

    # Merge data based on UID
    merged_data = []
    for uid in user_queries:
        merged_data.append({
            "user_query": user_queries[uid],
            "generated_graphql_query_payload": graphql_payloads[uid],
            "generated_graphql_query_response": graphql_responses[uid]
        })

    # Serialize merged data to JSON
    example_output = json.dumps(merged_data, indent=2)

    return example_output

# Call the merge_data function
example_output = merge_data()

# Use the example_output variable in the prompt string for OpenAI's API
prompt = f"""
Given the following examples:
{example_output}

...
"""

print(prompt)