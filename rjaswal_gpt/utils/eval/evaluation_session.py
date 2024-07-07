class QueryChecker:
    def __init__(self, expected_result, actual_result):
        self.expected_result = expected_result
        self.actual_result = actual_result

    def check_dimensions(self):
        dimensions = ["brand", "region", "category", "affiliate"]
        for dimension in dimensions:
            expected_value = self.expected_result.get(dimension)
            actual_value = self.actual_result.get(dimension)
            if expected_value and actual_value and expected_value != actual_value:
                return False
        return True

    def check_data_table(self):
        expected_data_key = self.expected_result.get("data_key")
        actual_data_key = self.actual_result.get("data_key")
        return expected_data_key == actual_data_key

    def check_metric_value(self):
        metric_name = self.expected_result.get("metric")
        expected_value = self.expected_result.get(metric_name)
        actual_value = self.actual_result.get(metric_name)
        return expected_value == actual_value

def process_queries(synthetic_queries):
    passed_queries = 0
    failed_queries = 0

    for query_data in synthetic_queries:
        expected_result = query_data["expectedResult"]
        actual_result = query_data["actualResult"]

        checker = QueryChecker(expected_result, actual_result)

        if checker.check_dimensions():
            if checker.check_data_table():
                if checker.check_metric_value():
                    passed_queries += 1
                else:
            else:
                failed_queries += 1
        else:
            failed_queries += 1

    return passed_queries, failed_queries



            # # Compare the result with the expected result
            # if table_data == expected_result:
            #     passed_queries += 1
            # else:
            #     failed_queries += 1

            # # Update progress bar
            # progress = "=" * (index * 20 // total_queries)
            # spaces = " " * (20 - len(progress))
            # print(f"\rProgress: [{progress}{spaces}] {index}/{total_queries} queries processed", end="", flush=True)

        # Save session log
        save_session_log(session_info)

        # Display summary
        # total_queries = passed_queries + failed_queries
        # success_rate = (passed_queries / total_queries) * 100 if total_queries > 0 else 0

        # summary_output = f"""
        # Summary:
        # Total Queries: {total_queries}
        # Passed Queries: {passed_queries}
        # Failed Queries: {failed_queries}
        # Success Rate: {success_rate:.2f}%

        # Results:
        # """

        # for query_info in session_info["queries"]:
        #     result = "Passed" if query_info["actual_result"] == query_info["expected_result"] else "Failed"
        #     summary_output += f"\nQuery: {query_info['user_query']}\nResult: {result}\n"

        # print(summary_output)



# In the main script
def main():
    # Load synthetic queries
    with open("test/synthetic_queries_003.json", "r") as file:
        synthetic_queries = json.load(file)

    # Process queries and get the pass/fail counts
    passed_queries, failed_queries = process_queries(synthetic_queries)

    # Print the summary
    print(f"Passed Queries: {passed_queries}")
    print(f"Failed Queries: {failed_queries}")

if __name__ == "__main__":
    main()