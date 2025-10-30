# Takes two lists of dictionaries (products and users) as input.
# Converts both into pandas DataFrames.
# Performs a left-join/merge to enrich the product data with seller information (username, email, and name) using the user ID present in the product data.
# Handles cases where a product's user might not be in the user list (though unlikely with this API, it's a critical real-world check).
# Calculates a new column revenue (price * quantity from the rating object, assuming rating.count is quantity for this exercise).
import pandas as pd
from pprint import pprint

class DataEnricher:
    
    def __init__(self, products_data, users_data):
        self.products_data = products_data
        self.users_data = users_data
        
    
    def _convert_products_to_df(self):
        # Columns I want: id, category, price, quentity, rrating
        return pd.DataFrame([{
            "id": item.get("id"),
            "category": item.get("category"),
            "price": item.get("price"),
            "quantity": item.get("rating", None).get("count", None),
            "rating": item.get("rating", None).get("rate", None)
        } for item in self.products_data])
        
        
    def _convert_users_to_df(self):
        # Username, email, name
        return pd.DataFrame([{
            "id": item.get("id", None),
            "email": item.get("email"),
            "user_name": item.get("username"),
            "first_name": item.get("name", None).get("firstname", None),
            "last_name": item.get("name", None).get("lastname", None)
        } for item in self.users_data])
    
        
    def _join_data(self):
        products_df = self._convert_products_to_df()
        users_df = self._convert_users_to_df()
        
        # merged_df = pd.me 
        return pd.merge(products_df, users_df, on='id', how='left')
    
    
    def enrich_data(self):
        enriched_df = self._join_data()
        enriched_df["revenue"] = enriched_df["quantity"] * enriched_df["price"]
        
        return enriched_df