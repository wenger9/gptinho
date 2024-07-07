import datetime
import json

class SessionLogger:
    def __init__(self, log_directory="log/session"):
        self.log_directory = log_directory

    def save_session_log(self, session_info):
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        log_filename = f"{self.log_directory}/session_log_{timestamp}.json"

        with open(log_filename, "w") as log_file:
            json.dump(session_info, log_file, indent=2)

    def log_query_info(self, user_query, brand_id, region_id, category_id, start_date, end_date,
                       data_key, data_metrics, generated_graphql_query, summary):
        query_info = {
            "user_query": user_query,
            "brand_id": brand_id,
            "region_id": region_id,
            "category_id": category_id,
            "start_date": start_date,
            "end_date": end_date,
            "data_key": data_key,
            "data_metrics": data_metrics,
            "generated_graphql_query": generated_graphql_query,
            "summary": summary
        }

        self.save_session_log(query_info)

        return query_info