import os

import pandas as pd
from databricks import sql as databricks_sql

class DatabricksImporter:
    def __init__(self, table):
        """Set Databricks connection"""
        self.connection = databricks_sql.connect(
            server_hostname=os.environ.get("DATABRICKS_HOST").replace('https://', ''),
            http_path=os.environ.get("DATABRICKS_HTTP_PATH"),
            access_token=os.environ.get("DATABRICKS_TOKEN"),
            _tls_no_verify=True
        )
        self.df = self.get_table(table)
    
    def create_query(self, table):
        return f'SELECT * FROM {table}'

    def query_databricks_table(self, query):
        with self.connection.cursor() as cursor:
            # Get table base data
            cursor.execute(query)
            self.data = cursor.fetchall()

        self.connection.close()
    
    def create_df_from_query(self):
        """Convert raw SQL query into Pandas dataframe"""
        columns = [key for key in self.data[0].asDict()]
        return pd.DataFrame(data=self.data, columns=columns)
    
    def get_table(self, table):
        query = self.create_query(table)
        self.query_databricks_table(query)
        df = self.create_df_from_query()
        return df