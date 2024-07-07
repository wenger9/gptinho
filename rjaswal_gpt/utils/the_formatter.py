# class TheFormatter:
#     '''
#     This class is used to format the messages for the chat completions.
#     It uses the .format() method to ensure the messages are properly formatted.
#     '''
#     # def __init__(self, schema_description):
#     # @staticmethod
#     def format_sys_msg(messages, schema_description, data_key=None, data_metrics=None,
#                         brand_id=None, region_id=None, category_id=None,
#                         start_date=None, end_date=None, affiliate_id=None, user_query=None):
#         formatted_messages = messages.copy()

#         formatted_messages[0]['content'] = formatted_messages[0]['content'].format(schema_description=schema_description)
#         formatted_messages[1]['content'] = formatted_messages[1]['content'].format()
#         formatted_messages[2]['content'] = formatted_messages[2]['content'].format()
#         formatted_messages[3]['content'] = formatted_messages[3]['content'].format(
#             data_key=data_key or "",
#             data_metrics=data_metrics or "",
#             brand_id=brand_id or "None",
#             region_id=region_id or "None",
#             category_id=category_id or "None",
#             start_date=start_date or "None",
#             end_date=end_date or "None",
#             affiliate_id="None",
#             user_query=user_query
#         )

#         return formatted_messages

#     # @staticmethod
#     def update_sys_msg(sys_msg, brand_id=None, region_id=None, category_id=None,
#                      start_date=None, end_date=None, data_key=None, data_metrics=None):
#         # updated_sys_msg = self.format_sys_msg(sys_msg, brand_id, region_id, category_id, start_date, end_date, data_key, data_metrics)
#         updated_sys_msg = format_sys_msg(sys_msg, brand_id, region_id, category_id, start_date, end_date, data_key, data_metrics)


#         if brand_id:
#             updated_sys_msg = updated_sys_msg.replace("{brand_id}", str(brand_id))
#         else:
#             updated_sys_msg = updated_sys_msg.replace("brandId: {brand_id}", "")

#         if region_id:
#             updated_sys_msg = updated_sys_msg.replace("{region_id}", str(region_id))
#         else:
#             updated_sys_msg = updated_sys_msg.replace("regionId: {region_id}", "")

#         if category_id:
#             updated_sys_msg = updated_sys_msg.replace("{category_id}", str(category_id))
#         else:
#             updated_sys_msg = updated_sys_msg.replace("categoryId: {category_id}", "")

#         if start_date:
#             updated_sys_msg = updated_sys_msg.replace("{start_date}", str(start_date))
#         else:
#             updated_sys_msg = updated_sys_msg.replace("startDate: {start_date}", "")

#         if end_date:
#             updated_sys_msg = updated_sys_msg.replace("{end_date}", str(end_date))
#         else:
#             updated_sys_msg = updated_sys_msg.replace("endDate: {end_date}", "")

#         if data_key:
#             updated_sys_msg = updated_sys_msg.replace("{data_key}", str(data_key))
#         else:
#             updated_sys_msg = updated_sys_msg.replace("dataKey: {data_key}", "")

#         if data_metrics:
#             updated_sys_msg = updated_sys_msg.replace("{data_metrics}", str(data_metrics))
#         else:
#             updated_sys_msg = updated_sys_msg.replace("dataMetrics: {data_metrics}", "")

#         return updated_sys_msg