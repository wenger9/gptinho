import json

def load_api_routes(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
        return data['data']['apiRoutes']

def validate_query(query_parameters, api_routes):
    target_route = query_parameters.get('target_data_table')
    
    if target_route is None:
        return False, "Target data table not specified in the query."
    
    route_info = next((route for route in api_routes if route['name'] == target_route), None)
    
    if route_info is None:
        return False, f"Route '{target_route}' not found in the API routes."
    
    valid_parameters = [param['name'] for param in route_info['parameters']]
    # query_param_names = list(query_parameters.keys())
    query_param_names = [param for param in query_parameters.keys() if param != 'target_data_table' and param != 'metrics']


    invalid_parameters = [param for param in query_param_names if param not in valid_parameters]
    
    if invalid_parameters:
        return False, f"Invalid parameters found for route '{target_route}': {', '.join(invalid_parameters)}"
    
    return True, "Query is valid."

# Load the API routes from the JSON file
api_routes = load_api_routes('meta/schema/mtm_api_routes.json')

# Example usage
query_parameters = {
    'brandId': 123,
    'regionId': 456,
    'categoryId': 789,
    'startDate': '2023-01-01',
    'endDate': '2023-12-31',
    'target_data_table': 'consumerAggregate',
    'metrics': ['new', 'retained', 'reactivated']
}

is_valid, message = validate_query(query_parameters, api_routes)

if is_valid:
    print("Query is valid. Proceed with execution.")
else:
    print(f"Error: {message}")