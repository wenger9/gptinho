import re
import logging

logger = logging.getLogger(__name__)

class TheValidator:
    @staticmethod
    def check_query_result(expected_result, actual_result):
        metric_name = expected_result["metric"]
        expected_value = expected_result.get(metric_name)
        actual_value = actual_result.get(metric_name)

        if expected_value is not None and actual_value is not None:
            return expected_value == actual_value
        else:
            return False

    @staticmethod
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

    # def check_missing_ids(brand_id, region_id, category_id):
    #     # Check if any of the required identifiers are None and assign default values
    #     if brand_id is None:
    #         brand_id = 0
    #         logger.warning("brand_id not found in the user query. Assigning default value of 0.")
    #     if region_id is None:
    #         region_id = 0
    #         logger.warning("region_id not found in the user query. Assigning default value of 0.")
    #     if category_id is None:
    #         category_id = 0
    #         logger.warning("category_id not found in the user query. Assigning default value of 0.")
        
    #     return brand_id, region_id, category_id

    @staticmethod
    def user_permitted_for_query(query, user):
        brand_match = re.search(r'brandId:\s+(\d+)', query)
        if brand_match:
            query_brand_id = int(brand_match.group(1))
            if not user.brands.filter(mtm_id=query_brand_id).exists():
                return False

        region_match = re.search(r'regionId:\s+(\d+)', query)
        if region_match:
            query_region_id = int(region_match.group(1))
            if not user.regions.filter(mtm_id=query_region_id).exists():
                return False

        return True

# def check_query_result(expected_result, actual_result):
#     metric_name = expected_result["metric"]
#     expected_value = expected_result.get(metric_name)
#     actual_value = actual_result.get(metric_name)

#     if expected_value is not None and actual_value is not None:
#         return expected_value == actual_value
#     else:
#         return False

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