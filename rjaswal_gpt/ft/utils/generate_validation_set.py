import json

validation_data = {
    "smapTable": [
        {"prompt": "What is the marketing cost for Clinique in Q1 2023 in EMEA?", "completion": "smapTable"},
        {"prompt": "Show me the total spend for Estee Lauder in North America in 2023.", "completion": "smapTable"},
        {"prompt": "Advertising expenses for MAC in the second quarter of 2022 in Asia.", "completion": "smapTable"},
        {"prompt": "What were the promotion costs for Tom Ford Beauty from June 1 2022 to Aug 15 2022 in Europe?", "completion": "smapTable"},
        {"prompt": "Total marketing expenses for Jo Malone London in USA for last fiscal year.", "completion": "smapTable"}
    ],
    "financeCard": [
        {"prompt": "What are the net amounts for Clinique in Q1 2023 in EMEA?", "completion": "financeCard"},
        {"prompt": "Show me the margin budget for Estee Lauder in North America in 2023.", "completion": "financeCard"},
        {"prompt": "NOP budget for MAC in the second quarter of 2022 in Asia.", "completion": "financeCard"},
        {"prompt": "What were the gross to net amounts for Tom Ford Beauty from June 1 2022 to Aug 15 2022 in Europe?", "completion": "financeCard"},
        {"prompt": "Total net amounts for Jo Malone London in USA for last fiscal year.", "completion": "financeCard"}
    ],
    "retailChart": [
        {"prompt": "Show me the retail chart for Clinique in Q1 2023 in EMEA.", "completion": "retailChart"},
        {"prompt": "Retail chart for Estee Lauder in North America in 2023.", "completion": "retailChart"},
        {"prompt": "Retail sales for MAC in the second quarter of 2022 in Asia.", "completion": "retailChart"},
        {"prompt": "Show me the retail performance for Tom Ford Beauty from June 1 2022 to Aug 15 2022 in Europe.", "completion": "retailChart"},
        {"prompt": "Total retail figures for Jo Malone London in USA for last fiscal year.", "completion": "retailChart"}
    ],
    "topRetailers": [
        {"prompt": "Who are the top retailers for Clinique in Q1 2023 in EMEA?", "completion": "topRetailers"},
        {"prompt": "Top retailers for Estee Lauder in North America in 2023.", "completion": "topRetailers"},
        {"prompt": "Retailer ranking for MAC in the second quarter of 2022 in Asia.", "completion": "topRetailers"},
        {"prompt": "Show me the top retailers for Tom Ford Beauty from June 1 2022 to Aug 15 2022 in Europe.", "completion": "topRetailers"},
        {"prompt": "Top performing retailers for Jo Malone London in USA for last fiscal year.", "completion": "topRetailers"}
    ],
    "consumerAggregate": [
        {"prompt": "How many new consumers for Clinique in Q1 2023 in EMEA?", "completion": "consumerAggregate"},
        {"prompt": "Show me the reactivated consumers for Estee Lauder in North America in 2023.", "completion": "consumerAggregate"},
        {"prompt": "Total retained consumers for MAC in the second quarter of 2022 in Asia.", "completion": "consumerAggregate"},
        {"prompt": "Show me the consumer engagement for Tom Ford Beauty from June 1 2022 to Aug 15 2022 in Europe.", "completion": "consumerAggregate"},
        {"prompt": "New consumers for Jo Malone London in USA for last fiscal year.", "completion": "consumerAggregate"}
    ]
}

# Flatten the data and write to JSONL
all_data = []
for key, value in validation_data.items():
    all_data.extend(value)

with open('validation_data.jsonl', 'w') as outfile:
    for entry in all_data:
        json.dump(entry, outfile)
        outfile.write('\n')
